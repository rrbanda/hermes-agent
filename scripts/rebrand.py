#!/usr/bin/env python3
"""Write brand.json and the packaging command table.

Python reads brand.json at runtime. The only file this script rewrites is
pyproject.toml [project.scripts], because setuptools reads that table as text
and cannot call the brand loader. Python modules stay hermes_cli.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")

_MAIN_SCRIPT = re.compile(
    r'(?m)^[A-Za-z0-9][\w.-]* = "hermes_cli\.main:main"$')
_ACP_SCRIPT = re.compile(
    r'(?m)^[A-Za-z0-9][\w.-]* = "acp_adapter\.entry:main"$')


def _replace(path: Path, pattern: re.Pattern[str], repl: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = pattern.subn(repl, text, count=1)
    if count != 1:
        raise SystemExit(f"{path.relative_to(ROOT)}: expected one {label}, found {count}")
    path.write_text(updated, encoding="utf-8")


def rebrand(cli: str, name: str) -> None:
    if not CLI_RE.fullmatch(cli):
        raise SystemExit("--cli must be a lowercase command name (letters, digits, hyphens)")
    if not name or any(ch in name for ch in "\r\n") or len(name) > 64:
        raise SystemExit("--name must be one line, 1-64 characters")
    acp = f"{cli}-acp"
    _replace(
        ROOT / "pyproject.toml",
        _MAIN_SCRIPT,
        f'{cli} = "hermes_cli.main:main"',
        "main script entry",
    )
    _replace(
        ROOT / "pyproject.toml",
        _ACP_SCRIPT,
        f'{acp} = "acp_adapter.entry:main"',
        "acp script entry",
    )
    brand = {"cli": cli, "name": name}
    (ROOT / "brand.json").write_text(json.dumps(brand, indent=2) + "\n", encoding="utf-8")
    print(f"branded as {name} (command: {cli})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set the user-facing product name for this checkout.")
    parser.add_argument("--cli", required=True, help="Command name, for example xyz")
    parser.add_argument("--name", required=True, help="Display name, for example Xyz")
    args = parser.parse_args(argv)
    rebrand(args.cli, args.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
