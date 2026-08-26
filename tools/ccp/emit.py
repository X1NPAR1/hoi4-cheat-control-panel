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


CATEGORY_LABELS = {
    "infantry": ("Infantry Equipment", "Piyade Teçhizatı"),
    "support": ("Support Equipment", "Destek Teçhizatı"),
    "artillery": ("Artillery", "Topçu"),
    "anti_tank": ("Anti-Tank", "Tanksavar"),
    "anti_air": ("Anti-Air", "Uçaksavar"),
    "motorized": ("Motorized & Armored Cars", "Motorize ve Zırhlı Araçlar"),
    "mechanized": ("Mechanized", "Mekanize"),
    "armored_car": ("Armored Cars", "Zırhlı Araçlar"),
    "armor": ("Tanks", "Tanklar"),
    "railway_gun": ("Railway Guns", "Demiryolu Topları"),
    "fighter": ("Fighters", "Avcı Uçakları"),
    "cas": ("Close Air Support", "Yakın Hava Desteği"),
    "naval_bomber": ("Naval Bombers", "Deniz Bombardıman Uçakları"),
    "tactical_bomber": ("Tactical Bombers", "Taktik Bombardıman Uçakları"),
    "strategic_bomber": ("Strategic Bombers", "Stratejik Bombardıman Uçakları"),
    "transport_plane": ("Transport Planes", "Nakliye Uçakları"),
    "helicopter": ("Helicopters", "Helikopterler"),
    "capital_ship": ("Capital Ships", "Ana Muharebe Gemileri"),
    "carrier": ("Carriers", "Uçak Gemileri"),
    "screen_ship": ("Screen Ships", "Refakat Gemileri"),
    "submarine": ("Submarines", "Denizaltılar"),
    "convoy": ("Convoys & Support Ships", "Konvoylar ve Destek Gemileri"),
    "train": ("Trains", "Trenler"),
    "missile": ("Missiles", "Füzeler"),
    "special": ("Special Equipment", "Özel Teçhizat"),
    "other": ("Other", "Diğer"),
}

LANGUAGE_INDEX = {"english": 0, "turkish": 1}


def emit_category_localisation(
    catalogue: list[Equipment], language: str, version: str
) -> str:
    """A localisation file naming every equipment category present in this install."""
    index = LANGUAGE_INDEX[language]
    lines = [
        f"l_{language}:",
        f"# GENERATED FILE - DO NOT EDIT (tools/generate_data.py, game {version})",
    ]
    for name in group_by_category(catalogue):
        fallback = (name.replace("_", " ").title(),) * 2
        label = CATEGORY_LABELS.get(name, fallback)[index]
        lines.append(f' CCP_EQCAT_{name.upper()}:0 "{label}"')
    return "\n".join(lines) + "\n"
