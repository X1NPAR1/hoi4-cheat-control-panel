"""Builds the Workshop payload and proves it contains nothing it should not.

    python tools/build_release.py

Copies mod/ to dist/<name>/ through a whitelist: only the file types the game
actually loads are carried across, so documentation, tooling, repository metadata
and stray editor files cannot reach the Workshop even by accident.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp.checks import ALL_CHECKS, Report
from ccp.meta import MOD_VERSION

REPO_ROOT = Path(__file__).resolve().parent.parent
MOD = REPO_ROOT / "mod"
DIST = REPO_ROOT / "dist"

ALLOWED_SUFFIXES = {".mod", ".txt", ".gui", ".gfx", ".yml", ".png", ".dds", ".tga"}
ALLOWED_ROOT_FILES = {"descriptor.mod", "thumbnail.png"}
ALLOWED_TOP_LEVEL = {"common", "interface", "gfx", "localisation"}


def collect() -> tuple[list[Path], list[Path]]:
    carried: list[Path] = []
    skipped: list[Path] = []
    for path in sorted(MOD.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(MOD)
        top = relative.parts[0]
        allowed = (
            relative.name in ALLOWED_ROOT_FILES
            if len(relative.parts) == 1
            else top in ALLOWED_TOP_LEVEL and path.suffix in ALLOWED_SUFFIXES
        )
        (carried if allowed else skipped).append(relative)
    return carried, skipped


def main() -> int:
    report = Report()
    for _, check in ALL_CHECKS:
        check(REPO_ROOT, MOD, report)
    if not report.ok:
        print("Release checklist failed; not building.", file=sys.stderr)
        for message in report.errors:
            print(f"  error: {message}", file=sys.stderr)
        return 1

    carried, skipped = collect()

    target = DIST / "hoi4_cheat_control_panel"
    if target.exists():
        shutil.rmtree(target)
    for relative in carried:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MOD / relative, destination)

    size = sum((target / relative).stat().st_size for relative in carried)
    print(f"HOI4 Cheat Control Panel {MOD_VERSION}")
    print(f"  {target}")
    print(f"  {len(carried)} files, {size / 1024:.0f} KB")
    if skipped:
        print(f"  {len(skipped)} file(s) excluded by the whitelist:")
        for relative in skipped:
            print(f"    {relative.as_posix()}")
    else:
        print("  nothing excluded — mod/ already contains only shippable files")

    print("\nUpload this directory with the Paradox Launcher: Mods -> Upload mod.")
    print("Hearts of Iron IV does not use SteamCMD for Workshop uploads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
