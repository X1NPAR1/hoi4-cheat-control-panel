"""Emits Clausewitz script for the Cheat Control Panel from a parsed catalogue."""

from __future__ import annotations

from .equipment import Equipment, group_by_category, latest_per_archetype

BANNER = (
    "# GENERATED FILE - DO NOT EDIT\n"
    "# Produced by tools/generate_data.py from the installed game files.\n"
    "# Source game version: {version}\n"
)

INDENT = "\t"


class Writer:
    def __init__(self) -> None:
        self._lines: list[str] = []
        self._depth = 0

    def line(self, text: str = "") -> None:
        self._lines.append(f"{INDENT * self._depth}{text}" if text else "")

    def open(self, text: str) -> None:
        self.line(f"{text} = {{")
        self._depth += 1

    def close(self) -> None:
        self._depth -= 1
        self.line("}")

    def blank(self) -> None:
        self._lines.append("")

    def text(self) -> str:
        return "\n".join(self._lines).rstrip() + "\n"


def _dlc_limit(writer: Writer, dlc: str | None, body) -> None:
    if dlc is None:
        body()
        return
    writer.open("if")
    writer.open("limit")
    writer.line(f'has_dlc = "{dlc}"')
    writer.close()
    body()
    writer.close()


def emit_equipment_effects(catalogue: list[Equipment], version: str) -> str:
    grouped = group_by_category(catalogue)
    categories = list(grouped)
    category_id = {name: index + 1 for index, name in enumerate(categories)}
    index_of = {item.key: index for index, item in enumerate(catalogue)}
    latest = latest_per_archetype(catalogue)

    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    writer.open("CCP_equipment_load_list")
    writer.line("clear_array = ccp_equipment_list")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_load")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        writer.open(f"CCP_equipment_load_{name}")
        for item in items:
            _dlc_limit(
                writer,
                item.dlc,
                lambda item=item: writer.line(
                    f"add_to_array = {{ array = ccp_equipment_list value = {index_of[item.key]} }}"
                ),
            )
        writer.close()
        writer.blank()

    writer.open("CCP_equipment_grant")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_grant")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        writer.open(f"CCP_equipment_grant_{name}")
        for position, item in enumerate(items):
            keyword = "if" if position == 0 else "else_if"
            writer.open(keyword)
            writer.open("limit")
            writer.line(f"check_variable = {{ ccp_equipment_selected = {index_of[item.key]} }}")
            writer.close()
            writer.line(
                f"add_equipment_to_stockpile = {{ type = {item.key} "
                "amount = var:ccp_equipment_amount }"
            )
            writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_equipment_grant_latest")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_grant_latest")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        writer.open(f"CCP_equipment_grant_latest_{name}")
        for position, item in enumerate(items):
            keyword = "if" if position == 0 else "else_if"
            newest = latest[item.archetype]
            writer.open(keyword)
            writer.open("limit")
            writer.line(f"check_variable = {{ ccp_equipment_selected = {index_of[item.key]} }}")
            writer.close()
            writer.line(
                f"add_equipment_to_stockpile = {{ type = {newest.key} "
                "amount = var:ccp_equipment_amount }"
            )
            writer.close()
        writer.close()
        writer.blank()

    return writer.text()


def _emit_category_router(
    writer: Writer, categories: list[str], category_id: dict[str, int], prefix: str
) -> None:
    for position, name in enumerate(categories):
        keyword = "if" if position == 0 else "else_if"
        writer.open(keyword)
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_equipment_category = {category_id[name]} }}")
        writer.close()
        writer.line(f"{prefix}_{name} = yes")
        writer.close()


def emit_equipment_localisation(catalogue: list[Equipment], version: str) -> str:
    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    writer.open("defined_text")
    writer.line("name = CCP_GetEquipmentName")
    for index, item in enumerate(catalogue):
        writer.open("text")
        writer.open("trigger")
        writer.line(f"check_variable = {{ ccp_entry = {index} }}")
        writer.close()
        writer.line(f"localization_key = {item.key}")
        writer.close()
    writer.open("text")
    writer.line("localization_key = CCP_EQUIPMENT_UNKNOWN")
    writer.close()
    writer.close()

    return writer.text()


def emit_equipment_categories_localisation(
    catalogue: list[Equipment], version: str
) -> str:
    categories = list(group_by_category(catalogue))
    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    writer.open("defined_text")
    writer.line("name = CCP_GetEquipmentCategoryName")
    for index, name in enumerate(categories, start=1):
        writer.open("text")
        writer.open("trigger")
        writer.line(f"check_variable = {{ ccp_equipment_category = {index} }}")
        writer.close()
        writer.line(f"localization_key = CCP_EQCAT_{name.upper()}")
        writer.close()
    writer.open("text")
    writer.line("localization_key = CCP_EQUIPMENT_UNKNOWN")
    writer.close()
    writer.close()

    return writer.text()


def category_localisation_keys(catalogue: list[Equipment]) -> list[tuple[str, str]]:
    """`(key, english default)` pairs for every equipment category in the catalogue."""
    labels = {
        "infantry": "Infantry Equipment",
        "support": "Support Equipment",
        "artillery": "Artillery",
        "anti_tank": "Anti-Tank",
        "anti_air": "Anti-Air",
        "motorized": "Motorized & Armored Cars",
        "mechanized": "Mechanized",
        "armored_car": "Armored Cars",
        "armor": "Tanks",
        "railway_gun": "Railway Guns",
        "fighter": "Fighters",
        "cas": "Close Air Support",
        "naval_bomber": "Naval Bombers",
        "tactical_bomber": "Tactical Bombers",
        "strategic_bomber": "Strategic Bombers",
        "transport_plane": "Transport Planes",
        "helicopter": "Helicopters",
        "capital_ship": "Capital Ships",
        "carrier": "Carriers",
        "screen_ship": "Screen Ships",
        "submarine": "Submarines",
        "convoy": "Convoys & Support Ships",
        "train": "Trains",
        "missile": "Missiles",
        "special": "Special Equipment",
        "other": "Other",
    }
    return [
        (f"CCP_EQCAT_{name.upper()}", labels.get(name, name.replace("_", " ").title()))
        for name in group_by_category(catalogue)
    ]
