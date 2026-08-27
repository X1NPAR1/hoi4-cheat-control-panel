"""Builds the Cheat Control Panel equipment catalogue from the installed game files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .gameloc import english_keys
from .paradox import Node, parse_file

CATEGORY_ORDER = [
    "infantry",
    "support",
    "artillery",
    "anti_tank",
    "anti_air",
    "motorized",
    "mechanized",
    "armored_car",
    "armor",
    "railway_gun",
    "fighter",
    "cas",
    "naval_bomber",
    "tactical_bomber",
    "strategic_bomber",
    "transport_plane",
    "helicopter",
    "capital_ship",
    "carrier",
    "screen_ship",
    "submarine",
    "convoy",
    "train",
    "missile",
    "special",
    "other",
]

_TYPE_TO_CATEGORY = {
    "infantry": "infantry",
    "support": "support",
    "artillery": "artillery",
    "anti_tank": "anti_tank",
    "anti_air": "anti_air",
    "rocket": "artillery",
    "motorized": "motorized",
    "mechanized": "mechanized",
    "armored_car": "armored_car",
    "armor": "armor",
    "railway_gun": "railway_gun",
    "fighter": "fighter",
    "interceptor": "fighter",
    "heavy_fighter": "fighter",
    "cas": "cas",
    "naval_bomber": "naval_bomber",
    "tactical_bomber": "tactical_bomber",
    "strategic_bomber": "strategic_bomber",
    "transport_plane": "transport_plane",
    "suicide": "special",
    "scout_plane": "special",
    "helicopter": "helicopter",
    "maritime_patrol_plane": "special",
    "capital_ship": "capital_ship",
    "carrier": "carrier",
    "screen_ship": "screen_ship",
    "submarine": "submarine",
    "support_ship": "screen_ship",
    "convoy": "convoy",
    "train": "train",
    "missile": "missile",
    "sam_missile": "missile",
    "flame": "armor",
    "amphibious": "armor",
}

_INTERFACE_FALLBACK = {
    "interface_category_land": "infantry",
    "interface_category_armor": "armor",
    "interface_category_air": "fighter",
    "interface_category_capital_ships": "capital_ship",
    "interface_category_screen_ships": "screen_ship",
    "interface_category_other_ships": "convoy",
}

DLC_BY_SOURCE_DIR = {
    "dlc018_together_for_victory": "Together for Victory",
    "dlc020_death_or_dishonor": "Death or Dishonor",
    "dlc022_waking_the_tiger": "Waking the Tiger",
    "dlc023_man_the_guns": "Man the Guns",
}


@dataclass
class Equipment:
    key: str
    archetype: str
    category: str
    year: int
    dlc: str | None = None
    types: list[str] = field(default_factory=list)


def _int_or(value: str | None, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


_SPECIFICITY = [
    "capital_ship",
    "carrier",
    "submarine",
    "screen_ship",
    "convoy",
    "train",
    "missile",
    "cas",
    "naval_bomber",
    "tactical_bomber",
    "strategic_bomber",
    "transport_plane",
    "helicopter",
    "fighter",
    "special",
    "railway_gun",
    "armor",
    "mechanized",
    "armored_car",
    "support",
    "anti_tank",
    "anti_air",
    "artillery",
    "motorized",
    "infantry",
]


def _category_for(types: list[str], interface_category: str | None) -> str:
    """An entry may declare several types; the most specific one names the category."""
    mapped = {_TYPE_TO_CATEGORY[token] for token in types if token in _TYPE_TO_CATEGORY}
    for candidate in _SPECIFICITY:
        if candidate in mapped:
            return candidate
    if mapped:
        return sorted(mapped, key=lambda name: CATEGORY_ORDER.index(name))[0]
    return _INTERFACE_FALLBACK.get(interface_category or "", "other")


def _equipment_files(game_dir: Path) -> list[tuple[Path, str | None]]:
    found: list[tuple[Path, str | None]] = []
    base = game_dir / "common" / "units" / "equipment"
    if base.is_dir():
        found += [(path, None) for path in sorted(base.glob("*.txt"))]

    for dlc_root in (game_dir / "integrated_dlc", game_dir / "dlc"):
        if not dlc_root.is_dir():
            continue
        for dlc_dir in sorted(dlc_root.iterdir()):
            dlc_name = DLC_BY_SOURCE_DIR.get(dlc_dir.name)
            sub = dlc_dir / "common" / "units" / "equipment"
            if sub.is_dir():
                found += [(path, dlc_name) for path in sorted(sub.glob("*.txt"))]
    return found


def _inherited(entries: dict[str, Node], key: str, field_name: str) -> str | None:
    """Walk the `archetype` chain until `field_name` is found."""
    seen: set[str] = set()
    while key and key in entries and key not in seen:
        seen.add(key)
        node = entries[key]
        value = node.get(field_name)
        if value is not None:
            return value
        key = node.get("archetype") or ""
    return None


def _inherited_list(entries: dict[str, Node], key: str, field_name: str) -> list[str]:
    seen: set[str] = set()
    while key and key in entries and key not in seen:
        seen.add(key)
        node = entries[key]
        values = node.get_all(field_name)
        if values:
            return values
        key = node.get("archetype") or ""
    return []


# add_equipment_to_stockpile refuses ships and railway guns outright: those are
# built as units, not held in a stockpile. Listing them would give the player a
# button the engine logs an error for and otherwise ignores.
UNSTOCKPILEABLE_TYPES = frozenset(
    {
        "capital_ship",
        "carrier",
        "screen_ship",
        "submarine",
        "support_ship",
        "railway_gun",
    }
)


def load_catalogue(game_dir: Path) -> list[Equipment]:
    """Every addable equipment variant, ordered by category then year then key."""
    entries: dict[str, Node] = {}
    raw: list[tuple[str, Node, str | None, str]] = []

    for path, dlc in _equipment_files(game_dir):
        root = parse_file(path)
        for container in root.children:
            if container.key not in ("equipments", "duplicate_archetypes"):
                continue
            for entry in container.children:
                if not entry.key or not entry.children:
                    continue
                raw.append((entry.key, entry, dlc, container.key))
                entries[entry.key] = entry

    referenced_as_archetype = {
        node.get("archetype") for _, node, _, _ in raw if node.get("archetype")
    }

    catalogue: list[Equipment] = []
    for key, node, dlc, container in raw:
        if node.get("is_archetype") == "yes" or key in referenced_as_archetype:
            continue
        # Everything under duplicate_archetypes is a designer archetype: a shape
        # the equipment designer derives variants from, never a stockpile item.
        if container == "duplicate_archetypes":
            continue

        archetype_key = node.get("archetype") or key
        types = _inherited_list(entries, key, "type")
        if UNSTOCKPILEABLE_TYPES.intersection(types):
            continue
        # A designer chassis is not a stockpile item; the equipment it names is.
        if node.get("derived_variant_name"):
            continue

        catalogue.append(
            Equipment(
                key=key,
                archetype=archetype_key,
                category=_category_for(
                    _inherited_list(entries, key, "type"),
                    _inherited(entries, key, "interface_category"),
                ),
                year=_int_or(_inherited(entries, key, "year"), 1936),
                dlc=dlc,
                types=_inherited_list(entries, key, "type"),
            )
        )

    named = english_keys(game_dir)
    catalogue = [item for item in catalogue if item.key in named]

    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    catalogue.sort(key=lambda item: (order.get(item.category, len(order)), item.year, item.key))
    return catalogue


def group_by_category(catalogue: list[Equipment]) -> dict[str, list[Equipment]]:
    grouped: dict[str, list[Equipment]] = {}
    for item in catalogue:
        grouped.setdefault(item.category, []).append(item)
    return {name: grouped[name] for name in CATEGORY_ORDER if name in grouped}


def latest_per_archetype(items: list[Equipment]) -> dict[str, Equipment]:
    latest: dict[str, Equipment] = {}
    for item in items:
        current = latest.get(item.archetype)
        if current is None or (item.year, item.key) >= (current.year, current.key):
            latest[item.archetype] = item
    return latest
