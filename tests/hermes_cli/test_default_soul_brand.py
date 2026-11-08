"""The seeded persona follows the checkout brand, and an unedited Hermes seed upgrades."""

import pytest

from hermes_cli.config import _ensure_default_soul_md
from hermes_cli.default_soul import DEFAULT_SOUL_MD, _UNBRANDED_SOUL_MD, is_legacy_template_soul
from hermes_constants import brand_cli, brand_display_name


def test_stock_soul_names_the_active_brand():
    assert DEFAULT_SOUL_MD.startswith(f"You are {brand_display_name()}")
    if brand_cli() == "hermes":
        assert "built by Nous Research" in DEFAULT_SOUL_MD
        return
    assert "Hermes" not in DEFAULT_SOUL_MD
    assert "Nous Research" not in DEFAULT_SOUL_MD
    assert is_legacy_template_soul(_UNBRANDED_SOUL_MD)


@pytest.mark.skipif(brand_cli() == "hermes", reason="upstream seed is already the active persona")
def test_unedited_hermes_soul_upgrades_when_rebranded(tmp_path):
    soul = tmp_path / "SOUL.md"
    soul.write_text(_UNBRANDED_SOUL_MD, encoding="utf-8")
    _ensure_default_soul_md(tmp_path)
    assert soul.read_text(encoding="utf-8") == DEFAULT_SOUL_MD
