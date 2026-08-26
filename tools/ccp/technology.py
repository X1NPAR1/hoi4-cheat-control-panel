"""Builds the technology catalogue from the installed game files.

`set_technology` needs a literal token, so the list has to be resolved when the
mod is built rather than walked at runtime, the same way equipment is.
Technologies group by the research folder the game itself assigns them.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .gameloc import english_keys
from .paradox import Node, parse_file

FOLDER_ORDER = [
    "infantry_folder",
    "support_folder",
    "artillery_folder",
    "armor_folder",
    "land_doctrine_folder",
    "naval_folder",
    "naval_doctrine_folder",
    "air_techs_folder",
    "air_doctrine_folder",
    "electronics_folder",
    "industry_folder",
    "special_projects_folder",
]

DLC_BY_FILE = {
    "MTG_naval.txt": "Man the Guns",
    "MTG_naval_Support.txt": "Man the Guns",
    "NSB_armor.txt": "No Step Back",
    "bba_air_techs.txt": "By Blood Alone",
}


@dataclass
class Technology:
    key: str
    folder: str
    year: int
    dlc: str | None = None


def _folder_of(node: Node) -> str | None:
    for child in node.children:
        if child.key == "folder":
            name = child.get("name")
            if name:
                return name
    return None


def _year(node: Node) -> int:
    raw = node.get("start_year")
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return 1936


def load_catalogue(game_dir: Path) -> list[Technology]:
    """Every researchable technology, ordered by folder then year then key."""
    catalogue: list[Technology] = []
    seen: set[str] = set()

    base = game_dir / "common" / "technologies"
    if not base.is_dir():
        return catalogue

    for path in sorted(base.glob("*.txt")):
        dlc = DLC_BY_FILE.get(path.name)
        root = parse_file(path)
        for container in root.children:
            if container.key != "technologies":
                continue
            for entry in container.children:
                if not entry.key or not entry.children or entry.key.startswith("@"):
                    continue
                folder = _folder_of(entry)
                if folder is None or entry.key in seen:
                    continue
                seen.add(entry.key)
                catalogue.append(
                    Technology(key=entry.key, folder=folder, year=_year(entry), dlc=dlc)
                )

    named = english_keys(game_dir)
    catalogue = [item for item in catalogue if item.key in named]

    order = {name: index for index, name in enumerate(FOLDER_ORDER)}
    catalogue.sort(key=lambda item: (order.get(item.folder, len(order)), item.year, item.key))
    return catalogue


def group_by_folder(catalogue: list[Technology]) -> dict[str, list[Technology]]:
    grouped: dict[str, list[Technology]] = {}
    for item in catalogue:
        grouped.setdefault(item.folder, []).append(item)
    known = [name for name in FOLDER_ORDER if name in grouped]
    extra = sorted(name for name in grouped if name not in FOLDER_ORDER)
    return {name: grouped[name] for name in known + extra}
