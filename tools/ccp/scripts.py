"""Emits the scripted GUI, the panel effects and the scripted localisation.

Everything here is derived from the same registries the interface is built from,
so a navigation button, its destination, its heading and its localisation key
cannot disagree.
"""

from __future__ import annotations

from .emit import BANNER, Writer
from .interface import NAV_STEP, NAV_TOP, PAD_SECTIONS, pad_widgets, section_containers
from .actions import ALL as COUNTRY_ACTIONS
from .countries import ACTIONS, PAGE_SIZE as COUNTRY_PAGE_SIZE

# The permissive half of the diplomacy rules the engine exposes to script. This is
# what the console's allowdiplo is used for; the console switch itself is out of
# reach, but these rules are the restrictions it lifts.
DIPLO_RULES = [
    "can_create_factions",
    "can_join_factions",
    "can_declare_war_on_same_ideology",
    "can_guarantee_other_ideologies",
    "can_puppet",
    "can_send_volunteers",
    "can_boost_other_ideologies",
    "can_access_market",
    "can_create_collaboration_government",
]
from .states import ACTIONS as STATE_ACTIONS, PAGE_SIZE as STATE_PAGE_SIZE
from .resources import AMOUNT_MAX, RESOURCES
from .sections import HOTKEYS, SECTIONS, section_id as section_index

from . import status

STATUS_IDLE = status.IDLE
STATUS_HOTKEY_CHANGED = status.HOTKEY_CHANGED
STATUS_CONFIRM_ON = status.CONFIRM_ON
STATUS_CONFIRM_OFF = status.CONFIRM_OFF
STATUS_GRANTED = status.RESOURCE_GRANTED

RESOURCE_ID = {resource.slug: index for index, resource in enumerate(RESOURCES, start=1)}

SETTINGS_VERSION = 2
DEFAULT_HOTKEY = 1


def _banner(writer: Writer, version: str) -> None:
    writer.line(BANNER.format(version=version).rstrip())
    writer.blank()


OVERFLOW_CEILING = 1_000_000_000


def _grant_body(writer: Writer, resource, apply) -> None:
    """Apply a grant, refusing it when the counter is about to wrap.

    Manpower is stored in a 32-bit counter. Pushing past its range makes the value
    go negative, which is worse than declining the grant and saying so.
    """
    if resource.slug != "manpower":
        apply()
        return

    writer.open("if")
    writer.open("limit")
    writer.line(f"check_variable = {{ manpower < {OVERFLOW_CEILING} }}")
    writer.close()
    apply()
    writer.close()
    writer.open("else")
    writer.line(f"set_variable = {{ ccp_status = {status.OVERFLOW_BLOCKED} }}")
    writer.close()


def emit_core_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    writer.open("CCP_ensure_settings")
    writer.line("set_variable = { ccp_player = THIS }")
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
    writer.line("set_variable = { ccp_target_country = THIS }")
    writer.line("set_variable = { ccp_diplo_rules = 0 }")
    writer.line("set_variable = { ccp_ai_goodwill = 0 }")
    writer.line("set_variable = { ccp_equipment_category = 1 }")
    writer.line("set_variable = { ccp_equipment_page = 0 }")
    writer.line("set_variable = { ccp_equipment_pages_last = 0 }")
    writer.line("set_variable = { ccp_equipment_selected = -1 }")
    writer.line("set_variable = { ccp_research_folder = 1 }")
    writer.line("set_variable = { ccp_research_page = 0 }")
    writer.line("set_variable = { ccp_research_pages_last = 0 }")
    writer.line("set_variable = { ccp_research_selected = -1 }")
    writer.line("set_variable = { ccp_country_page = 0 }")
    writer.line("set_variable = { ccp_country_pages_last = 0 }")
    writer.line("set_variable = { ccp_pending_action = 0 }")
    writer.line("set_variable = { ccp_modal_open = 0 }")
    writer.line("set_variable = { ccp_state_page = 0 }")
    writer.line("set_variable = { ccp_state_pages_last = 0 }")
    writer.line("set_variable = { ccp_state_picker_on = 0 }")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_mark_dirty")
    writer.line("add_to_variable = { ccp_ui_revision = 1 }")
    writer.close()
    writer.blank()

    writer.open("CCP_open_panel")
    writer.line("CCP_ensure_settings = yes")
    writer.line("set_variable = { ccp_player = THIS }")
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
        if section.slug == "equipment":
            writer.line("CCP_equipment_load_page = yes")
        if section.slug == "research":
            writer.line("CCP_research_load_page = yes")
        if section.slug == "country":
            writer.line("CCP_country_rebuild = yes")
        if section.slug == "states":
            writer.line("CCP_state_rebuild = yes")
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

            def apply(resource=resource, amount=amount) -> None:
                writer.line(f"{resource.effect} = {amount}")
                writer.line(f"set_variable = {{ ccp_status = {STATUS_GRANTED} }}")
                writer.line(
                    f"set_variable = {{ ccp_granted_resource = {RESOURCE_ID[resource.slug]} }}"
                )
                writer.line(f"set_variable = {{ ccp_granted_amount = {amount} }}")

            _grant_body(writer, resource, apply)
            writer.line("CCP_mark_dirty = yes")
            writer.close()
            writer.blank()

        writer.open(f"CCP_grant_{resource.slug}_custom")

        def apply_custom(resource=resource) -> None:
            writer.line("set_temp_variable = { ccp_grant = var:ccp_amount }")
            writer.open("clamp_temp_variable")
            writer.line("var = ccp_grant")
            writer.line("min = 0")
            writer.line(f"max = {resource.safe_max}")
            writer.close()
            writer.line(f"{resource.effect} = var:ccp_grant")
            writer.line(f"set_variable = {{ ccp_status = {STATUS_GRANTED} }}")
            writer.line(
                f"set_variable = {{ ccp_granted_resource = {RESOURCE_ID[resource.slug]} }}"
            )
            writer.line("set_variable = { ccp_granted_amount = var:ccp_grant }")

        _grant_body(writer, resource, apply_custom)
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_toggle_diplo_rules")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_diplo_rules = 1 }")
    writer.close()
    writer.line("set_variable = { ccp_diplo_rules = 0 }")
    writer.open("set_rule")
    for rule in DIPLO_RULES:
        writer.line(f"{rule} = no")
    writer.close()
    writer.line(f"set_variable = {{ ccp_status = {status.DIPLO_OFF} }}")
    writer.close()
    writer.open("else")
    writer.line("set_variable = { ccp_diplo_rules = 1 }")
    writer.open("set_rule")
    for rule in DIPLO_RULES:
        writer.line(f"{rule} = yes")
    writer.close()
    writer.line(f"set_variable = {{ ccp_status = {status.DIPLO_ON} }}")
    writer.close()
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_toggle_ai_goodwill")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_ai_goodwill = 1 }")
    writer.close()
    writer.line("set_variable = { ccp_ai_goodwill = 0 }")
    writer.open("every_country")
    writer.open("limit")
    writer.line("NOT = { tag = ROOT }")
    writer.close()
    writer.line("remove_opinion_modifier = { target = ROOT modifier = ccp_goodwill }")
    writer.close()
    writer.line(f"set_variable = {{ ccp_status = {status.GOODWILL_OFF} }}")
    writer.close()
    writer.open("else")
    writer.line("set_variable = { ccp_ai_goodwill = 1 }")
    writer.open("every_country")
    writer.open("limit")
    writer.line("NOT = { tag = ROOT }")
    writer.close()
    writer.line("add_opinion_modifier = { target = ROOT modifier = ccp_goodwill }")
    writer.line("add_ai_strategy = { type = befriend id = ROOT value = 200 }")
    writer.close()
    writer.line(f"set_variable = {{ ccp_status = {status.GOODWILL_ON} }}")
    writer.close()
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


def emit_country_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    writer.open("CCP_country_rebuild")
    writer.line("clear_array = ccp_country_all")
    writer.open("every_country")
    writer.open("limit")
    writer.line("exists = yes")
    writer.line("NOT = { tag = ROOT }")
    writer.close()
    writer.line("ROOT = { add_to_array = { array = ccp_country_all value = PREV } }")
    writer.close()
    writer.line("set_variable = { ccp_country_count = ccp_country_all^num }")
    writer.line("CCP_country_recount_pages = yes")
    writer.line("set_variable = { ccp_country_page = 0 }")
    writer.line("CCP_country_load_page = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_country_recount_pages")
    writer.line("set_variable = { ccp_country_pages_last = ccp_country_count }")
    writer.line("subtract_from_variable = { ccp_country_pages_last = 1 }")
    writer.line("clamp_variable = { var = ccp_country_pages_last min = 0 }")
    writer.line("set_temp_variable = { ccp_page_remainder = ccp_country_pages_last }")
    writer.line(f"modulo_temp_variable = {{ ccp_page_remainder = {COUNTRY_PAGE_SIZE} }}")
    writer.line("subtract_from_variable = { ccp_country_pages_last = var:ccp_page_remainder }")
    writer.line(f"divide_variable = {{ ccp_country_pages_last = {COUNTRY_PAGE_SIZE} }}")
    writer.close()
    writer.blank()

    writer.open("CCP_country_load_page")
    writer.line("clear_array = ccp_country_page_items")
    writer.line("set_variable = { ccp_country_page_shown = ccp_country_page }")
    writer.line("add_to_variable = { ccp_country_page_shown = 1 }")
    writer.line("set_variable = { ccp_country_pages_shown = ccp_country_pages_last }")
    writer.line("add_to_variable = { ccp_country_pages_shown = 1 }")
    writer.line("set_temp_variable = { ccp_page_first = var:ccp_country_page }")
    writer.line(f"multiply_temp_variable = {{ ccp_page_first = {COUNTRY_PAGE_SIZE} }}")
    writer.line("set_temp_variable = { ccp_page_last = var:ccp_page_first }")
    writer.line(f"add_to_temp_variable = {{ ccp_page_last = {COUNTRY_PAGE_SIZE - 1} }}")
    writer.open("for_loop_effect")
    writer.line("start = 0")
    writer.line("end = ccp_country_count")
    writer.line("value = ccp_slot")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_slot >= ccp_page_first }")
    writer.line("check_variable = { ccp_slot <= ccp_page_last }")
    writer.close()
    writer.open("add_to_array")
    writer.line("array = ccp_country_page_items")
    writer.line("value = ccp_country_all^ccp_slot")
    writer.close()
    writer.close()
    writer.close()
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, comparison, step in (
        ("next", "ccp_country_page < ccp_country_pages_last", "add_to_variable"),
        ("prev", "ccp_country_page > 0", "subtract_from_variable"),
    ):
        writer.open(f"CCP_country_{name}_page")
        writer.open("if")
        writer.open("limit")
        writer.line(f"check_variable = {{ {comparison} }}")
        writer.close()
        writer.line(f"{step} = {{ ccp_country_page = 1 }}")
        writer.line("CCP_country_load_page = yes")
        writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_country_target")
    writer.line("set_variable = { ccp_target_country = THIS }")
    writer.line(f"set_variable = {{ ccp_status = {status.TARGET_PICKED} }}")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for index, action in enumerate(ACTIONS, start=1):
        writer.open(f"CCP_country_request_{action.slug}")
        writer.line(f"set_variable = {{ ccp_pending_action = {index} }}")
        writer.line("set_variable = { ccp_pending_country = THIS }")
        if action.destructive:
            writer.open("if")
            writer.open("limit")
            writer.line("check_variable = { ccp_confirm_destructive = 1 }")
            writer.close()
            writer.line("set_variable = { ccp_modal_open = 1 }")
            writer.line("CCP_mark_dirty = yes")
            writer.close()
            writer.open("else")
            writer.line("CCP_country_apply = yes")
            writer.close()
        else:
            writer.line("CCP_country_apply = yes")
        writer.close()
        writer.blank()

    writer.open("CCP_country_cancel")
    writer.line("set_variable = { ccp_modal_open = 0 }")
    writer.line("set_variable = { ccp_pending_action = 0 }")
    writer.line(f"set_variable = {{ ccp_status = {status.ACTION_CANCELLED} }}")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_country_apply")
    writer.open("var:ccp_player")
    for index, action in enumerate(ACTIONS, start=1):
        writer.open("if" if index == 1 else "else_if")
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_pending_action = {index} }}")
        writer.close()
        for line in action.body:
            writer.line(line)
        writer.close()
    writer.close()
    writer.line(f"set_variable = {{ ccp_status = {status.COUNTRY_ACTION} }}")
    writer.line("set_variable = { ccp_modal_open = 0 }")
    writer.line("CCP_country_rebuild = yes")
    writer.close()

    return writer.text()


def emit_state_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    writer.open("CCP_state_rebuild")
    writer.line("clear_array = ccp_state_all")
    writer.open("every_state")
    writer.line("ROOT = { add_to_array = { array = ccp_state_all value = PREV } }")
    writer.close()
    writer.line("set_variable = { ccp_state_count = ccp_state_all^num }")
    writer.line("CCP_state_recount_pages = yes")
    writer.line("set_variable = { ccp_state_page = 0 }")
    writer.line("CCP_state_load_page = yes")
    writer.close()
    writer.blank()

    writer.open("CCP_state_recount_pages")
    writer.line("set_variable = { ccp_state_pages_last = ccp_state_count }")
    writer.line("subtract_from_variable = { ccp_state_pages_last = 1 }")
    writer.line("clamp_variable = { var = ccp_state_pages_last min = 0 }")
    writer.line("set_temp_variable = { ccp_page_remainder = ccp_state_pages_last }")
    writer.line(f"modulo_temp_variable = {{ ccp_page_remainder = {STATE_PAGE_SIZE} }}")
    writer.line("subtract_from_variable = { ccp_state_pages_last = var:ccp_page_remainder }")
    writer.line(f"divide_variable = {{ ccp_state_pages_last = {STATE_PAGE_SIZE} }}")
    writer.close()
    writer.blank()

    writer.open("CCP_state_load_page")
    writer.line("clear_array = ccp_state_page_items")
    writer.line("set_variable = { ccp_state_page_shown = ccp_state_page }")
    writer.line("add_to_variable = { ccp_state_page_shown = 1 }")
    writer.line("set_variable = { ccp_state_pages_shown = ccp_state_pages_last }")
    writer.line("add_to_variable = { ccp_state_pages_shown = 1 }")
    writer.line("set_temp_variable = { ccp_page_first = var:ccp_state_page }")
    writer.line(f"multiply_temp_variable = {{ ccp_page_first = {STATE_PAGE_SIZE} }}")
    writer.line("set_temp_variable = { ccp_page_last = var:ccp_page_first }")
    writer.line(f"add_to_temp_variable = {{ ccp_page_last = {STATE_PAGE_SIZE - 1} }}")
    writer.open("for_loop_effect")
    writer.line("start = 0")
    writer.line("end = ccp_state_count")
    writer.line("value = ccp_slot")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_slot >= ccp_page_first }")
    writer.line("check_variable = { ccp_slot <= ccp_page_last }")
    writer.close()
    writer.open("add_to_array")
    writer.line("array = ccp_state_page_items")
    writer.line("value = ccp_state_all^ccp_slot")
    writer.close()
    writer.close()
    writer.close()
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for name, comparison, step in (
        ("next", "ccp_state_page < ccp_state_pages_last", "add_to_variable"),
        ("prev", "ccp_state_page > 0", "subtract_from_variable"),
    ):
        writer.open(f"CCP_state_{name}_page")
        writer.open("if")
        writer.open("limit")
        writer.line(f"check_variable = {{ {comparison} }}")
        writer.close()
        writer.line(f"{step} = {{ ccp_state_page = 1 }}")
        writer.line("CCP_state_load_page = yes")
        writer.close()
        writer.close()
        writer.blank()

    for action in STATE_ACTIONS:
        writer.open(f"CCP_state_{action.slug}")
        writer.line("set_variable = { ccp_state = THIS }")
        writer.open(action.actor)
        writer.open("var:ccp_state")
        for line in action.body:
            writer.line(line)
        writer.close()
        writer.close()
        code = status.STATE_GIVEN if action.slug == "give" else status.STATE_ACTION
        writer.line(f"set_variable = {{ ccp_status = {code} }}")
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    return writer.text()


def emit_action_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    for action in COUNTRY_ACTIONS:
        writer.open(f"CCP_action_{action.slug}")
        for line in action.body:
            writer.line(line)
        writer.line(f"set_variable = {{ ccp_status = {status.NATION_ACTION} }}")
        writer.line(f"set_variable = {{ ccp_last_action = {COUNTRY_ACTIONS.index(action) + 1} }}")
        writer.line("CCP_history_record = yes")
        writer.line("CCP_mark_dirty = yes")
        writer.close()
        writer.blank()

    return writer.text()


HISTORY_LENGTH = 10


def emit_history_effects(version: str) -> str:
    writer = Writer()
    _banner(writer, version)

    writer.open("CCP_history_record")
    writer.line("add_to_array = { array = ccp_history value = var:ccp_last_action }")
    writer.open("if")
    writer.open("limit")
    writer.line(f"check_variable = {{ ccp_history^num > {HISTORY_LENGTH} }}")
    writer.close()
    writer.line("remove_from_array = { array = ccp_history index = 0 }")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("CCP_history_clear")
    writer.line("clear_array = ccp_history")
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.blank()

    for slot in range(HISTORY_LENGTH):
        writer.open(f"CCP_history_repeat_{slot + 1}")
        writer.open("if")
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_history^num > {slot} }}")
        writer.close()
        writer.line(f"set_variable = {{ ccp_last_action = ccp_history^{slot} }}")
        writer.line("CCP_action_replay = yes")
        writer.close()
        writer.close()
        writer.blank()

    writer.open("CCP_action_replay")
    for index, action in enumerate(COUNTRY_ACTIONS, start=1):
        writer.open("if" if index == 1 else "else_if")
        writer.open("limit")
        writer.line(f"check_variable = {{ ccp_last_action = {index} }}")
        writer.close()
        writer.line(f"CCP_action_{action.slug} = yes")
        writer.close()
    writer.close()

    return writer.text()


def emit_scripted_gui(version: str, categories: list[str], folders: list[str]) -> str:
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

    writer.open("ccp_state_picker")
    writer.line("context_type = selected_state_context")
    writer.line('window_name = "ccp_state_picker_window"')
    writer.blank()
    writer.open("visible")
    writer.line("check_variable = { ccp_state_picker_on = 1 }")
    writer.close()
    writer.blank()
    writer.open("effects")
    for action in STATE_ACTIONS:
        writer.open(f"ccp_picker_{action.slug}_click")
        writer.line(f"CCP_state_{action.slug} = yes")
        writer.close()
    writer.close()
    writer.close()
    writer.blank()

    writer.open("ccp_modal")
    writer.line("context_type = player_context")
    writer.line('window_name = "ccp_modal_window"')
    writer.blank()
    writer.open("visible")
    writer.line("check_variable = { ccp_modal_open = 1 }")
    writer.close()
    writer.blank()
    writer.line("dirty = ccp_ui_revision")
    writer.blank()
    writer.open("effects")
    writer.open("ccp_modal_cancel_click")
    writer.line("CCP_country_cancel = yes")
    writer.close()
    writer.open("ccp_modal_confirm_click")
    writer.line("CCP_country_apply = yes")
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
    writer.open("ccp_diplo_rules_toggle_click")
    writer.line("CCP_toggle_diplo_rules = yes")
    writer.close()
    writer.open("ccp_ai_goodwill_toggle_click")
    writer.line("CCP_toggle_ai_goodwill = yes")
    writer.close()
    for index, name in enumerate(categories, start=1):
        writer.open(f"ccp_equipment_category_{index}_click")
        writer.line(f"CCP_equipment_select_{name} = yes")
        writer.close()
    writer.open("ccp_equipment_prev_click")
    writer.line("CCP_equipment_prev_page = yes")
    writer.close()
    writer.open("ccp_equipment_next_click")
    writer.line("CCP_equipment_next_page = yes")
    writer.close()
    writer.open("ccp_equipment_entry_add_click")
    writer.line("set_variable = { ccp_equipment_selected = var:v }")
    writer.line("CCP_equipment_grant = yes")
    writer.close()
    writer.open("ccp_equipment_entry_latest_click")
    writer.line("set_variable = { ccp_equipment_selected = var:v }")
    writer.line("CCP_equipment_grant_latest = yes")
    writer.close()
    writer.open("ccp_equipment_all_click")
    writer.line("CCP_equipment_grant_category = yes")
    writer.close()
    for index, name in enumerate(folders, start=1):
        writer.open(f"ccp_research_category_{index}_click")
        writer.line(f"CCP_research_select_{name} = yes")
        writer.close()
    writer.open("ccp_research_prev_click")
    writer.line("CCP_research_prev_page = yes")
    writer.close()
    writer.open("ccp_research_next_click")
    writer.line("CCP_research_next_page = yes")
    writer.close()
    writer.open("ccp_research_all_click")
    writer.line("CCP_research_grant_folder = yes")
    writer.close()
    writer.open("ccp_research_everything_click")
    writer.line("CCP_research_grant_everything = yes")
    writer.close()
    writer.open("ccp_country_entry_target_click")
    writer.line("CCP_country_target = yes")
    writer.close()
    writer.open("ccp_research_entry_grant_click")
    writer.line("set_variable = { ccp_research_selected = var:v }")
    writer.line("CCP_research_grant = yes")
    writer.close()
    writer.open("ccp_country_prev_click")
    writer.line("CCP_country_prev_page = yes")
    writer.close()
    writer.open("ccp_country_next_click")
    writer.line("CCP_country_next_page = yes")
    writer.close()
    for action in ACTIONS:
        writer.open(f"ccp_country_entry_{action.slug}_click")
        writer.line(f"CCP_country_request_{action.slug} = yes")
        writer.close()
    writer.open("ccp_state_picker_toggle_click")
    writer.open("if")
    writer.open("limit")
    writer.line("check_variable = { ccp_state_picker_on = 1 }")
    writer.close()
    writer.line("set_variable = { ccp_state_picker_on = 0 }")
    writer.close()
    writer.open("else")
    writer.line("set_variable = { ccp_state_picker_on = 1 }")
    writer.close()
    writer.line("CCP_mark_dirty = yes")
    writer.close()
    writer.open("ccp_state_prev_click")
    writer.line("CCP_state_prev_page = yes")
    writer.close()
    writer.open("ccp_state_next_click")
    writer.line("CCP_state_next_page = yes")
    writer.close()
    for action in STATE_ACTIONS:
        writer.open(f"ccp_state_entry_{action.slug}_click")
        writer.line(f"CCP_state_{action.slug} = yes")
        writer.close()
    for action in COUNTRY_ACTIONS:
        writer.open(f"ccp_action_{action.slug}_run_click")
        writer.line(f"CCP_action_{action.slug} = yes")
        writer.close()
    writer.open("ccp_history_clear_click")
    writer.line("CCP_history_clear = yes")
    writer.close()
    for slot in range(HISTORY_LENGTH):
        writer.open(f"ccp_history_repeat_{slot + 1}_click")
        writer.line(f"CCP_history_repeat_{slot + 1} = yes")
        writer.close()
    writer.close()
    writer.blank()

    writer.open("triggers")

    # In Ironman the panel opens on the dashboard and goes no further: the notice
    # is the only thing shown, and every navigation button is disabled.
    for index in range(1, len(SECTIONS) + 1):
        writer.open(f"ccp_nav_{index}_click_enabled")
        writer.line("NOT = { is_ironman = yes }")
        writer.close()
    for widget in ("ccp_ironman_plate", "ccp_ironman_notice"):
        writer.open(f"{widget}_visible")
        writer.line("is_ironman = yes")
        writer.line(f"check_variable = {{ ccp_section = {section_index('dashboard')} }}")
        writer.line("check_variable = { ccp_panel_open = 1 }")
        writer.close()

    containers = section_containers(categories, folders)

    # A dynamic list draws its entries regardless of the grid box that holds them,
    # so the entry template's own widgets carry the section's visibility trigger too.
    from . import interface as ui

    entry_windows = {
        "equipment": (ui.equipment_entry_window(), False),
        "research": (ui.research_entry_window(), False),
        "country": (ui.country_entry_window(), True),
        "states": (ui.state_entry_window(), True),
    }
    dashboard = section_index("dashboard")
    for leaf in containers["dashboard"].leaves():
        if leaf.startswith("ccp_ironman"):
            continue
        writer.open(f"{leaf}_visible")
        writer.line(f"check_variable = {{ ccp_section = {dashboard} }}")
        writer.line("NOT = { is_ironman = yes }")
        writer.close()

    for slug, (window, _scoped) in entry_windows.items():
        index = section_index(slug)
        for leaf in window.leaves():
            writer.open(f"{leaf}_visible")
            writer.line(f"check_variable = {{ ccp_section = {index} }}")
            writer.line("check_variable = { ccp_panel_open = 1 }")
            writer.close()
    for index, section in enumerate(SECTIONS, start=1):
        for leaf in containers[section.slug].leaves():
            writer.open(f"{leaf}_visible")
            writer.line(f"check_variable = {{ ccp_section = {index} }}")
            writer.close()
    for index in range(1, len(HOTKEYS) + 1):
        writer.open(f"ccp_hotkey_choice_{index}_click_enabled")
        writer.line(f"NOT = {{ check_variable = {{ ccp_hotkey_id = {index} }} }}")
        writer.close()

    pad_sections = [section_index(slug) for slug in PAD_SECTIONS]
    for widget in pad_widgets():
        writer.open(f"{widget.name}_visible")
        writer.open("OR")
        for index in pad_sections:
            writer.line(f"check_variable = {{ ccp_section = {index} }}")
        writer.close()
        writer.close()

    writer.open("ccp_equipment_prev_click_enabled")
    writer.line("check_variable = { ccp_equipment_page > 0 }")
    writer.close()
    writer.open("ccp_equipment_next_click_enabled")
    writer.line("check_variable = { ccp_equipment_page < ccp_equipment_pages_last }")
    writer.close()
    writer.open("ccp_research_prev_click_enabled")
    writer.line("check_variable = { ccp_research_page > 0 }")
    writer.close()
    writer.open("ccp_research_next_click_enabled")
    writer.line("check_variable = { ccp_research_page < ccp_research_pages_last }")
    writer.close()
    writer.open("ccp_country_prev_click_enabled")
    writer.line("check_variable = { ccp_country_page > 0 }")
    writer.close()
    writer.open("ccp_country_next_click_enabled")
    writer.line("check_variable = { ccp_country_page < ccp_country_pages_last }")
    writer.close()
    for slot in range(HISTORY_LENGTH):
        for suffix in ("_plate", "_text"):
            writer.open(f"ccp_history_row_{slot + 1}{suffix}_visible")
            writer.line(f"check_variable = {{ ccp_history^num > {slot} }}")
            writer.line(f"check_variable = {{ ccp_section = {section_index('history')} }}")
            writer.close()
        writer.open(f"ccp_history_repeat_{slot + 1}_visible")
        writer.line(f"check_variable = {{ ccp_history^num > {slot} }}")
        writer.line(f"check_variable = {{ ccp_section = {section_index('history')} }}")
        writer.close()

    writer.open("ccp_state_prev_click_enabled")
    writer.line("check_variable = { ccp_state_page > 0 }")
    writer.close()
    writer.open("ccp_state_next_click_enabled")
    writer.line("check_variable = { ccp_state_page < ccp_state_pages_last }")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("properties")
    writer.open("ccp_nav_highlight")
    writer.line("y = ccp_nav_highlight_y")
    writer.close()
    writer.close()
    writer.blank()

    writer.open("dynamic_lists")
    writer.open("ccp_equipment_list")
    writer.line("array = ccp_equipment_page_items")
    writer.line('entry_container = "ccp_equipment_entry"')
    writer.close()
    writer.open("ccp_research_list")
    writer.line("array = ccp_research_page_items")
    writer.line('entry_container = "ccp_research_entry"')
    writer.close()
    writer.open("ccp_state_list")
    writer.line("array = ccp_state_page_items")
    writer.line("change_scope = yes")
    writer.line('entry_container = "ccp_state_entry"')
    writer.close()
    writer.open("ccp_country_list")
    writer.line("array = ccp_country_page_items")
    writer.line("change_scope = yes")
    writer.line('entry_container = "ccp_country_entry"')
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
            (f"check_variable = {{ ccp_status = {status.EQUIPMENT_GRANTED} }}", "CCP_STATUS_EQUIPMENT"),
            (f"check_variable = {{ ccp_status = {status.TECH_GRANTED} }}", "CCP_STATUS_TECH"),
            (f"check_variable = {{ ccp_status = {status.FOLDER_RESEARCHED} }}", "CCP_STATUS_FOLDER"),
            (f"check_variable = {{ ccp_status = {status.COUNTRY_ACTION} }}", "CCP_STATUS_COUNTRY"),
            (f"check_variable = {{ ccp_status = {status.ACTION_CANCELLED} }}", "CCP_STATUS_CANCELLED"),
            (f"check_variable = {{ ccp_status = {status.STATE_ACTION} }}", "CCP_STATUS_STATE"),
            (f"check_variable = {{ ccp_status = {status.NATION_ACTION} }}", "CCP_STATUS_ACTION"),
            (f"check_variable = {{ ccp_status = {status.OVERFLOW_BLOCKED} }}", "CCP_STATUS_OVERFLOW"),
            (f"check_variable = {{ ccp_status = {status.CATEGORY_GRANTED} }}", "CCP_STATUS_CATEGORY"),
            (f"check_variable = {{ ccp_status = {status.SELECTION_FAILED} }}", "CCP_STATUS_SELECTION"),
            (f"check_variable = {{ ccp_status = {status.GOODWILL_OFF} }}", "CCP_STATUS_GOODWILL_OFF"),
            (f"check_variable = {{ ccp_status = {status.GOODWILL_ON} }}", "CCP_STATUS_GOODWILL_ON"),
            (f"check_variable = {{ ccp_status = {status.DIPLO_OFF} }}", "CCP_STATUS_DIPLO_OFF"),
            (f"check_variable = {{ ccp_status = {status.DIPLO_ON} }}", "CCP_STATUS_DIPLO_ON"),
            (f"check_variable = {{ ccp_status = {status.STATE_GIVEN} }}", "CCP_STATUS_GIVEN"),
            (f"check_variable = {{ ccp_status = {status.EVERYTHING_RESEARCHED} }}", "CCP_STATUS_EVERYTHING"),
            (f"check_variable = {{ ccp_status = {status.TARGET_PICKED} }}", "CCP_STATUS_TARGET"),
        ],
        "CCP_STATUS_IDLE",
    )

    _defined_text(
        writer,
        "CCP_GetDiploRulesState",
        [("check_variable = { ccp_diplo_rules = 1 }", "CCP_DIPLO_ON")],
        "CCP_DIPLO_OFF",
    )

    _defined_text(
        writer,
        "CCP_GetGoodwillState",
        [("check_variable = { ccp_ai_goodwill = 1 }", "CCP_GOODWILL_ON")],
        "CCP_GOODWILL_OFF",
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

    for slot in range(HISTORY_LENGTH):
        _defined_text(
            writer,
            f"CCP_GetHistory{slot + 1}",
            [
                (f"check_variable = {{ ccp_history^{slot} = {index} }}", action.key)
                for index, action in enumerate(COUNTRY_ACTIONS, start=1)
            ],
            "CCP_HISTORY_EMPTY",
        )

    _defined_text(
        writer,
        "CCP_GetLastAction",
        [
            (f"check_variable = {{ ccp_last_action = {index} }}", action.key)
            for index, action in enumerate(COUNTRY_ACTIONS, start=1)
        ],
        COUNTRY_ACTIONS[0].key,
    )

    _defined_text(
        writer,
        "CCP_GetIronmanNotice",
        [("is_ironman = yes", "CCP_IRONMAN_ON")],
        "CCP_IRONMAN_OFF",
    )

    _defined_text(
        writer,
        "CCP_GetStatePickerState",
        [("check_variable = { ccp_state_picker_on = 1 }", "CCP_STATE_PICKER_ON")],
        "CCP_STATE_PICKER_OFF",
    )

    _defined_text(
        writer,
        "CCP_GetPendingAction",
        [
            (f"check_variable = {{ ccp_pending_action = {index} }}", action.key)
            for index, action in enumerate(ACTIONS, start=1)
        ],
        ACTIONS[0].key,
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
