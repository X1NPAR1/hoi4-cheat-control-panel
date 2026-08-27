"""Which technology unlocks which equipment.

Technologies declare `enable_equipments`, so the mapping is real game data rather
than a guess. The panel uses it to disable the add button for equipment the
country cannot field yet and to say which technology is missing.
"""

from __future__ import annotations

import re
from pathlib import Path

from .paradox import parse_file

ENABLE = re.compile(r"enable_equipments\s*=\s*\{([^}]*)\}")


def equipment_unlocks(game_dir: Path) -> dict[str, str]:
    """`equipment key -> technology key`, using the earliest technology that grants it."""
    unlocks: dict[str, str] = {}
    base = game_dir / "common" / "technologies"
    if not base.is_dir():
        return unlocks

    for path in sorted(base.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        root = parse_file(path)
        for container in root.children:
            if container.key != "technologies":
                continue
            for entry in container.children:
                if not entry.key or not entry.children:
                    continue
                for child in entry.children:
                    if child.key != "enable_equipments":
                        continue
                    for value in child.get_all("enable_equipments") or [
                        item for grand in child.children for item in grand.values
                    ]:
                        unlocks.setdefault(value, entry.key)
    return unlocks
