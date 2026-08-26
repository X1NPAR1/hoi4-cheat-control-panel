"""Emits Clausewitz script for the Cheat Control Panel from a parsed catalogue."""

from __future__ import annotations

from . import status
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


PAGE_SIZE = 16


def emit_equipment_effects(catalogue: list[Equipment], version: str) -> str:
    grouped = group_by_category(catalogue)
    categories = list(grouped)
    category_id = {name: index + 1 for index, name in enumerate(categories)}
    index_of = {item.key: index for index, item in enumerate(catalogue)}
    latest = latest_per_archetype(catalogue)

    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    for name, items in grouped.items():
        pages = max(1, -(-len(items) // PAGE_SIZE))
        writer.open(f"CCP_equipment_select_{name}")
        writer.line(f"set_variable = {{ ccp_equipment_category = {category_id[name]} }}")
        writer.line("set_variable = { ccp_equipment_page = 0 }")
        writer.line(f"set_variable = {{ ccp_equipment_pages_last = {pages - 1} }}")
        writer.line("set_variable = { ccp_equipment_selected = -1 }")
        writer.line("CCP_equipment_load_page = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_equipment_load_page")
    writer.line("clear_array = ccp_equipment_page_items")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_load")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        pages = max(1, -(-len(items) // PAGE_SIZE))
        writer.open(f"CCP_equipment_load_{name}")
        for page in range(pages):
            keyword = "if" if page == 0 else "else_if"
            writer.open(keyword)
            writer.open("limit")
            writer.line(f"check_variable = {{ ccp_equipment_page = {page} }}")
            writer.close()
            for item in items[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]:
                _dlc_limit(
                    writer,
                    item.dlc,
                    lambda item=item: writer.line(
                        "add_to_array = { array = ccp_equipment_page_items "
                        f"value = {index_of[item.key]} }}"
                    ),
                )
            writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_equipment_next_page")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_equipment_page < ccp_equipment_pages_last }")
    writer.close()
    writer.line("add_to_variable = { ccp_equipment_page = 1 }")
    writer.line("CCP_equipment_load_page = yes")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_equipment_prev_page")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_equipment_page > 0 }")
    writer.close()
    writer.line("subtract_from_variable = { ccp_equipment_page = 1 }")
    writer.line("CCP_equipment_load_page = yes")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_equipment_grant")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_grant")
    writer.line(f"set_variable = {{ ccp_status = {status.EQUIPMENT_GRANTED} }}")
    writer.line("CCP_mark_dirty = yes")
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
                "amount = var:ccp_amount }"
            )
            writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_equipment_grant_latest")
    _emit_category_router(writer, categories, category_id, "CCP_equipment_grant_latest")
    writer.line(f"set_variable = {{ ccp_status = {status.EQUIPMENT_GRANTED} }}")
    writer.line("CCP_mark_dirty = yes")
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
                "amount = var:ccp_amount }"
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

    for name, variable in (
        ("CCP_GetEquipmentName", "ccp_entry"),
        ("CCP_GetEquipmentSelectedName", "ccp_equipment_selected"),
    ):
        _equipment_names(writer, catalogue, name, variable)

    return writer.text()


def _equipment_names(writer: Writer, catalogue, name: str, variable: str) -> None:
    writer.open("defined_text")
    writer.line(f"name = {name}")
    for index, item in enumerate(catalogue):
        writer.open("text")
        writer.open("trigger")
        writer.line(f"check_variable = {{ {variable} = {index} }}")
        writer.close()
        writer.line(f"localization_key = {item.key}")
        writer.close()
    writer.open("text")
    writer.line("localization_key = CCP_EQUIPMENT_UNKNOWN")
    writer.close()
    writer.close()
    writer.blank()


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


CATEGORY_LABELS: dict[str, tuple[str, str, str, str, str, str]] = {
    "infantry": ("Infantry Equipment", "Infanterieausrüstung", "Équipement d'infanterie", "Пехотное снаряжение", "Piyade Teçhizatı", "Infanterie-uitrusting"),
    "support": ("Support Equipment", "Unterstützungsausrüstung", "Équipement de soutien", "Снаряжение поддержки", "Destek Teçhizatı", "Ondersteuningsuitrusting"),
    "artillery": ("Artillery", "Artillerie", "Artillerie", "Артиллерия", "Topçu", "Artillerie"),
    "anti_tank": ("Anti-Tank", "Panzerabwehr", "Antichar", "Противотанковые", "Tanksavar", "Antitank"),
    "anti_air": ("Anti-Air", "Flugabwehr", "Antiaérien", "Зенитные", "Uçaksavar", "Luchtafweer"),
    "motorized": ("Motorized & Armored Cars", "Motorisiert & Panzerwagen", "Motorisé et automitrailleuses", "Мотопехота и бронеавтомобили", "Motorize ve Zırhlı Araçlar", "Gemotoriseerd & pantserwagens"),
    "mechanized": ("Mechanized", "Mechanisiert", "Mécanisé", "Механизированные", "Mekanize", "Gemechaniseerd"),
    "armored_car": ("Armored Cars", "Panzerwagen", "Automitrailleuses", "Бронеавтомобили", "Zırhlı Araçlar", "Pantserwagens"),
    "armor": ("Tanks", "Panzer", "Chars", "Танки", "Tanklar", "Tanks"),
    "railway_gun": ("Railway Guns", "Eisenbahngeschütze", "Canons ferroviaires", "Железнодорожные орудия", "Demiryolu Topları", "Spoorweggeschut"),
    "fighter": ("Fighters", "Jäger", "Chasseurs", "Истребители", "Avcı Uçakları", "Jagers"),
    "cas": ("Close Air Support", "Nahunterstützung", "Appui aérien rapproché", "Штурмовики", "Yakın Hava Desteği", "Luchtsteun"),
    "naval_bomber": ("Naval Bombers", "Marinebomber", "Bombardiers navals", "Морские бомбардировщики", "Deniz Bombardıman Uçakları", "Marinebommenwerpers"),
    "tactical_bomber": ("Tactical Bombers", "Taktische Bomber", "Bombardiers tactiques", "Тактические бомбардировщики", "Taktik Bombardıman Uçakları", "Tactische bommenwerpers"),
    "strategic_bomber": ("Strategic Bombers", "Strategische Bomber", "Bombardiers stratégiques", "Стратегические бомбардировщики", "Stratejik Bombardıman Uçakları", "Strategische bommenwerpers"),
    "transport_plane": ("Transport Planes", "Transportflugzeuge", "Avions de transport", "Транспортные самолёты", "Nakliye Uçakları", "Transportvliegtuigen"),
    "helicopter": ("Helicopters", "Hubschrauber", "Hélicoptères", "Вертолёты", "Helikopterler", "Helikopters"),
    "capital_ship": ("Capital Ships", "Grosskampfschiffe", "Navires de ligne", "Крупные корабли", "Ana Muharebe Gemileri", "Grote schepen"),
    "carrier": ("Carriers", "Flugzeugträger", "Porte-avions", "Авианосцы", "Uçak Gemileri", "Vliegdekschepen"),
    "screen_ship": ("Screen Ships", "Sicherungsschiffe", "Navires d'escorte", "Корабли охранения", "Refakat Gemileri", "Escorteschepen"),
    "submarine": ("Submarines", "U-Boote", "Sous-marins", "Подводные лодки", "Denizaltılar", "Onderzeeërs"),
    "convoy": ("Convoys & Support Ships", "Konvois & Versorgungsschiffe", "Convois et navires de soutien", "Конвои и суда снабжения", "Konvoylar ve Destek Gemileri", "Konvooien & steunschepen"),
    "train": ("Trains", "Züge", "Trains", "Поезда", "Trenler", "Treinen"),
    "missile": ("Missiles", "Raketen", "Missiles", "Ракеты", "Füzeler", "Raketten"),
    "special": ("Special Equipment", "Spezialausrüstung", "Équipement spécial", "Особое снаряжение", "Özel Teçhizat", "Speciale uitrusting"),
    "other": ("Other", "Sonstige", "Autre", "Прочее", "Diğer", "Overig"),
}

LANGUAGE_INDEX = {
    "english": 0,
    "german": 1,
    "french": 2,
    "russian": 3,
    "turkish": 4,
    "dutch": 5,
}


def emit_category_localisation(
    catalogue: list[Equipment], language: str, version: str
) -> str:
    """A localisation file naming every equipment category present in this install."""
    index = LANGUAGE_INDEX[language]
    label_language = "english" if language in ("turkish", "dutch") else language
    lines = [
        f"l_{label_language}:",
        f"# GENERATED FILE - DO NOT EDIT (tools/generate_data.py, game {version})",
    ]
    for name in group_by_category(catalogue):
        fallback = (name.replace("_", " ").title(),) * 2
        label = CATEGORY_LABELS.get(name, fallback)[index]
        lines.append(f' CCP_EQCAT_{name.upper()}:0 "{label}"')
    return "\n".join(lines) + "\n"
