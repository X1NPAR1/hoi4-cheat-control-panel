"""Emits the research effects and scripted localisation from the technology catalogue."""

from __future__ import annotations

from . import status
from .emit import BANNER, Writer, _dlc_limit
from .technology import Technology, group_by_folder

PAGE_SIZE = 16


def _folder_router(writer: Writer, folders: list[str], prefix: str) -> None:
    for position, name in enumerate(folders):
        keyword = "if" if position == 0 else "else_if"
        writer.open(keyword)
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_research_folder = {position + 1} }}")
        writer.close()
        writer.line(f"{prefix}_{name} = yes")
        writer.close()


def emit_research_effects(catalogue: list[Technology], version: str) -> str:
    grouped = group_by_folder(catalogue)
    folders = list(grouped)
    index_of = {item.key: index for index, item in enumerate(catalogue)}

    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    for position, name in enumerate(folders, start=1):
        pages = max(1, -(-len(grouped[name]) // PAGE_SIZE))
        writer.open(f"CCP_research_select_{name}")
        writer.line(f"set_variable = {{ ccp_research_folder = {position} }}")
        writer.line("set_variable = { ccp_research_page = 0 }")
        writer.line(f"set_variable = {{ ccp_research_pages_last = {pages - 1} }}")
        writer.line("set_variable = { ccp_research_selected = -1 }")
        writer.line("CCP_research_load_page = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_research_load_page")
    writer.line("clear_array = ccp_research_page_items")
    writer.line("set_variable = { ccp_research_page_shown = ccp_research_page }")
    writer.line("add_to_variable = { ccp_research_page_shown = 1 }")
    writer.line("set_variable = { ccp_research_pages_shown = ccp_research_pages_last }")
    writer.line("add_to_variable = { ccp_research_pages_shown = 1 }")
    _folder_router(writer, folders, "CCP_research_load")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        pages = max(1, -(-len(items) // PAGE_SIZE))
        writer.open(f"CCP_research_load_{name}")
        for page in range(pages):
            keyword = "if" if page == 0 else "else_if"
            writer.open(keyword)
            writer.open("limit")
            writer.line(f"check_variable = {{ ccp_research_page = {page} }}")
            writer.close()
            for item in items[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]:
                _dlc_limit(
                    writer,
                    item.dlc,
                    lambda item=item: writer.line(
                        "add_to_array = { array = ccp_research_page_items "
                        f"value = {index_of[item.key]} }}"
                    ),
                )
            writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_research_next_page")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_research_page < ccp_research_pages_last }")
    writer.close()
    writer.line("add_to_variable = { ccp_research_page = 1 }")
    writer.line("CCP_research_load_page = yes")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_research_prev_page")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_research_page > 0 }")
    writer.close()
    writer.line("subtract_from_variable = { ccp_research_page = 1 }")
    writer.line("CCP_research_load_page = yes")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_research_grant")
    writer.line(f"set_variable = {{ ccp_status = {status.SELECTION_FAILED} }}")
    _folder_router(writer, folders, "CCP_research_grant")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        writer.open(f"CCP_research_grant_{name}")
        for position, item in enumerate(items):
            keyword = "if" if position == 0 else "else_if"
            writer.open(keyword)
            writer.open("limit")
            writer.line(f"check_variable = {{ ccp_research_selected = {index_of[item.key]} }}")
            writer.close()
            writer.line("custom_effect_tooltip = CCP_RESEARCH_GRANT_TOOLTIP")
            writer.open("hidden_effect")
            writer.line(f"set_technology = {{ {item.key} = 1 popup = no }}")
            writer.line(f"set_variable = {{ ccp_status = {status.TECH_GRANTED} }}")
            writer.close()
            writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_research_grant_folder")
    _folder_router(writer, folders, "CCP_research_all")
    writer.line(f"set_variable = {{ ccp_status = {status.FOLDER_RESEARCHED} }}")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, items in grouped.items():
        writer.open(f"CCP_research_all_{name}")
        by_dlc: dict[str | None, list[Technology]] = {}
        for item in items:
            by_dlc.setdefault(item.dlc, []).append(item)
        for dlc, entries in by_dlc.items():
            _dlc_limit(
                writer,
                dlc,
                lambda entries=entries: _set_technologies(writer, entries),
            )
        writer.close()
        writer.blank()

    return writer.text()


def _set_technologies(writer: Writer, entries: list[Technology]) -> None:
    writer.open("set_technology")
    for item in entries:
        writer.line(f"{item.key} = 1")
    writer.line("popup = no")
    writer.close()


def emit_research_localisation(catalogue: list[Technology], version: str) -> str:
    writer = Writer()
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()

    for name, variable in (
        ("CCP_GetTechnologyName", "v"),
        ("CCP_GetTechnologySelectedName", "ccp_research_selected"),
    ):
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
        writer.line("localization_key = CCP_RESEARCH_UNKNOWN")
        writer.close()
        writer.close()
        writer.blank()

    folders = list(group_by_folder(catalogue))
    writer.open("defined_text")
    writer.line("name = CCP_GetResearchFolderName")
    for position, name in enumerate(folders, start=1):
        writer.open("text")
        writer.open("trigger")
        writer.line(f"check_variable = {{ ccp_research_folder = {position} }}")
        writer.close()
        writer.line(f"localization_key = {name}")
        writer.close()
    writer.open("text")
    writer.line("localization_key = CCP_RESEARCH_UNKNOWN")
    writer.close()
    writer.close()

    return writer.text()
