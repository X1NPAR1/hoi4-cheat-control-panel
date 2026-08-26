"""Regenerates the panel's interface, scripts and hand-authored localisation.

    python tools/build_interface.py

Everything it writes is derived from the registries in tools/ccp/, so layout,
navigation, effects and strings are guaranteed to agree with each other.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp import interface
from ccp.equipment import group_by_category, load_catalogue
from ccp.technology import group_by_folder
from ccp.technology import load_catalogue as load_technologies
from ccp.layout import emit_file
from ccp.meta import descriptor
from ccp.scripts import (
    emit_action_effects,
    emit_core_effects,
    emit_country_effects,
    emit_state_effects,
    emit_scripted_gui,
    emit_scripted_localisation,
)
from ccp.languages import NATIVE, OVERLAY
from ccp.strings import emit_localisation
from generate_data import find_game_dir, game_version

REPO_ROOT = Path(__file__).resolve().parent.parent
MOD = REPO_ROOT / "mod"
OVERLAYS = REPO_ROOT / "extras" / "language_overlays"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix == ".yml" else "utf-8"
    path.write_text(content, encoding=encoding, newline="\n")
    print(f"  {path.relative_to(REPO_ROOT).as_posix():<62} {len(content.splitlines()):>5} lines")


def main() -> int:
    game_dir = find_game_dir(None)
    version = game_version(game_dir)
    categories = list(group_by_category(load_catalogue(game_dir)))
    folders = list(group_by_folder(load_technologies(game_dir)))
    print(f"Target game version: {version}\n")

    print("Written:")
    write(MOD / "descriptor.mod", descriptor())
    write(
        MOD / "interface" / "ccp_main.gui",
        emit_file(
            interface.main_window(categories, folders),
            interface.equipment_entry_window(),
            interface.research_entry_window(),
            interface.country_entry_window(),
            interface.state_entry_window(),
            interface.state_picker_window(),
            interface.modal_window(),
        ),
    )
    write(MOD / "interface" / "ccp_launcher.gui", emit_file(interface.launcher_window()))
    write(MOD / "interface" / "ccp_hotkeys.gui", emit_file(interface.hotkey_window()))

    write(
        MOD / "common" / "scripted_guis" / "ccp_generated_gui.txt",
        emit_scripted_gui(version, categories, folders),
    )
    write(
        MOD / "common" / "scripted_effects" / "ccp_generated_core.txt",
        emit_core_effects(version),
    )
    write(
        MOD / "common" / "scripted_effects" / "ccp_generated_country.txt",
        emit_country_effects(version),
    )
    write(
        MOD / "common" / "scripted_effects" / "ccp_generated_actions.txt",
        emit_action_effects(version),
    )
    write(
        MOD / "common" / "scripted_effects" / "ccp_generated_state.txt",
        emit_state_effects(version),
    )
    write(
        MOD / "common" / "scripted_localisation" / "ccp_generated_core_loc.txt",
        emit_scripted_localisation(version),
    )

    for language in NATIVE:
        write(
            MOD / "localisation" / language / f"ccp_core_l_{language}.yml",
            emit_localisation(language),
        )

    for language in OVERLAY:
        write(
            OVERLAYS / language / f"ccp_core_l_english.yml",
            emit_localisation(language).replace(f"l_{language}:", "l_english:", 1),
        )

    for language_dir in sorted((MOD / "localisation").iterdir()):
        if language_dir.is_dir() and language_dir.name not in NATIVE:
            for stale in sorted(language_dir.iterdir()):
                stale.unlink()
            language_dir.rmdir()
            print(f"  removed unsupported localisation/{language_dir.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
