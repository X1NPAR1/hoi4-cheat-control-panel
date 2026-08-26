"""Builds the panel's windows from the design grid in `theme.py`."""

from __future__ import annotations

from . import theme as t
from .layout import Button, Container, Grid, Icon, Text, Widget
from .actions import BY_SECTION as ACTION_SECTIONS
from .countries import ACTIONS
from .states import ACTIONS as STATE_ACTIONS, PAGE_SIZE as STATE_PAGE_SIZE
from .sections import HOTKEYS, SECTIONS

CONTENT_X = t.SIDEBAR_WIDTH + 24
CONTENT_TOP = t.HEADER_HEIGHT + 20
HEADING_HEIGHT = 24
DIVIDER_Y = CONTENT_TOP + HEADING_HEIGHT + 6
BODY_TOP = DIVIDER_Y + 16

NAV_TOP = t.HEADER_HEIGHT + 36
NAV_STEP = t.SIDEBAR_ITEM_HEIGHT

CARD_WIDTH = 320
CARD_HEIGHT = 96
CARD_GAP = 16

FOOTER_TOP = t.PANEL_HEIGHT - t.FOOTER_HEIGHT


def _nav_y(index: int) -> int:
    return NAV_TOP + index * NAV_STEP


def _header() -> list[Widget]:
    return [
        Icon("ccp_body_plate", 0, t.HEADER_HEIGHT, sprite="GFX_ccp_panel_body"),
        Icon("ccp_header_plate", 0, 0, sprite="GFX_ccp_panel_header"),
        Icon("ccp_header_logo", 12, 8, sprite="GFX_ccp_logo"),
        Text("ccp_header_title", 64, 9, key="CCP_TITLE", width=520, height=24, font="hoi_20b"),
        Text("ccp_header_subtitle", 64, 32, key="CCP_SUBTITLE", width=640, height=18),
        Button(
            "ccp_close",
            -12 - t.BUTTON_WIDTH,
            13,
            key="CCP_BUTTON_CLOSE",
            tooltip="CCP_TOOLTIP_CLOSE",
            click_sound="click_close",
            orientation="upper_right",
        ),
    ]


def _sidebar() -> list[Widget]:
    widgets: list[Widget] = [
        Icon("ccp_sidebar_plate", 0, t.HEADER_HEIGHT, sprite="GFX_ccp_panel_sidebar"),
        Text(
            "ccp_sidebar_heading",
            16,
            t.HEADER_HEIGHT + 12,
            key="CCP_SIDEBAR_HEADING",
            width=t.SIDEBAR_WIDTH - 32,
            height=18,
        ),
        Icon("ccp_nav_highlight", 0, NAV_TOP, sprite="GFX_ccp_sidebar_item", frame=3),
    ]
    for index, section in enumerate(SECTIONS):
        widgets.append(
            Button(
                f"ccp_nav_{index + 1}",
                0,
                _nav_y(index),
                sprite="GFX_ccp_sidebar_item",
                key=section.key,
                tooltip=f"{section.key}_TOOLTIP",
            )
        )
    return widgets


def _footer() -> list[Widget]:
    return [
        Icon("ccp_footer_plate", 0, FOOTER_TOP, sprite="GFX_ccp_panel_footer"),
        Text(
            "ccp_footer_status",
            16,
            FOOTER_TOP + 8,
            key="CCP_GetStatus",
            width=760,
            height=18,
        ),
        Text(
            "ccp_footer_hint",
            -16 - 480,
            FOOTER_TOP + 8,
            key="CCP_FOOTER_HINT",
            width=480,
            height=18,
            align="right",
            orientation="upper_right",
        ),
    ]


def _content_shell() -> list[Widget]:
    return [
        Text(
            "ccp_content_heading",
            CONTENT_X,
            CONTENT_TOP,
            key="CCP_GetSectionName",
            width=t.CONTENT_WIDTH - 48,
            height=HEADING_HEIGHT,
            font="hoi_20b",
        ),
        Icon("ccp_content_divider", CONTENT_X, DIVIDER_Y, sprite="GFX_ccp_divider"),
    ]


def _stat_card(name: str, column: int, row: int, label: str, value: str, tooltip: str) -> Container:
    card = Container(
        f"ccp_card_{name}",
        CONTENT_X + column * (CARD_WIDTH + CARD_GAP),
        BODY_TOP + row * (CARD_HEIGHT + CARD_GAP),
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
    )
    return card.add(
        Icon(f"ccp_card_{name}_plate", 0, 0, sprite="GFX_ccp_card"),
        Text(
            f"ccp_card_{name}_label",
            16,
            14,
            key=label,
            width=CARD_WIDTH - 32,
            height=18,
            tooltip=tooltip,
        ),
        Text(
            f"ccp_card_{name}_value",
            16,
            40,
            key=value,
            width=CARD_WIDTH - 32,
            height=36,
            font="hoi_24header",
            tooltip=tooltip,
        ),
    )


DASHBOARD_CARDS = [
    ("country", "CCP_CARD_COUNTRY", "CCP_CARD_COUNTRY_VALUE"),
    ("political_power", "CCP_CARD_PP", "CCP_CARD_PP_VALUE"),
    ("command_power", "CCP_CARD_CP", "CCP_CARD_CP_VALUE"),
    ("manpower", "CCP_CARD_MANPOWER", "CCP_CARD_MANPOWER_VALUE"),
    ("army_xp", "CCP_CARD_ARMY_XP", "CCP_CARD_ARMY_XP_VALUE"),
    ("navy_xp", "CCP_CARD_NAVY_XP", "CCP_CARD_NAVY_XP_VALUE"),
    ("air_xp", "CCP_CARD_AIR_XP", "CCP_CARD_AIR_XP_VALUE"),
    ("stability", "CCP_CARD_STABILITY", "CCP_CARD_STABILITY_VALUE"),
    ("factories", "CCP_CARD_FACTORIES", "CCP_CARD_FACTORIES_VALUE"),
]


def _dashboard() -> Container:
    section = Container("ccp_section_dashboard", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    for index, (name, label, value) in enumerate(DASHBOARD_CARDS):
        section.add(
            _stat_card(name, index % 3, index // 3, label, value, f"{label}_TOOLTIP")
        )
    return section


def _settings() -> Container:
    section = Container("ccp_section_settings", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    section.add(
        Text(
            "ccp_settings_hotkey_label",
            CONTENT_X,
            BODY_TOP,
            key="CCP_SETTINGS_HOTKEY",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_hotkey_help",
            CONTENT_X,
            BODY_TOP + 24,
            key="CCP_SETTINGS_HOTKEY_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=18,
        ),
    )
    for index, (_, _, _label) in enumerate(HOTKEYS):
        section.add(
            Button(
                f"ccp_hotkey_choice_{index + 1}",
                CONTENT_X + index * (t.BUTTON_WIDTH + 8),
                BODY_TOP + 54,
                key=f"CCP_HOTKEY_{index + 1}",
                tooltip=f"CCP_HOTKEY_{index + 1}_TOOLTIP",
            )
        )
    section.add(
        Text(
            "ccp_settings_hotkey_current",
            CONTENT_X,
            BODY_TOP + 94,
            key="CCP_SETTINGS_HOTKEY_CURRENT",
            width=t.CONTENT_WIDTH - 48,
            height=18,
        ),
        Text(
            "ccp_settings_confirm_label",
            CONTENT_X,
            BODY_TOP + 140,
            key="CCP_SETTINGS_CONFIRM",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_confirm_help",
            CONTENT_X,
            BODY_TOP + 164,
            key="CCP_SETTINGS_CONFIRM_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=18,
        ),
        Button(
            "ccp_confirm_toggle",
            CONTENT_X,
            BODY_TOP + 194,
            key="CCP_GetConfirmState",
            tooltip="CCP_SETTINGS_CONFIRM_TOOLTIP",
        ),
        Text(
            "ccp_settings_language_label",
            CONTENT_X,
            BODY_TOP + 246,
            key="CCP_SETTINGS_LANGUAGE",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_language_help",
            CONTENT_X,
            BODY_TOP + 270,
            key="CCP_SETTINGS_LANGUAGE_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=72,
        ),
    )
    return section


PAD_X = t.PANEL_WIDTH - 24 - t.READOUT_WIDTH
ROW_WIDTH = PAD_X - CONTENT_X - 24

DIGIT_ROWS = [("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9")]


def _digit_pad() -> list[Widget]:
    widgets: list[Widget] = [
        Text(
            "ccp_pad_label",
            PAD_X,
            BODY_TOP,
            key="CCP_PAD_LABEL",
            width=t.READOUT_WIDTH,
            height=18,
        ),
        Icon("ccp_pad_readout_plate", PAD_X, BODY_TOP + 22, sprite="GFX_ccp_readout"),
        Text(
            "ccp_pad_readout",
            PAD_X + 10,
            BODY_TOP + 31,
            key="CCP_PAD_VALUE",
            width=t.READOUT_WIDTH - 20,
            height=22,
            font="hoi_20b",
            align="right",
        ),
    ]

    top = BODY_TOP + 22 + t.READOUT_HEIGHT + 10
    step_x = t.KEY_WIDTH + 8
    step_y = t.KEY_HEIGHT + 8

    for row, digits in enumerate(DIGIT_ROWS):
        for column, digit in enumerate(digits):
            widgets.append(
                Button(
                    f"ccp_pad_{digit}",
                    PAD_X + column * step_x,
                    top + row * step_y,
                    sprite="GFX_ccp_key",
                    key=f"CCP_PAD_DIGIT_{digit}",
                    tooltip="CCP_PAD_DIGIT_TOOLTIP",
                )
            )

    bottom = top + 3 * step_y
    widgets += [
        Button(
            "ccp_pad_0",
            PAD_X,
            bottom,
            sprite="GFX_ccp_key",
            key="CCP_PAD_DIGIT_0",
            tooltip="CCP_PAD_DIGIT_TOOLTIP",
        ),
        Button(
            "ccp_pad_back",
            PAD_X + step_x,
            bottom,
            sprite="GFX_ccp_key",
            key="CCP_PAD_BACK",
            tooltip="CCP_PAD_BACK_TOOLTIP",
        ),
        Button(
            "ccp_pad_clear",
            PAD_X + 2 * step_x,
            bottom,
            sprite="GFX_ccp_key",
            key="CCP_PAD_CLEAR",
            tooltip="CCP_PAD_CLEAR_TOOLTIP",
            click_sound="click_close",
        ),
        Text(
            "ccp_pad_help",
            PAD_X,
            bottom + t.KEY_HEIGHT + 12,
            key="CCP_PAD_HELP",
            width=t.READOUT_WIDTH,
            height=72,
        ),
    ]
    return widgets


def _resource_row(index: int, resource) -> Container:
    row = Container(
        f"ccp_row_{resource.slug}",
        CONTENT_X,
        BODY_TOP + index * t.ROW_HEIGHT,
        width=ROW_WIDTH,
        height=t.ROW_HEIGHT - 8,
    )
    row.add(
        Icon(f"ccp_row_{resource.slug}_plate", 0, 0, sprite="GFX_ccp_row"),
        Text(
            f"ccp_row_{resource.slug}_label",
            12,
            8,
            key=resource.key,
            width=240,
            height=18,
            font="hoi_18mbs",
            tooltip=f"{resource.key}_TOOLTIP",
        ),
        Text(
            f"ccp_row_{resource.slug}_value",
            12,
            29,
            key=f"{resource.key}_VALUE",
            width=240,
            height=18,
            tooltip=f"{resource.key}_TOOLTIP",
        ),
    )

    step = t.SMALL_BUTTON_WIDTH + 8
    first = ROW_WIDTH - 12 - 5 * step + 8
    for slot, amount in enumerate(resource.presets):
        row.add(
            Button(
                f"ccp_grant_{resource.slug}_{slot + 1}",
                first + slot * step,
                14,
                sprite="GFX_ccp_button_small",
                key=f"{resource.key}_P{slot + 1}",
                tooltip=f"{resource.key}_P{slot + 1}_TOOLTIP",
            )
        )
    row.add(
        Button(
            f"ccp_grant_{resource.slug}_custom",
            first + 4 * step,
            14,
            sprite="GFX_ccp_button_small",
            key="CCP_BUTTON_CUSTOM",
            tooltip=f"{resource.key}_CUSTOM_TOOLTIP",
        )
    )
    return row


def _resources() -> Container:
    from .resources import RESOURCES

    section = Container("ccp_section_resources", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    for index, resource in enumerate(RESOURCES):
        section.add(_resource_row(index, resource))
    return section


CATEGORY_WIDTH = 200
CATEGORY_HEIGHT = 26
LIST_X = CONTENT_X + CATEGORY_WIDTH + 16
LIST_WIDTH = PAD_X - LIST_X - 24
ENTRY_HEIGHT = 32
PAGE_SIZE = 16


def _equipment(categories: list[str]) -> Container:
    section = Container("ccp_section_equipment", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)

    section.add(
        Text(
            "ccp_equipment_category_heading",
            CONTENT_X,
            BODY_TOP,
            key="CCP_EQUIPMENT_CATEGORIES",
            width=CATEGORY_WIDTH,
            height=18,
        )
    )
    for index, name in enumerate(categories):
        section.add(
            Button(
                f"ccp_equipment_category_{index + 1}",
                CONTENT_X,
                BODY_TOP + 22 + index * CATEGORY_HEIGHT,
                sprite="GFX_ccp_sidebar_item",
                key=f"CCP_EQCAT_{name.upper()}",
                tooltip="CCP_EQUIPMENT_CATEGORY_TOOLTIP",
            )
        )

    section.add(
        Text(
            "ccp_equipment_list_heading",
            LIST_X,
            BODY_TOP,
            key="CCP_GetEquipmentCategoryName",
            width=LIST_WIDTH,
            height=18,
            font="hoi_18mbs",
        ),
        Grid(
            "ccp_equipment_list",
            LIST_X,
            BODY_TOP + 24,
            width=LIST_WIDTH,
            height=PAGE_SIZE * ENTRY_HEIGHT,
            slot_width=LIST_WIDTH,
            slot_height=ENTRY_HEIGHT,
            max_horizontal=1,
            max_vertical=PAGE_SIZE,
        ),
        Button(
            "ccp_equipment_prev",
            LIST_X,
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
        ),
        Text(
            "ccp_equipment_page_label",
            LIST_X + t.SMALL_BUTTON_WIDTH + 12,
            BODY_TOP + 37 + PAGE_SIZE * ENTRY_HEIGHT,
            key="CCP_EQUIPMENT_PAGE",
            width=LIST_WIDTH - 2 * (t.SMALL_BUTTON_WIDTH + 12),
            height=18,
            align="centre",
        ),
        Button(
            "ccp_equipment_next",
            LIST_X + LIST_WIDTH - t.SMALL_BUTTON_WIDTH,
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
        ),
    )
    return section


def equipment_entry_window() -> Container:
    """One row of the equipment list, instantiated per array element by the engine."""
    entry = Container("ccp_equipment_entry", 0, 0, width=LIST_WIDTH, height=ENTRY_HEIGHT)
    return entry.add(
        Icon("ccp_equipment_entry_plate", 0, 0, sprite="GFX_ccp_list_row"),
        Text(
            "ccp_equipment_entry_name",
            10,
            7,
            key="CCP_GetEquipmentName",
            width=LIST_WIDTH - 2 * t.SMALL_BUTTON_WIDTH - 40,
            height=18,
        ),
        Button(
            "ccp_equipment_entry_latest",
            LIST_WIDTH - 2 * t.SMALL_BUTTON_WIDTH - 12,
            2,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_LATEST",
            tooltip="CCP_EQUIPMENT_LATEST_TOOLTIP",
        ),
        Button(
            "ccp_equipment_entry_add",
            LIST_WIDTH - t.SMALL_BUTTON_WIDTH - 6,
            2,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_ADD",
            tooltip="CCP_EQUIPMENT_ADD_TOOLTIP",
        ),
    )


def _browser(
    slug: str,
    categories: list[str],
    category_key,
    heading_loc: str,
    extra: list[Widget] | None = None,
) -> Container:
    """A category column beside a paged list — the shape Equipment and Research share."""
    section = Container(f"ccp_section_{slug}", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)

    section.add(
        Text(
            f"ccp_{slug}_category_heading",
            CONTENT_X,
            BODY_TOP,
            key="CCP_EQUIPMENT_CATEGORIES",
            width=CATEGORY_WIDTH,
            height=18,
        )
    )
    for index, name in enumerate(categories):
        section.add(
            Button(
                f"ccp_{slug}_category_{index + 1}",
                CONTENT_X,
                BODY_TOP + 22 + index * CATEGORY_HEIGHT,
                sprite="GFX_ccp_sidebar_item",
                key=category_key(name),
                tooltip="CCP_EQUIPMENT_CATEGORY_TOOLTIP",
            )
        )

    section.add(
        Text(
            f"ccp_{slug}_list_heading",
            LIST_X,
            BODY_TOP,
            key=heading_loc,
            width=LIST_WIDTH,
            height=18,
            font="hoi_18mbs",
        ),
        Grid(
            f"ccp_{slug}_list",
            LIST_X,
            BODY_TOP + 24,
            width=LIST_WIDTH,
            height=PAGE_SIZE * ENTRY_HEIGHT,
            slot_width=LIST_WIDTH,
            slot_height=ENTRY_HEIGHT,
            max_horizontal=1,
            max_vertical=PAGE_SIZE,
        ),
        Button(
            f"ccp_{slug}_prev",
            LIST_X,
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
        ),
        Text(
            f"ccp_{slug}_page_label",
            LIST_X + t.SMALL_BUTTON_WIDTH + 12,
            BODY_TOP + 37 + PAGE_SIZE * ENTRY_HEIGHT,
            key=f"CCP_{slug.upper()}_PAGE",
            width=LIST_WIDTH - 2 * (t.SMALL_BUTTON_WIDTH + 12),
            height=18,
            align="centre",
        ),
        Button(
            f"ccp_{slug}_next",
            LIST_X + LIST_WIDTH - t.SMALL_BUTTON_WIDTH,
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
        ),
    )
    if extra:
        section.add(*extra)
    return section


def _research(folders: list[str]) -> Container:
    return _browser(
        "research",
        folders,
        lambda name: name,
        "CCP_GetResearchFolderName",
        extra=[
            Button(
                "ccp_research_all",
                LIST_X,
                BODY_TOP + 70 + PAGE_SIZE * ENTRY_HEIGHT,
                key="CCP_RESEARCH_ALL",
                tooltip="CCP_RESEARCH_ALL_TOOLTIP",
            ),
            Text(
                "ccp_research_all_help",
                LIST_X + t.BUTTON_WIDTH + 12,
                BODY_TOP + 76 + PAGE_SIZE * ENTRY_HEIGHT,
                key="CCP_RESEARCH_ALL_HELP",
                width=LIST_WIDTH - t.BUTTON_WIDTH - 12,
                height=18,
            ),
        ],
    )


def research_entry_window() -> Container:
    entry = Container("ccp_research_entry", 0, 0, width=LIST_WIDTH, height=ENTRY_HEIGHT)
    return entry.add(
        Icon("ccp_research_entry_plate", 0, 0, sprite="GFX_ccp_list_row"),
        Text(
            "ccp_research_entry_name",
            10,
            7,
            key="CCP_GetTechnologyName",
            width=LIST_WIDTH - t.SMALL_BUTTON_WIDTH - 30,
            height=18,
        ),
        Button(
            "ccp_research_entry_grant",
            LIST_WIDTH - t.SMALL_BUTTON_WIDTH - 6,
            2,
            sprite="GFX_ccp_button_small",
            key="CCP_RESEARCH_GRANT",
            tooltip="CCP_RESEARCH_GRANT_TOOLTIP",
        ),
    )


COUNTRY_LIST_WIDTH = t.CONTENT_WIDTH - 48
COUNTRY_ENTRY_HEIGHT = 34


def _country() -> Container:
    section = Container("ccp_section_country", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    return section.add(
        Text(
            "ccp_country_help",
            CONTENT_X,
            BODY_TOP,
            key="CCP_COUNTRY_HELP",
            width=COUNTRY_LIST_WIDTH,
            height=18,
        ),
        Grid(
            "ccp_country_list",
            CONTENT_X,
            BODY_TOP + 26,
            width=COUNTRY_LIST_WIDTH,
            height=PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            slot_width=COUNTRY_LIST_WIDTH,
            slot_height=COUNTRY_ENTRY_HEIGHT,
            max_horizontal=1,
            max_vertical=PAGE_SIZE,
        ),
        Button(
            "ccp_country_prev",
            CONTENT_X,
            BODY_TOP + 34 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
        ),
        Text(
            "ccp_country_page_label",
            CONTENT_X + t.SMALL_BUTTON_WIDTH + 12,
            BODY_TOP + 39 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            key="CCP_COUNTRY_PAGE",
            width=COUNTRY_LIST_WIDTH - 2 * (t.SMALL_BUTTON_WIDTH + 12),
            height=18,
            align="centre",
        ),
        Button(
            "ccp_country_next",
            CONTENT_X + COUNTRY_LIST_WIDTH - t.SMALL_BUTTON_WIDTH,
            BODY_TOP + 34 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
        ),
    )


def country_entry_window() -> Container:
    entry = Container(
        "ccp_country_entry", 0, 0, width=COUNTRY_LIST_WIDTH, height=COUNTRY_ENTRY_HEIGHT
    )
    entry.add(
        Icon("ccp_country_entry_plate", 0, 0, sprite="GFX_ccp_list_row"),
        Text(
            "ccp_country_entry_name",
            10,
            8,
            key="CCP_COUNTRY_ENTRY_NAME",
            width=COUNTRY_LIST_WIDTH - len(ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6) - 24,
            height=18,
        ),
    )
    first = COUNTRY_LIST_WIDTH - len(ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6)
    for index, action in enumerate(ACTIONS):
        entry.add(
            Button(
                f"ccp_country_entry_{action.slug}",
                first + index * (t.SMALL_BUTTON_WIDTH + 6),
                3,
                sprite="GFX_ccp_button_danger" if action.destructive else "GFX_ccp_button_small",
                key=action.key,
                tooltip=f"{action.key}_TOOLTIP",
            )
        )
    return entry


def modal_window() -> Container:
    modal_x = (t.PANEL_WIDTH - t.MODAL_WIDTH) // 2
    modal_y = (t.PANEL_HEIGHT - t.MODAL_HEIGHT) // 2
    window = Container(
        "ccp_modal_window",
        0,
        0,
        width=t.PANEL_WIDTH,
        height=t.PANEL_HEIGHT,
        orientation="center",
        origo="center",
    )
    return window.add(
        Icon("ccp_modal_scrim", 0, 0, sprite="GFX_ccp_modal_scrim"),
        Icon("ccp_modal_plate", modal_x, modal_y, sprite="GFX_ccp_modal"),
        Text(
            "ccp_modal_title",
            modal_x + 24,
            modal_y + 22,
            key="CCP_MODAL_TITLE",
            width=t.MODAL_WIDTH - 48,
            height=24,
            font="hoi_20b",
        ),
        Text(
            "ccp_modal_body",
            modal_x + 24,
            modal_y + 60,
            key="CCP_MODAL_BODY",
            width=t.MODAL_WIDTH - 48,
            height=90,
        ),
        Button(
            "ccp_modal_cancel",
            modal_x + 24,
            modal_y + t.MODAL_HEIGHT - 24 - t.BUTTON_HEIGHT,
            key="CCP_BUTTON_CANCEL",
            tooltip="CCP_TOOLTIP_CANCEL",
            click_sound="click_close",
        ),
        Button(
            "ccp_modal_confirm",
            modal_x + t.MODAL_WIDTH - 24 - t.BUTTON_WIDTH,
            modal_y + t.MODAL_HEIGHT - 24 - t.BUTTON_HEIGHT,
            sprite="GFX_ccp_button_danger",
            key="CCP_BUTTON_CONFIRM",
            tooltip="CCP_TOOLTIP_CONFIRM",
            click_sound="click_ok",
        ),
    )


STATE_LIST_WIDTH = t.CONTENT_WIDTH - 48
STATE_ENTRY_HEIGHT = 38


def _states() -> Container:
    section = Container("ccp_section_states", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    return section.add(
        Text(
            "ccp_state_help",
            CONTENT_X,
            BODY_TOP,
            key="CCP_STATE_HELP",
            width=STATE_LIST_WIDTH - t.BUTTON_WIDTH - 16,
            height=36,
        ),
        Button(
            "ccp_state_picker_toggle",
            CONTENT_X + STATE_LIST_WIDTH - t.BUTTON_WIDTH,
            BODY_TOP,
            key="CCP_GetStatePickerState",
            tooltip="CCP_STATE_PICKER_TOOLTIP",
        ),
        Grid(
            "ccp_state_list",
            CONTENT_X,
            BODY_TOP + 44,
            width=STATE_LIST_WIDTH,
            height=STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            slot_width=STATE_LIST_WIDTH,
            slot_height=STATE_ENTRY_HEIGHT,
            max_horizontal=1,
            max_vertical=STATE_PAGE_SIZE,
        ),
        Button(
            "ccp_state_prev",
            CONTENT_X,
            BODY_TOP + 52 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
        ),
        Text(
            "ccp_state_page_label",
            CONTENT_X + t.SMALL_BUTTON_WIDTH + 12,
            BODY_TOP + 57 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            key="CCP_STATE_PAGE",
            width=STATE_LIST_WIDTH - 2 * (t.SMALL_BUTTON_WIDTH + 12),
            height=18,
            align="centre",
        ),
        Button(
            "ccp_state_next",
            CONTENT_X + STATE_LIST_WIDTH - t.SMALL_BUTTON_WIDTH,
            BODY_TOP + 52 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
        ),
    )


def state_entry_window() -> Container:
    entry = Container(
        "ccp_state_entry", 0, 0, width=STATE_LIST_WIDTH, height=STATE_ENTRY_HEIGHT
    )
    entry.add(
        Icon("ccp_state_entry_plate", 0, 0, sprite="GFX_ccp_list_row"),
        Text(
            "ccp_state_entry_name",
            10,
            3,
            key="CCP_STATE_ENTRY_NAME",
            width=STATE_LIST_WIDTH - len(STATE_ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6) - 24,
            height=18,
        ),
        Text(
            "ccp_state_entry_owner",
            10,
            20,
            key="CCP_STATE_ENTRY_OWNER",
            width=STATE_LIST_WIDTH - len(STATE_ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6) - 24,
            height=16,
        ),
    )
    first = STATE_LIST_WIDTH - len(STATE_ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6)
    for index, action in enumerate(STATE_ACTIONS):
        entry.add(
            Button(
                f"ccp_state_entry_{action.slug}",
                first + index * (t.SMALL_BUTTON_WIDTH + 6),
                5,
                sprite="GFX_ccp_button_danger" if action.destructive else "GFX_ccp_button_small",
                key=action.key,
                tooltip=f"{action.key}_TOOLTIP",
            )
        )
    return entry


def state_picker_window() -> Container:
    """Attached to the state view, so clicking a state on the map acts on it directly."""
    width = len(STATE_ACTIONS) * (t.SMALL_BUTTON_WIDTH + 6) + 18
    window = Container(
        "ccp_state_picker_window",
        0,
        0,
        width=width,
        height=64,
        clipping=False,
    )
    window.add(
        Icon("ccp_picker_plate", 0, 0, sprite="GFX_ccp_card"),
        Text(
            "ccp_picker_title",
            10,
            6,
            key="CCP_STATE_PICKER_TITLE",
            width=width - 20,
            height=16,
        ),
    )
    for index, action in enumerate(STATE_ACTIONS):
        window.add(
            Button(
                f"ccp_picker_{action.slug}",
                9 + index * (t.SMALL_BUTTON_WIDTH + 6),
                26,
                sprite="GFX_ccp_button_danger" if action.destructive else "GFX_ccp_button_small",
                key=action.key,
                tooltip=f"{action.key}_TOOLTIP",
            )
        )
    return window


ACTION_COLUMNS = 3
ACTION_CARD_WIDTH = 320
ACTION_CARD_HEIGHT = 74
ACTION_CARD_GAP = 12


def _action_section(slug: str) -> Container:
    """A grid of one-click country actions, each with its own explanation."""
    section = Container(f"ccp_section_{slug}", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    section.add(
        Text(
            f"ccp_{slug}_help",
            CONTENT_X,
            BODY_TOP,
            key=f"CCP_{slug.upper()}_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=18,
        )
    )

    for index, action in enumerate(ACTION_SECTIONS[slug]):
        column = index % ACTION_COLUMNS
        row = index // ACTION_COLUMNS
        x = CONTENT_X + column * (ACTION_CARD_WIDTH + ACTION_CARD_GAP)
        y = BODY_TOP + 30 + row * (ACTION_CARD_HEIGHT + ACTION_CARD_GAP)
        card = Container(
            f"ccp_action_{action.slug}",
            x,
            y,
            width=ACTION_CARD_WIDTH,
            height=ACTION_CARD_HEIGHT,
        )
        card.add(
            Icon(f"ccp_action_{action.slug}_plate", 0, 0, sprite="GFX_ccp_card"),
            Text(
                f"ccp_action_{action.slug}_help",
                12,
                8,
                key=f"{action.key}_HELP",
                width=ACTION_CARD_WIDTH - 24,
                height=30,
            ),
            Button(
                f"ccp_action_{action.slug}_run",
                12,
                ACTION_CARD_HEIGHT - t.BUTTON_HEIGHT - 10,
                sprite="GFX_ccp_button_danger" if action.danger else "GFX_ccp_button",
                key=action.key,
                tooltip=f"{action.key}_TOOLTIP",
            ),
        )
        section.add(card)
    return section


HISTORY_LENGTH = 10
HISTORY_ROW_HEIGHT = 34
HISTORY_WIDTH = t.CONTENT_WIDTH - 48


def _history() -> Container:
    section = Container("ccp_section_history", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    section.add(
        Text(
            "ccp_history_help",
            CONTENT_X,
            BODY_TOP,
            key="CCP_HISTORY_HELP",
            width=HISTORY_WIDTH - t.BUTTON_WIDTH - 16,
            height=36,
        ),
        Button(
            "ccp_history_clear",
            CONTENT_X + HISTORY_WIDTH - t.BUTTON_WIDTH,
            BODY_TOP,
            sprite="GFX_ccp_button_danger",
            key="CCP_HISTORY_CLEAR",
            tooltip="CCP_HISTORY_CLEAR_TOOLTIP",
        ),
    )
    for slot in range(HISTORY_LENGTH):
        row = Container(
            f"ccp_history_row_{slot + 1}",
            CONTENT_X,
            BODY_TOP + 48 + slot * HISTORY_ROW_HEIGHT,
            width=HISTORY_WIDTH,
            height=HISTORY_ROW_HEIGHT - 2,
        )
        row.add(
            Icon(f"ccp_history_row_{slot + 1}_plate", 0, 0, sprite="GFX_ccp_list_row"),
            Text(
                f"ccp_history_row_{slot + 1}_text",
                10,
                7,
                key=f"CCP_HISTORY_ENTRY_{slot + 1}",
                width=HISTORY_WIDTH - t.SMALL_BUTTON_WIDTH - 30,
                height=18,
            ),
            Button(
                f"ccp_history_repeat_{slot + 1}",
                HISTORY_WIDTH - t.SMALL_BUTTON_WIDTH - 6,
                2,
                sprite="GFX_ccp_button_small",
                key="CCP_HISTORY_REPEAT",
                tooltip="CCP_HISTORY_REPEAT_TOOLTIP",
            ),
        )
        section.add(row)
    return section


SECTION_BUILDERS = {
    "dashboard": _dashboard,
    "resources": _resources,
    "settings": _settings,
}

PAD_SECTIONS = ("resources", "equipment")


def section_containers(categories: list[str], folders: list[str]) -> dict[str, Container]:
    """Each registered section, built once so layout and triggers see the same tree."""
    builders = dict(SECTION_BUILDERS)
    builders["equipment"] = lambda: _equipment(categories)
    builders["research"] = lambda: _research(folders)
    builders["country"] = _country
    builders["states"] = _states
    builders["history"] = _history
    for slug in ACTION_SECTIONS:
        builders[slug] = (lambda name: lambda: _action_section(name))(slug)
    return {section.slug: builders[section.slug]() for section in SECTIONS}


def pad_widgets() -> list[Widget]:
    """The amount pad lives outside the sections because several of them share it."""
    return _digit_pad()


def main_window(categories: list[str], folders: list[str]) -> Container:
    window = Container(
        "ccp_main_window",
        0,
        0,
        width=t.PANEL_WIDTH,
        height=t.PANEL_HEIGHT,
        orientation="center",
        origo="center",
    )
    window.add(*_header(), *_sidebar(), *_content_shell(), *_footer())
    window.add(*pad_widgets())
    window.add(*section_containers(categories, folders).values())
    return window


def launcher_window() -> Container:
    window = Container(
        "ccp_launcher_window",
        8,
        160,
        width=46,
        height=46,
        orientation="upper_left",
        clipping=False,
    )
    return window.add(
        Button(
            "ccp_launcher",
            0,
            0,
            sprite="GFX_ccp_launcher_button",
            tooltip="CCP_TOOLTIP_LAUNCHER",
        )
    )


def hotkey_window() -> Container:
    from .sections import HOTKEYS as keys

    window = Container(
        "ccp_hotkey_listener_window", 0, 0, width=8, height=8, clipping=False
    )
    for index, (shortcut, _, _) in enumerate(keys, start=1):
        window.add(
            Button(
                f"ccp_hotkey_{index}",
                0,
                0,
                sprite="GFX_ccp_blank",
                shortcut=shortcut,
                click_sound=None,
            )
        )
    return window
