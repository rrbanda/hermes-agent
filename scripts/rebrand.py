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


def _clean_tagline(tagline: str) -> str:
    text = tagline.strip()
    if any(ch in text for ch in "\r\n") or len(text) > 120:
        raise SystemExit("--tagline must be one line, at most 120 characters")
    return text


def _clean_hero(hero: str) -> str:
    from hermes_constants import accepted_brand_hero

    cleaned = accepted_brand_hero(hero)
    if hero.strip() and not cleaned:
        raise SystemExit("--hero must be at most 30 lines, 80 columns each")
    return cleaned


def _read_brand() -> dict:
    path = ROOT / "brand.json"
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return raw if isinstance(raw, dict) else {}


def _kept_hero() -> str:
    hero = _read_brand().get("hero")
    if not isinstance(hero, str):
        return ""
    try:
        return _clean_hero(hero)
    except SystemExit:
        return ""


def _kept_tagline() -> str:
    tagline = _read_brand().get("tagline")
    if not isinstance(tagline, str):
        return ""
    try:
        return _clean_tagline(tagline)
    except SystemExit:
        return ""


def rebrand(cli: str, name: str, tagline: str | None = None, hero: str | None = None) -> None:
    if not CLI_RE.fullmatch(cli):
        raise SystemExit("--cli must be a lowercase command name (letters, digits, hyphens)")
    if not name or any(ch in name for ch in "\r\n") or len(name) > 64:
        raise SystemExit("--name must be one line, 1-64 characters")
    if tagline is None:
        tagline = _kept_tagline()
    else:
        tagline = _clean_tagline(tagline)
    if hero is None:
        hero = _kept_hero()
    else:
        hero = _clean_hero(hero)
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
    if tagline:
        brand["tagline"] = tagline
    if hero:
        brand["hero"] = hero
    (ROOT / "brand.json").write_text(json.dumps(brand, indent=2) + "\n", encoding="utf-8")
    print(f"branded as {name} (command: {cli})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set the user-facing product name for this checkout.")
    parser.add_argument("--cli", required=True, help="Command name, for example xyz")
    parser.add_argument("--name", required=True, help="Display name, for example Xyz")
    parser.add_argument(
        "--tagline",
        default=None,
        help="Chat banner slogan. Omit this to keep the previous one. An empty value clears it.",
    )
    parser.add_argument(
        "--hero",
        default=None,
        help="Session-panel figure. Empty clears it. Omit this to keep the previous one.",
    )
    parser.add_argument(
        "--hero-file",
        default=None,
        help="Read the session-panel figure from a text file. At most 30 lines, 80 columns.",
    )
    args = parser.parse_args(argv)
    hero = args.hero
    if args.hero_file is not None:
        if hero is not None:
            raise SystemExit("pass either --hero or --hero-file")
        try:
            hero = Path(args.hero_file).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise SystemExit(f"could not read --hero-file: {exc}") from exc
    rebrand(args.cli, args.name, args.tagline, hero)
    return 0


if __name__ == "__main__":
    sys.exit(main())
