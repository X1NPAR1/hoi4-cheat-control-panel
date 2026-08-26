"""Emits the scripted GUI, the panel effects and the scripted localisation.

Everything here is derived from the same registries the interface is built from,
so a navigation button, its destination, its heading and its localisation key
cannot disagree.
"""

from __future__ import annotations

from .emit import BANNER, Writer
from .interface import NAV_STEP, NAV_TOP
from .resources import AMOUNT_MAX, RESOURCES
from .sections import HOTKEYS, SECTIONS

STATUS_IDLE = 0
STATUS_HOTKEY_CHANGED = 1
STATUS_CONFIRM_ON = 2
STATUS_CONFIRM_OFF = 3
STATUS_GRANTED = 4

RESOURCE_ID = {resource.slug: index for index, resource in enumerate(RESOURCES, start=1)}

SETTINGS_VERSION = 2
DEFAULT_HOTKEY = 1


def _banner(writer: Writer, version: str) -> None:
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()


def emit_core_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    writer.open("CCP_ensure_settings")
    writer.open("if")
    writer.open("limit")
    writer.line(f"check_variable = {{ ccp_settings_version < {SETTINGS_VERSION} }}")
    writer.close()
    writer.line(f"set_variable = {{ ccp_settings_version = {SETTINGS_VERSION} }}")
    writer.line(f"set_variable = {{ ccp_hotkey_id = {DEFAULT_HOTKEY} }}")
    writer.line("set_variable = { ccp_confirm_destructive = 1 }")
    writer.line("set_variable = { ccp_section = 1 }")
    writer.line(f"set_variable = {{ ccp_nav_highlight_y = {NAV_TOP} }}")
    writer.line(f"set_variable = {{ ccp_status = {STATUS_IDLE} }}")
    writer.line("set_variable = { ccp_amount = 1000 }")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_mark_dirty")
    writer.line("add_to_variable = { ccp_ui_revision = 1 }")
    writer.close()
    writer.blank()

    writer.open("CCP_open_panel")
    writer.line("CCP_ensure_settings = yes")
    writer.line("set_variable = { ccp_panel_open = 1 }")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_close_panel")
    writer.line("set_variable = { ccp_panel_open = 0 }")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_toggle_panel")
    writer.line("CCP_ensure_settings = yes")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_panel_open = 1 }")
    writer.close()
    writer.line("CCP_close_panel = yes")
    writer.close()
    writer.open("else")
    writer.line("CCP_open_panel = yes")
    writer.close()
    writer.close()
    writer.blank()

    for index, section in enumerate(SECTIONS, start=1):
        writer.open(f"CCP_show_{section.slug}")
        writer.line(f"set_variable = {{ ccp_section = {index} }}")
        writer.line(
            f"set_variable = {{ ccp_nav_highlight_y = {NAV_TOP + (index - 1) * NAV_STEP} }}")
        writer.line(f"set_variable = {{ ccp_status = {STATUS_IDLE} }}")
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    for index in range(1, len(HOTKEYS) + 1):
        writer.open(f"CCP_set_hotkey_{index}")
        writer.line(f"set_variable = {{ ccp_hotkey_id = {index} }}")
        writer.line(f"set_variable = {{ ccp_status = {STATUS_HOTKEY_CHANGED} }}")
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_pad_clear")
    writer.line("set_variable = { ccp_amount = 0 }")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for digit in range(10):
        writer.open(f"CCP_pad_digit_{digit}")
        writer.open("if")
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_amount < {(AMOUNT_MAX - digit) // 10 + 1} }}")
        writer.close()
        writer.line("multiply_variable = { ccp_amount = 10 }")
        if digit:
            writer.line(f"add_to_variable = {{ ccp_amount = {digit} }}")
        writer.close()
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_pad_backspace")
    writer.line("set_temp_variable = { ccp_pad_last = var:ccp_amount }")
    writer.line("modulo_temp_variable = { ccp_pad_last = 10 }")
    writer.line("subtract_from_variable = { ccp_amount = var:ccp_pad_last }")
    writer.line("divide_variable = { ccp_amount = 10 }")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for resource in RESOURCES:
        for slot, amount in enumerate(resource.presets, start=1):
            writer.open(f"CCP_grant_{resource.slug}_{slot}")
            writer.line(f"{resource.effect} = {amount}")
            writer.line(f"set_variable = {{ ccp_status = {STATUS_GRANTED} }}")
            writer.line(f"set_variable = {{ ccp_granted_resource = {RESOURCE_ID[resource.slug]} }}")
            writer.line(f"set_variable = {{ ccp_granted_amount = {amount} }}")
            writer.line("CCP_mark_dirty = yes")
            writer.close()
            writer.blank()

        writer.open(f"CCP_grant_{resource.slug}_custom")
        writer.line("set_temp_variable = { ccp_grant = var:ccp_amount }")
        writer.open("clamp_temp_variable")
        writer.line("var = ccp_grant")
        writer.line("min = 0")
        writer.line(f"max = {resource.safe_max}")
        writer.close()
        writer.line(f"{resource.effect} = var:ccp_grant")
        writer.line(f"set_variable = {{ ccp_status = {STATUS_GRANTED} }}")
        writer.line(f"set_variable = {{ ccp_granted_resource = {RESOURCE_ID[resource.slug]} }}")
        writer.line("set_variable = { ccp_granted_amount = var:ccp_grant }")
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_toggle_confirmations")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_confirm_destructive = 1 }")
    writer.close()
    writer.line("set_variable = { ccp_confirm_destructive = 0 }")
    writer.line(f"set_variable = {{ ccp_status = {STATUS_CONFIRM_OFF} }}")
    writer.close()
    writer.open("else")
    writer.line("set_variable = { ccp_confirm_destructive = 1 }")
    writer.line(f"set_variable = {{ ccp_status = {STATUS_CONFIRM_ON} }}")
    writer.close()
    writer.line("CCP_mark_dirty = yes")
    writer.close()

    return writer.text()


def emit_scripted_gui(version: str) -> str:
    writer = Writer()
    _banner(writer, version)
    writer.open("scripted_gui")
    writer.blank()

    writer.open("ccp_launcher_button")
    writer.line("context_type = player_context")
    writer.line('window_name = "ccp_launcher_window"')
    writer.blank()
    writer.open("visible")
    writer.line("always = yes")
    writer.close()
    writer.blank()
    writer.open("effects")
    writer.open("ccp_launcher_click")
    writer.line("CCP_toggle_panel = yes")
    writer.close()
    writer.close()
    writer.close()
    writer.blank()

    writer.open("ccp_hotkey_listener")
    writer.line("context_type = player_context")
    writer.line('window_name = "ccp_hotkey_listener_window"')
    writer.blank()
    writer.open("visible")
    writer.line("always = yes")
    writer.close()
    writer.blank()
    writer.open("effects")
    for index in range(1, len(HOTKEYS) + 1):
        writer.open(f"ccp_hotkey_{index}_click")
        writer.line("CCP_ensure_settings = yes")
        writer.open("if")
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_hotkey_id = {index} }}")
        writer.close()
        writer.line("CCP_toggle_panel = yes")
        writer.close()
        writer.close()
    writer.close()
    writer.close()
    writer.blank()

    writer.open("ccp_main_panel")
    writer.line("context_type = player_context")
    writer.line('window_name = "ccp_main_window"')
    writer.blank()
    writer.open("visible")
    writer.line("check_variable = { ccp_panel_open = 1 }")
    writer.close()
    writer.blank()
    writer.line("dirty = ccp_ui_revision")
    writer.blank()

    writer.open("effects")
    writer.open("ccp_close_click")
    writer.line("CCP_close_panel = yes")
    writer.close()
    for index, section in enumerate(SECTIONS, start=1):
        writer.open(f"ccp_nav_{index}_click")
        writer.line(f"CCP_show_{section.slug} = yes")
        writer.close()
    for index in range(1, len(HOTKEYS) + 1):
        writer.open(f"ccp_hotkey_choice_{index}_click")
        writer.line(f"CCP_set_hotkey_{index} = yes")
        writer.close()
    for digit in range(10):
        writer.open(f"ccp_pad_{digit}_click")
        writer.line(f"CCP_pad_digit_{digit} = yes")
        writer.close()
    writer.open("ccp_pad_back_click")
    writer.line("CCP_pad_backspace = yes")
    writer.close()
    writer.open("ccp_pad_clear_click")
    writer.line("CCP_pad_clear = yes")
    writer.close()
    for resource in RESOURCES:
        for slot in range(1, len(resource.presets) + 1):
            writer.open(f"ccp_grant_{resource.slug}_{slot}_click")
            writer.line(f"CCP_grant_{resource.slug}_{slot} = yes")
            writer.close()
        writer.open(f"ccp_grant_{resource.slug}_custom_click")
        writer.line(f"CCP_grant_{resource.slug}_custom = yes")
        writer.close()
    writer.open("ccp_confirm_toggle_click")
    writer.line("CCP_toggle_confirmations = yes")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("triggers")
    for index, section in enumerate(SECTIONS, start=1):
        writer.open(f"{section.window}_visible")
        writer.line(f"check_variable = {{ ccp_section = {index} }}")
        writer.close()
    for index in range(1, len(HOTKEYS) + 1):
        writer.open(f"ccp_hotkey_choice_{index}_click_enabled")
        writer.line(f"NOT = {{ check_variable = {{ ccp_hotkey_id = {index} }} }}")
        writer.close()
    writer.close()
    writer.blank()

    writer.open("properties")
    writer.open("ccp_nav_highlight")
    writer.line("y = ccp_nav_highlight_y")
    writer.close()
    writer.close()

    writer.close()
    writer.close()
    return writer.text()


def _defined_text(writer: Writer, name: str, entries: list[tuple[str, str]], fallback: str) -> None:
    writer.open("defined_text")
    writer.line(f"name = {name}")
    for condition, key in entries:
        writer.open("text")
        writer.open("trigger")
        writer.line(condition)
        writer.close()
        writer.line(f"localization_key = {key}")
        writer.close()
    writer.open("text")
    writer.line(f"localization_key = {fallback}")
    writer.close()
    writer.close()
    writer.blank()


def emit_scripted_localisation(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    _defined_text(
        writer,
        "CCP_GetSectionName",
        [
            (f"check_variable = {{ ccp_section = {index} }}", section.key)
            for index, section in enumerate(SECTIONS, start=1)
        ],
        SECTIONS[0].key,
    )

    _defined_text(
        writer,
        "CCP_GetStatus",
        [
            (f"check_variable = {{ ccp_status = {STATUS_HOTKEY_CHANGED} }}", "CCP_STATUS_HOTKEY"),
            (f"check_variable = {{ ccp_status = {STATUS_CONFIRM_ON} }}", "CCP_STATUS_CONFIRM_ON"),
            (f"check_variable = {{ ccp_status = {STATUS_CONFIRM_OFF} }}", "CCP_STATUS_CONFIRM_OFF"),
            (f"check_variable = {{ ccp_status = {STATUS_GRANTED} }}", "CCP_STATUS_GRANTED"),
        ],
        "CCP_STATUS_IDLE",
    )

    _defined_text(
        writer,
        "CCP_GetConfirmState",
        [("check_variable = { ccp_confirm_destructive = 1 }", "CCP_CONFIRM_ON")],
        "CCP_CONFIRM_OFF",
    )

    _defined_text(
        writer,
        "CCP_GetGrantedResource",
        [
            (f"check_variable = {{ ccp_granted_resource = {RESOURCE_ID[resource.slug]} }}", resource.key)
            for resource in RESOURCES
        ],
        RESOURCES[0].key,
    )

    _defined_text(
        writer,
        "CCP_GetHotkeyName",
        [
            (f"check_variable = {{ ccp_hotkey_id = {index} }}", f"CCP_HOTKEY_{index}")
            for index in range(1, len(HOTKEYS) + 1)
        ],
        f"CCP_HOTKEY_{DEFAULT_HOTKEY}",
    )

    return writer.text()
