"""Installs the working copy into the game's local mod directory for testing.

    python tools/install_local.py

Copies mod/ to Documents/Paradox Interactive/Hearts of Iron IV/mod/<folder>/ and
writes the matching .mod descriptor. Copying rather than linking keeps the game
away from the repository path, which may contain characters the engine mishandles.

    python tools/install_local.py --language turkish

Hearts of Iron IV has no localisation folder for Turkish or Dutch, so those
translations ship as an overlay that replaces the English files. An overlay
already in place is detected and reapplied, because an install that silently put
the panel back into English every time would be its own bug.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MOD_DIR = REPO_ROOT / "mod"
FOLDER_NAME = "hoi4_cheat_control_panel"
OVERLAY_DIR = REPO_ROOT / "extras" / "language_overlays"
BASE_LANGUAGE = "english"


def overlay_languages() -> list[str]:
    if not OVERLAY_DIR.is_dir():
        return []
    return sorted(path.name for path in OVERLAY_DIR.iterdir() if path.is_dir())


def installed_overlay(target: Path) -> str | None:
    """Which overlay, if any, the copy being replaced was carrying."""
    for language in overlay_languages():
        files = sorted((OVERLAY_DIR / language).glob("*.yml"))
        if not files:
            continue
        if all(
            (target / "localisation" / BASE_LANGUAGE / path.name).is_file()
            and (target / "localisation" / BASE_LANGUAGE / path.name).read_bytes()
            == path.read_bytes()
            for path in files
        ):
            return language
    return None


def apply_overlay(target: Path, language: str) -> int:
    source = OVERLAY_DIR / language
    if not source.is_dir():
        raise SystemExit(f"no overlay for {language}; have {overlay_languages()}")
    destination = target / "localisation" / BASE_LANGUAGE
    count = 0
    for path in sorted(source.glob("*.yml")):
        shutil.copy2(path, destination / path.name)
        count += 1
    return count


def game_data_dir() -> Path:
    documents = Path(os.environ.get("USERPROFILE", Path.home())) / "Documents"
    return documents / "Paradox Interactive" / "Hearts of Iron IV"


def descriptor_fields(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    return {
        key: value
        for key, value in re.findall(r'^\s*(\w+)\s*=\s*"([^"]*)"', text, re.MULTILINE)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--language",
        choices=[BASE_LANGUAGE, *overlay_languages()],
        help="overlay to apply; omit to keep whatever the installed copy has",
    )
    options = parser.parse_args()

    data_dir = game_data_dir()
    if not data_dir.is_dir():
        print(f"Game data directory not found: {data_dir}", file=sys.stderr)
        return 2

    target = data_dir / "mod" / FOLDER_NAME
    outer = data_dir / "mod" / f"{FOLDER_NAME}.mod"

    # The launcher writes remote_file_id once the mod is published; it is the only
    # link between this folder and its Workshop item. Reinstalling must not drop it,
    # or the next upload would create a second entry instead of updating the first.
    published = descriptor_fields(outer).get("remote_file_id") or descriptor_fields(
        target / "descriptor.mod"
    ).get("remote_file_id")

    language = options.language or installed_overlay(target)

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(MOD_DIR, target)

    overlaid = 0
    if language and language != BASE_LANGUAGE:
        overlaid = apply_overlay(target, language)

    source = (MOD_DIR / "descriptor.mod").read_text(encoding="utf-8-sig").rstrip()
    if published:
        source += f'\nremote_file_id="{published}"'
        (target / "descriptor.mod").write_text(source + "\n", encoding="utf-8", newline="\n")

    fields = descriptor_fields(target / "descriptor.mod")
    outer.write_text(f'{source}\npath="{target.as_posix()}"\n', encoding="utf-8", newline="\n")

    files = sum(1 for path in target.rglob("*") if path.is_file())
    size = sum(path.stat().st_size for path in target.rglob("*") if path.is_file())
    print(f"Installed {fields.get('name', FOLDER_NAME)} {fields.get('version', '')}".rstrip())
    print(f"  {target}")
    print(f"  {files} files, {size / 1024:.0f} KB")
    print(f"  descriptor: {data_dir / 'mod' / (FOLDER_NAME + '.mod')}")
    if overlaid:
        print(f"  language: {language} overlay, {overlaid} file(s) over english")
    else:
        print(f"  language: {BASE_LANGUAGE}, following the game's setting")
    print()
    print("Enable it in the Paradox Launcher playset, then start the game.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
