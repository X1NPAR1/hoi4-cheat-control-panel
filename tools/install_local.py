"""Installs the working copy into the game's local mod directory for testing.

    python tools/install_local.py

Copies mod/ to Documents/Paradox Interactive/Hearts of Iron IV/mod/<folder>/ and
writes the matching .mod descriptor. Copying rather than linking keeps the game
away from the repository path, which may contain characters the engine mishandles.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MOD_DIR = REPO_ROOT / "mod"
FOLDER_NAME = "hoi4_cheat_control_panel"


def game_data_dir() -> Path:
    documents = Path(os.environ.get("USERPROFILE", Path.home())) / "Documents"
    return documents / "Paradox Interactive" / "Hearts of Iron IV"


def descriptor_fields() -> dict[str, str]:
    text = (MOD_DIR / "descriptor.mod").read_text(encoding="utf-8-sig")
    return {
        key: value
        for key, value in re.findall(r'^\s*(\w+)\s*=\s*"([^"]*)"', text, re.MULTILINE)
    }


def main() -> int:
    data_dir = game_data_dir()
    if not data_dir.is_dir():
        print(f"Game data directory not found: {data_dir}", file=sys.stderr)
        return 2

    target = data_dir / "mod" / FOLDER_NAME
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(MOD_DIR, target)

    fields = descriptor_fields()
    source = (MOD_DIR / "descriptor.mod").read_text(encoding="utf-8-sig").rstrip()
    descriptor = f'{source}\npath="{target.as_posix()}"\n'
    (data_dir / "mod" / f"{FOLDER_NAME}.mod").write_text(
        descriptor, encoding="utf-8", newline="\n"
    )

    files = sum(1 for path in target.rglob("*") if path.is_file())
    size = sum(path.stat().st_size for path in target.rglob("*") if path.is_file())
    print(f"Installed {fields.get('name', FOLDER_NAME)} {fields.get('version', '')}".rstrip())
    print(f"  {target}")
    print(f"  {files} files, {size / 1024:.0f} KB")
    print(f"  descriptor: {data_dir / 'mod' / (FOLDER_NAME + '.mod')}")
    print()
    print("Enable it in the Paradox Launcher playset, then start the game.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
