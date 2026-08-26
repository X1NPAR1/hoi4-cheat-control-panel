"""Regenerates the mod's data-driven script from the installed Hearts of Iron IV files.

    python tools/generate_data.py [--game-dir PATH]

Writes into mod/common/scripted_effects/ and mod/common/scripted_localisation/.
Everything it writes carries a GENERATED banner and must never be hand-edited.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp.emit import (
    emit_category_localisation,
    emit_equipment_categories_localisation,
    emit_equipment_effects,
    emit_equipment_localisation,
)
from ccp.equipment import group_by_category, load_catalogue
from ccp.languages import NATIVE, OVERLAY

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_GAME_DIRS = [
    Path(r"D:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
    Path(r"C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV"),
    Path(r"C:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
    Path(r"E:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
    Path(r"F:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
]


def find_game_dir(explicit: str | None) -> Path:
    candidates = [Path(explicit)] if explicit else DEFAULT_GAME_DIRS
    for candidate in candidates:
        if (candidate / "launcher-settings.json").is_file():
            return candidate
    searched = "\n  ".join(str(path) for path in candidates)
    raise SystemExit(f"Hearts of Iron IV was not found. Searched:\n  {searched}")


def game_version(game_dir: Path) -> str:
    settings = json.loads((game_dir / "launcher-settings.json").read_text(encoding="utf-8-sig"))
    return settings.get("rawVersion", "unknown")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix == ".yml" else "utf-8"
    path.write_text(content, encoding=encoding, newline="\n")
    print(f"  {path.relative_to(REPO_ROOT).as_posix():<70} {len(content.splitlines()):>6} lines")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", help="Path to the Hearts of Iron IV install directory")
    args = parser.parse_args()

    game_dir = find_game_dir(args.game_dir)
    version = game_version(game_dir)
    print(f"Game: {game_dir}")
    print(f"Version: {version}\n")

    catalogue = load_catalogue(game_dir)
    if not catalogue:
        raise SystemExit("No equipment was parsed. The game files may be unreadable.")

    grouped = group_by_category(catalogue)
    print(f"Equipment: {len(catalogue)} variants across {len(grouped)} categories")
    for name, items in grouped.items():
        print(f"  {name:<20} {len(items):>4}")
    print()

    effects = REPO_ROOT / "mod" / "common" / "scripted_effects"
    scripted_loc = REPO_ROOT / "mod" / "common" / "scripted_localisation"

    print("Written:")
    write(effects / "ccp_generated_equipment.txt", emit_equipment_effects(catalogue, version))
    write(
        scripted_loc / "ccp_generated_equipment_loc.txt",
        emit_equipment_localisation(catalogue, version),
    )
    write(
        scripted_loc / "ccp_generated_equipment_categories_loc.txt",
        emit_equipment_categories_localisation(catalogue, version),
    )
    for language in NATIVE:
        write(
            REPO_ROOT / "mod" / "localisation" / language
            / f"ccp_generated_equipment_l_{language}.yml",
            emit_category_localisation(catalogue, language, version),
        )

    for language in OVERLAY:
        write(
            REPO_ROOT / "extras" / "language_overlays" / language
            / "ccp_generated_equipment_l_english.yml",
            emit_category_localisation(catalogue, language, version),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
