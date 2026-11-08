"""The rebrand script accepts any command name and can replace a previous one."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "rebrand.py"

_PYPROJECT = """\
[project.scripts]
hermes = "hermes_cli.main:main"
hermes-agent = "agent.legacy_cli:main"
hermes-acp = "acp_adapter.entry:main"
"""


def _rebrand_module(tmp_path: Path):
    spec = importlib.util.spec_from_file_location("rebrand_checkout_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = tmp_path
    (tmp_path / "pyproject.toml").write_text(_PYPROJECT, encoding="utf-8")
    return module


def test_rebrand_writes_manifest_and_both_script_lines(tmp_path: Path):
    module = _rebrand_module(tmp_path)
    module.rebrand("acme", "Acme")
    brand = json.loads((tmp_path / "brand.json").read_text(encoding="utf-8"))
    text = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert brand == {"cli": "acme", "name": "Acme"}
    assert 'acme = "hermes_cli.main:main"' in text
    assert 'acme-acp = "acp_adapter.entry:main"' in text
    assert 'hermes-agent = "agent.legacy_cli:main"' in text
    assert "hermes = " not in text
    assert "hermes-acp = " not in text


def test_second_rebrand_replaces_the_previous_name(tmp_path: Path):
    module = _rebrand_module(tmp_path)
    module.rebrand("xyz", "Xyz")
    module.rebrand("acme", "Acme")
    brand = json.loads((tmp_path / "brand.json").read_text(encoding="utf-8"))
    text = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert brand == {"cli": "acme", "name": "Acme"}
    assert text.count('= "hermes_cli.main:main"') == 1
    assert text.count('= "acp_adapter.entry:main"') == 1
    assert "xyz = " not in text
    assert "xyz-acp = " not in text


@pytest.mark.parametrize("cli,name", [("Xyz", "Xyz"), ("", "Acme"), ("acme", ""), ("acme", "A\nB")])
def test_rebrand_rejects_a_bad_cli_or_name(tmp_path: Path, cli: str, name: str):
    module = _rebrand_module(tmp_path)
    with pytest.raises(SystemExit):
        module.rebrand(cli, name)
    assert not (tmp_path / "brand.json").exists()
