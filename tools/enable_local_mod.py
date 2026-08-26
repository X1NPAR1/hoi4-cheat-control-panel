"""Adds the locally installed mod to the Paradox Launcher playset and gives it a thumbnail.

    python tools/enable_local_mod.py [--playset NAME]

The launcher registers a discovered local mod in its `mods` table but does not
always add it to a playset, which leaves it visible in the library yet absent
from the playset list. It also leaves `thumbnailPath` empty for local mods, so
the mod shows without its logo. This fixes both.

The launcher must be closed: it holds the database open and rewrites it on exit.
The database is backed up next to itself before anything is changed.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DESCRIPTOR_NAME = "hoi4_cheat_control_panel.mod"


def game_data_dir() -> Path:
    documents = Path(os.environ.get("USERPROFILE", Path.home())) / "Documents"
    return documents / "Paradox Interactive" / "Hearts of Iron IV"


def launcher_is_running() -> bool:
    try:
        output = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Paradox Launcher.exe"],
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return "Paradox Launcher.exe" in output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--playset", help="Playset to add the mod to (default: the only one)")
    parser.add_argument(
        "--force", action="store_true", help="Proceed even while the launcher is running"
    )
    args = parser.parse_args()

    if launcher_is_running() and not args.force:
        print(
            "The Paradox Launcher is running. Close it completely, then run this again.\n"
            "It holds the database open and rewrites it on exit, so changes made now "
            "would be discarded.",
            file=sys.stderr,
        )
        return 2

    data_dir = game_data_dir()
    database = data_dir / "launcher-v2.sqlite"
    if not database.is_file():
        print(f"Launcher database not found: {database}", file=sys.stderr)
        return 2

    registry_id = f"mod/{DESCRIPTOR_NAME}"
    thumbnail = data_dir / "mod" / "hoi4_cheat_control_panel" / "thumbnail.png"
    if not thumbnail.is_file():
        print(f"Thumbnail not found: {thumbnail}\nRun tools/install_local.py first.", file=sys.stderr)
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = database.with_name(f"launcher-v2.sqlite.{stamp}.bak")
    shutil.copy2(database, backup)
    print(f"Backed up database to {backup.name}")

    connection = sqlite3.connect(database)
    try:
        row = connection.execute(
            "select id, displayName from mods where gameRegistryId = ?", (registry_id,)
        ).fetchone()
        if row is None:
            print(
                f"The launcher has not registered `{registry_id}` yet.\n"
                "Open the launcher once so it scans the mod directory, close it, then rerun.",
                file=sys.stderr,
            )
            return 1
        mod_id, display_name = row

        connection.execute(
            "update mods set thumbnailPath = ? where id = ?", (str(thumbnail), mod_id)
        )

        if args.playset:
            playsets = connection.execute(
                "select id, name from playsets where name = ? and isRemoved = 0", (args.playset,)
            ).fetchall()
        else:
            playsets = connection.execute(
                "select id, name from playsets where isRemoved = 0"
            ).fetchall()
        if not playsets:
            print("No playset found to add the mod to.", file=sys.stderr)
            return 1

        for playset_id, playset_name in playsets:
            existing = connection.execute(
                "select enabled from playsets_mods where playsetId = ? and modId = ?",
                (playset_id, mod_id),
            ).fetchone()
            if existing is None:
                position = connection.execute(
                    "select coalesce(max(position), -1) + 1 from playsets_mods where playsetId = ?",
                    (playset_id,),
                ).fetchone()[0]
                connection.execute(
                    "insert into playsets_mods (playsetId, modId, enabled, position) "
                    "values (?, ?, 1, ?)",
                    (playset_id, mod_id, position),
                )
                print(f"Added to playset `{playset_name}` at position {position}, enabled")
            else:
                connection.execute(
                    "update playsets_mods set enabled = 1 where playsetId = ? and modId = ?",
                    (playset_id, mod_id),
                )
                print(f"Enabled in playset `{playset_name}`")

        active = connection.execute(
            "select count(*) from playsets where isActive = 1 and isRemoved = 0"
        ).fetchone()[0]
        if active == 0:
            chosen = playsets[0][0]
            connection.execute("update playsets set isActive = 1 where id = ?", (chosen,))
            print(
                f"Activated playset `{playsets[0][1]}` - no playset was active, "
                "which makes the launcher start the game with no mods at all"
            )

        connection.commit()
    finally:
        connection.close()

    load_file = data_dir / "dlc_load.json"
    payload = {"enabled_mods": [], "disabled_dlcs": []}
    if load_file.is_file():
        payload = json.loads(load_file.read_text(encoding="utf-8"))
    enabled = payload.get("enabled_mods", [])
    if registry_id not in enabled:
        enabled.append(registry_id)
    payload["enabled_mods"] = enabled
    load_file.write_text(json.dumps(payload), encoding="utf-8", newline="\n")

    print(f"\n{display_name} is enabled.")
    print(f"  thumbnail: {thumbnail}")
    print(f"  {load_file.name}: {payload['enabled_mods']}")
    print("\nReopen the launcher and press Play.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
