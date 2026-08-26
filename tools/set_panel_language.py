"""Switches the installed panel to Turkish or Dutch.

    python tools/set_panel_language.py turkish
    python tools/set_panel_language.py --restore

Hearts of Iron IV loads exactly ten localisation folders and neither Turkish nor
Dutch is among them, so those translations cannot ship as a language of their own.
They are written to extras/language_overlays/ under English keys instead, and this
copies the chosen one over the *installed* mod's English localisation.

It never touches the repository, so the shipped mod always stays English for
English players. The game itself stays in English too; only this panel changes.
`--restore` copies the repository's English strings back over the install.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp.languages import DISPLAY_NAMES, OVERLAY
from install_local import FOLDER_NAME, game_data_dir

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERLAYS = REPO_ROOT / "extras" / "language_overlays"
REPO_ENGLISH = REPO_ROOT / "mod" / "localisation" / "english"


def installed_english() -> Path:
    return game_data_dir() / "mod" / FOLDER_NAME / "localisation" / "english"


def copy_into(source: Path, target: Path) -> int:
    if not target.is_dir():
        print(
            f"{target} not found.\nRun tools/install_local.py first.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    copied = 0
    for path in sorted(source.glob("*.yml")):
        shutil.copy2(path, target / path.name)
        copied += 1
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", nargs="?", choices=sorted(OVERLAY))
    parser.add_argument(
        "--restore", action="store_true", help="Put the English strings back"
    )
    args = parser.parse_args()

    if not args.restore and not args.language:
        parser.error("give a language, or --restore")

    target = installed_english()

    if args.restore:
        copied = copy_into(REPO_ENGLISH, target)
        print(f"Panel language restored to English ({copied} file(s)).")
        return 0

    source = OVERLAYS / args.language
    if not source.is_dir():
        print(f"{source} not found. Run tools/build_interface.py first.", file=sys.stderr)
        return 2

    copied = copy_into(source, target)
    print(f"Panel language set to {DISPLAY_NAMES[args.language]} ({copied} file(s)).")
    print(f"  {target}")
    print("\nThe game itself stays in English; only this panel changes.")
    print("Reinstalling with tools/install_local.py resets it to English.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
