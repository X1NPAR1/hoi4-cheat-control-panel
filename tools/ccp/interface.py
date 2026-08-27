"""Builds the panel's windows from the design grid in `theme.py`."""

from __future__ import annotations

from . import theme as t
from .layout import Button, Container, Grid, Icon, Text, Widget

_LABELS: dict[str, dict[str, str]] | None = None

SMALL_SPRITES = {"GFX_ccp_button_small", "GFX_ccp_button_small_danger"}


def _labels() -> dict[str, dict[str, str]]:
    global _LABELS
    if _LABELS is None:
        from .strings import all_strings

        _LABELS = all_strings()
    return _LABELS


def label_width(key: str | None, font: str, padding: int, minimum: int) -> int:
    """Wide enough for the longest translation of this label, in any language.

    Buttons are sized here rather than left to a fixed sprite width, so a German
    or Russian label cannot spill past its own button or collide with the next one.
    """
    if key is None:
        return minimum
    row = _labels().get(key)
    if row is None:
        return minimum
    longest = max(t.text_width(value, font) for value in row.values())
    return max(minimum, longest + padding)


def button_width(key: str | None, sprite: str = "GFX_ccp_button") -> int:
    if sprite in SMALL_SPRITES:
        return label_width(key, "hoi_16mbs", t.SMALL_BUTTON_PADDING, t.SMALL_BUTTON_MIN_WIDTH)
    return label_width(key, "hoi_16mbs", t.BUTTON_PADDING, t.BUTTON_MIN_WIDTH)


def button_height(sprite: str = "GFX_ccp_button") -> int:
    return t.SMALL_BUTTON_HEIGHT if sprite in SMALL_SPRITES else t.BUTTON_HEIGHT


def action_button(name: str, x: int, y: int, key: str, sprite: str, tooltip: str) -> Button:
    return Button(
        name,
        x,
        y,
        sprite=sprite,
        key=key,
        tooltip=tooltip,
        width=button_width(key, sprite),
        height=button_height(sprite),
    )


def right_aligned_row(
    prefix: str,
    entries: list[tuple[str, str, str, bool]],
    right_edge: int,
    y: int,
    gap: int = 6,
) -> tuple[list[Button], int]:
    """Lay buttons out from the right edge using their real widths.

    Returns the buttons and the width they occupy, so the label beside them can be
    given exactly the space that is left instead of a guess.
    """
    sized = [
        (slug, key, sprite, tooltip, button_width(key, sprite))
        for slug, key, sprite, tooltip in entries
    ]
    total = sum(width for *_, width in sized) + gap * (len(sized) - 1 if sized else 0)
    x = right_edge - total
    buttons: list[Button] = []
    for slug, key, sprite, tooltip, width in sized:
        buttons.append(
            Button(
                f"{prefix}_{slug}",
                x,
                y,
                sprite=sprite,
                key=key,
                tooltip=tooltip,
                width=width,
                height=button_height(sprite),
            )
        )
        x += width + gap
    return buttons, total

from .actions import BY_SECTION as ACTION_SECTIONS, level_id
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

CARD_GAP = 16
CARD_WIDTH = (t.CONTENT_WIDTH - 48 - 2 * CARD_GAP) // 3
CARD_HEIGHT = 104

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
            -16 - button_width("CCP_BUTTON_CLOSE"),
            16,
            key="CCP_BUTTON_CLOSE",
            tooltip="CCP_TOOLTIP_CLOSE",
            click_sound="click_close",
            orientation="upper_right",
            width=button_width("CCP_BUTTON_CLOSE"),
            height=t.BUTTON_HEIGHT,
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
        Icon(
            "ccp_nav_highlight",
            0,
            NAV_TOP,
            sprite="GFX_ccp_sidebar_active",
        ),
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
                width=t.SIDEBAR_WIDTH,
                height=t.SIDEBAR_ITEM_HEIGHT,
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
        Icon(
            f"ccp_card_{name}_plate",
            0,
            0,
            sprite="GFX_ccp_plate_card",
        ),
        Text(
            f"ccp_card_{name}_label",
            16,
            16,
            key=label,
            width=CARD_WIDTH - 32,
            height=18,
            tooltip=tooltip,
        ),
        Text(
            f"ccp_card_{name}_value",
            16,
            44,
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
    section.add(
        Icon(
            "ccp_ironman_plate",
            CONTENT_X,
            BODY_TOP,
            sprite="GFX_ccp_plate_action",
        ),
        Text(
            "ccp_ironman_notice",
            CONTENT_X + 16,
            BODY_TOP + 16,
            key="CCP_IRONMAN_LOCKED",
            width=t.CONTENT_WIDTH - 80,
            height=86,
            font="hoi_18mbs",
        ),
    )
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
    x = CONTENT_X
    for index, (_, _, _label) in enumerate(HOTKEYS):
        key = f"CCP_HOTKEY_{index + 1}"
        width = button_width(key)
        section.add(
            Button(
                f"ccp_hotkey_choice_{index + 1}",
                x,
                BODY_TOP + 54,
                key=key,
                tooltip=f"{key}_TOOLTIP",
                width=width,
                height=t.BUTTON_HEIGHT,
            )
        )
        x += width + 8
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
            width=max(button_width("CCP_CONFIRM_ON"), button_width("CCP_CONFIRM_OFF")),
            height=t.BUTTON_HEIGHT,
        ),
        Text(
            "ccp_settings_diplo_label",
            CONTENT_X,
            BODY_TOP + 246,
            key="CCP_SETTINGS_DIPLO",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_diplo_help",
            CONTENT_X,
            BODY_TOP + 270,
            key="CCP_SETTINGS_DIPLO_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=36,
        ),
        Button(
            "ccp_diplo_rules_toggle",
            CONTENT_X,
            BODY_TOP + 310,
            key="CCP_GetDiploRulesState",
            tooltip="CCP_SETTINGS_DIPLO_TOOLTIP",
            width=max(button_width("CCP_DIPLO_ON"), button_width("CCP_DIPLO_OFF")),
            height=t.BUTTON_HEIGHT,
        ),
        Button(
            "ccp_ai_goodwill_toggle",
            CONTENT_X + max(button_width("CCP_DIPLO_ON"), button_width("CCP_DIPLO_OFF")) + 10,
            BODY_TOP + 310,
            key="CCP_GetGoodwillState",
            tooltip="CCP_SETTINGS_GOODWILL_TOOLTIP",
            width=max(button_width("CCP_GOODWILL_ON"), button_width("CCP_GOODWILL_OFF")),
            height=t.BUTTON_HEIGHT,
        ),
        Text(
            "ccp_settings_language_label",
            CONTENT_X,
            BODY_TOP + 352,
            key="CCP_SETTINGS_LANGUAGE",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_compat_label",
            CONTENT_X,
            BODY_TOP + 396,
            key="CCP_SETTINGS_COMPAT",
            width=t.CONTENT_WIDTH - 48,
            height=20,
            font="hoi_18mbs",
        ),
        Text(
            "ccp_settings_compat_help",
            CONTENT_X,
            BODY_TOP + 420,
            key="CCP_SETTINGS_COMPAT_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=72,
        ),
        Text(
            "ccp_settings_ironman",
            CONTENT_X,
            BODY_TOP + 496,
            key="CCP_GetIronmanNotice",
            width=t.CONTENT_WIDTH - 48,
            height=36,
        ),
        Text(
            "ccp_settings_language_help",
            CONTENT_X,
            BODY_TOP + 376,
            key="CCP_SETTINGS_LANGUAGE_HELP",
            width=t.CONTENT_WIDTH - 48,
            height=72,
        ),
    )
    return section


PAD_X = t.PANEL_WIDTH - 24 - t.READOUT_WIDTH
ROW_LABEL_WIDTH = 260
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
                    width=t.KEY_WIDTH,
                    height=t.KEY_HEIGHT,
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
            width=t.KEY_WIDTH,
            height=t.KEY_HEIGHT,
        ),
        Button(
            "ccp_pad_back",
            PAD_X + step_x,
            bottom,
            sprite="GFX_ccp_key",
            key="CCP_PAD_BACK",
            tooltip="CCP_PAD_BACK_TOOLTIP",
            width=t.KEY_WIDTH,
            height=t.KEY_HEIGHT,
        ),
        Button(
            "ccp_pad_clear",
            PAD_X + 2 * step_x,
            bottom,
            sprite="GFX_ccp_key",
            key="CCP_PAD_CLEAR",
            tooltip="CCP_PAD_CLEAR_TOOLTIP",
            width=t.KEY_WIDTH,
            height=t.KEY_HEIGHT,
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
        Icon(f"ccp_row_{resource.slug}_plate", 0, 0, sprite="GFX_ccp_plate_row_resource"),
        Text(
            f"ccp_row_{resource.slug}_label",
            12,
            8,
            key=resource.key,
            width=ROW_LABEL_WIDTH,
            height=18,
            font="hoi_18mbs",
            tooltip=f"{resource.key}_TOOLTIP",
        ),
        Text(
            f"ccp_row_{resource.slug}_value",
            12,
            29,
            key=f"{resource.key}_VALUE",
            width=ROW_LABEL_WIDTH,
            height=18,
            tooltip=f"{resource.key}_TOOLTIP",
        ),
    )

    entries = [
        (
            str(slot + 1),
            f"{resource.key}_P{slot + 1}",
            "GFX_ccp_button_small",
            f"{resource.key}_P{slot + 1}_TOOLTIP",
        )
        for slot in range(len(resource.presets))
    ]
    entries.append(
        ("custom", "CCP_BUTTON_CUSTOM", "GFX_ccp_button_small", f"{resource.key}_CUSTOM_TOOLTIP")
    )
    buttons, used = right_aligned_row(
        f"ccp_grant_{resource.slug}", entries, ROW_WIDTH - 12, 14
    )
    row.add(*buttons)
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
STOCK_WIDTH = 96


def _equipment(categories: list[str]) -> Container:
    return _browser(
        "equipment",
        categories,
        lambda name: f"CCP_EQCAT_{name.upper()}",
        "CCP_GetEquipmentCategoryName",
        extra=[
            Button(
                "ccp_equipment_all",
                LIST_X,
                BODY_TOP + 70 + PAGE_SIZE * ENTRY_HEIGHT,
                key="CCP_EQUIPMENT_ALL",
                tooltip="CCP_EQUIPMENT_ALL_TOOLTIP",
                width=button_width("CCP_EQUIPMENT_ALL"),
                height=t.BUTTON_HEIGHT,
            ),
            Text(
                "ccp_equipment_all_help",
                LIST_X + button_width("CCP_EQUIPMENT_ALL") + 12,
                BODY_TOP + 76 + PAGE_SIZE * ENTRY_HEIGHT,
                key="CCP_EQUIPMENT_ALL_HELP",
                width=LIST_WIDTH - button_width("CCP_EQUIPMENT_ALL") - 12,
                height=18,
            ),
        ],
    )


def _equipment_unused(categories: list[str]) -> Container:
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
                width=CATEGORY_WIDTH,
                height=CATEGORY_HEIGHT - 2,
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
            f"ccp_equipment_prev",
            LIST_X,
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
        Text(
            "ccp_equipment_page_label",
            LIST_X + button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") + 12,
            BODY_TOP + 37 + PAGE_SIZE * ENTRY_HEIGHT,
            key="CCP_EQUIPMENT_PAGE",
            width=LIST_WIDTH - button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small") - 24,
            height=18,
            align="centre",
        ),
        Button(
            f"ccp_equipment_next",
            LIST_X + LIST_WIDTH - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
    )
    return section


def equipment_entry_window() -> Container:
    """One row of the equipment list, instantiated per array element by the engine."""
    entry = Container("ccp_equipment_entry", 0, 0, width=LIST_WIDTH, height=ENTRY_HEIGHT)
    buttons, used = right_aligned_row(
        "ccp_equipment_entry",
        [
            ("latest", "CCP_EQUIPMENT_LATEST", "GFX_ccp_button_small", "CCP_EQUIPMENT_LATEST_TOOLTIP"),
            ("add", "CCP_EQUIPMENT_ADD", "GFX_ccp_button_small", "CCP_EQUIPMENT_ADD_TOOLTIP"),
        ],
        LIST_WIDTH - 8,
        2,
    )
    entry.add(
        Icon(
            "ccp_equipment_entry_plate",
            0,
            0,
            sprite="GFX_ccp_plate_row_equipment",
        ),
        Text(
            "ccp_equipment_entry_name",
            12,
            7,
            key="CCP_GetEquipmentName",
            width=LIST_WIDTH - used - STOCK_WIDTH - 36,
            height=18,
        ),
        Text(
            "ccp_equipment_entry_stock",
            LIST_WIDTH - used - STOCK_WIDTH - 16,
            7,
            key="CCP_GetEquipmentStock",
            width=STOCK_WIDTH,
            height=18,
            align="right",
            tooltip="CCP_EQUIPMENT_STOCK_TOOLTIP",
        ),
    )
    entry.add(*buttons)
    return entry


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
                width=CATEGORY_WIDTH,
                height=CATEGORY_HEIGHT - 2,
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
            width=button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
        Text(
            f"ccp_{slug}_page_label",
            LIST_X + button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") + 12,
            BODY_TOP + 37 + PAGE_SIZE * ENTRY_HEIGHT,
            key=f"CCP_{slug.upper()}_PAGE",
            width=LIST_WIDTH - button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small") - 24,
            height=18,
            align="centre",
        ),
        Button(
            f"ccp_{slug}_next",
            LIST_X + LIST_WIDTH - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            BODY_TOP + 32 + PAGE_SIZE * ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
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
                width=button_width("CCP_RESEARCH_ALL"),
                height=t.BUTTON_HEIGHT,
            ),
            Button(
                "ccp_research_everything",
                LIST_X + button_width("CCP_RESEARCH_ALL") + 10,
                BODY_TOP + 70 + PAGE_SIZE * ENTRY_HEIGHT,
                sprite="GFX_ccp_button_confirm",
                key="CCP_RESEARCH_EVERYTHING",
                tooltip="CCP_RESEARCH_EVERYTHING_TOOLTIP",
                width=button_width("CCP_RESEARCH_EVERYTHING"),
                height=t.BUTTON_HEIGHT,
            ),
            Text(
                "ccp_research_all_help",
                LIST_X,
                BODY_TOP + 106 + PAGE_SIZE * ENTRY_HEIGHT,
                key="CCP_RESEARCH_ALL_HELP",
                width=LIST_WIDTH,
                height=18,
            ),
        ],
    )


def research_entry_window() -> Container:
    entry = Container("ccp_research_entry", 0, 0, width=LIST_WIDTH, height=ENTRY_HEIGHT)
    buttons, used = right_aligned_row(
        "ccp_research_entry",
        [("grant", "CCP_RESEARCH_GRANT", "GFX_ccp_button_small", "CCP_RESEARCH_GRANT_TOOLTIP")],
        LIST_WIDTH - 8,
        2,
    )
    entry.add(
        Icon(
            "ccp_research_entry_plate",
            0,
            0,
            sprite="GFX_ccp_plate_row_equipment",
        ),
        Text(
            "ccp_research_entry_name",
            12,
            7,
            key="CCP_GetTechnologyName",
            width=LIST_WIDTH - used - 28,
            height=18,
        ),
    )
    entry.add(*buttons)
    return entry


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
            f"ccp_country_prev",
            CONTENT_X,
            BODY_TOP + 34 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
        Text(
            "ccp_country_page_label",
            CONTENT_X + button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") + 12,
            BODY_TOP + 39 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            key="CCP_COUNTRY_PAGE",
            width=COUNTRY_LIST_WIDTH - button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small") - 24,
            height=18,
            align="centre",
        ),
        Button(
            f"ccp_country_next",
            CONTENT_X + COUNTRY_LIST_WIDTH - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            BODY_TOP + 34 + PAGE_SIZE * COUNTRY_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
    )


def country_entry_window() -> Container:
    entry = Container(
        "ccp_country_entry", 0, 0, width=COUNTRY_LIST_WIDTH, height=COUNTRY_ENTRY_HEIGHT
    )
    entries = [
        ("target", "CCP_COUNTRY_TARGET", "GFX_ccp_button_small", "CCP_COUNTRY_TARGET_TOOLTIP")
    ]
    entries += [
        (
            action.slug,
            action.key,
            "GFX_ccp_button_small_danger" if action.destructive else "GFX_ccp_button_small",
            f"{action.key}_TOOLTIP",
        )
        for action in ACTIONS
    ]
    buttons, used = right_aligned_row(
        "ccp_country_entry", entries, COUNTRY_LIST_WIDTH - 8, 3
    )
    entry.add(
        Icon(
            "ccp_country_entry_plate",
            0,
            0,
            sprite="GFX_ccp_plate_row_country",
        ),
        Text(
            "ccp_country_entry_name",
            12,
            8,
            key="CCP_COUNTRY_ENTRY_NAME",
            width=COUNTRY_LIST_WIDTH - used - 28,
            height=18,
        ),
    )
    entry.add(*buttons)
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
            width=button_width("CCP_BUTTON_CANCEL"),
            height=t.BUTTON_HEIGHT,
        ),
        Button(
            "ccp_modal_confirm",
            modal_x + t.MODAL_WIDTH - 24 - button_width("CCP_BUTTON_CONFIRM"),
            modal_y + t.MODAL_HEIGHT - 24 - t.BUTTON_HEIGHT,
            sprite="GFX_ccp_button_danger",
            key="CCP_BUTTON_CONFIRM",
            tooltip="CCP_TOOLTIP_CONFIRM",
            click_sound="click_ok",
            width=button_width("CCP_BUTTON_CONFIRM"),
            height=t.BUTTON_HEIGHT,
        ),
    )


STATE_LIST_WIDTH = t.CONTENT_WIDTH - 48
PICKER_TOGGLE_WIDTH = max(
    button_width("CCP_STATE_PICKER_ON"), button_width("CCP_STATE_PICKER_OFF")
)
STATE_ENTRY_HEIGHT = 38


def _states() -> Container:
    section = Container("ccp_section_states", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    return section.add(
        Text(
            "ccp_state_help",
            CONTENT_X,
            BODY_TOP,
            key="CCP_STATE_HELP",
            width=STATE_LIST_WIDTH - PICKER_TOGGLE_WIDTH - 16,
            height=22,
        ),
        Text(
            "ccp_state_target",
            CONTENT_X,
            BODY_TOP + 22,
            key="CCP_STATE_TARGET",
            width=STATE_LIST_WIDTH - PICKER_TOGGLE_WIDTH - 16,
            height=18,
        ),
        Button(
            "ccp_state_picker_toggle",
            CONTENT_X + STATE_LIST_WIDTH - PICKER_TOGGLE_WIDTH,
            BODY_TOP,
            key="CCP_GetStatePickerState",
            tooltip="CCP_STATE_PICKER_TOOLTIP",
            width=PICKER_TOGGLE_WIDTH,
            height=t.BUTTON_HEIGHT,
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
            f"ccp_state_prev",
            CONTENT_X,
            BODY_TOP + 52 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_PREV",
            tooltip="CCP_EQUIPMENT_PREV_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
        Text(
            "ccp_state_page_label",
            CONTENT_X + button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") + 12,
            BODY_TOP + 57 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            key="CCP_STATE_PAGE",
            width=STATE_LIST_WIDTH - button_width("CCP_EQUIPMENT_PREV", "GFX_ccp_button_small") - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small") - 24,
            height=18,
            align="centre",
        ),
        Button(
            f"ccp_state_next",
            CONTENT_X + STATE_LIST_WIDTH - button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            BODY_TOP + 52 + STATE_PAGE_SIZE * STATE_ENTRY_HEIGHT,
            sprite="GFX_ccp_button_small",
            key="CCP_EQUIPMENT_NEXT",
            tooltip="CCP_EQUIPMENT_NEXT_TOOLTIP",
            width=button_width("CCP_EQUIPMENT_NEXT", "GFX_ccp_button_small"),
            height=t.SMALL_BUTTON_HEIGHT,
        ),
    )


def state_entry_window() -> Container:
    entry = Container(
        "ccp_state_entry", 0, 0, width=STATE_LIST_WIDTH, height=STATE_ENTRY_HEIGHT
    )
    buttons, used = right_aligned_row(
        "ccp_state_entry",
        [
            (
                action.slug,
                action.key,
                "GFX_ccp_button_small_danger" if action.destructive else "GFX_ccp_button_small",
                f"{action.key}_TOOLTIP",
            )
            for action in STATE_ACTIONS
        ],
        STATE_LIST_WIDTH - 8,
        5,
    )
    label_width_available = STATE_LIST_WIDTH - used - 28
    entry.add(
        Icon(
            "ccp_state_entry_plate",
            0,
            0,
            sprite="GFX_ccp_plate_row_state",
        ),
        Text(
            "ccp_state_entry_name",
            12,
            4,
            key="CCP_STATE_ENTRY_NAME",
            width=label_width_available,
            height=18,
        ),
        Text(
            "ccp_state_entry_owner",
            12,
            21,
            key="CCP_STATE_ENTRY_OWNER",
            width=label_width_available,
            height=16,
        ),
    )
    entry.add(*buttons)
    return entry


def picker_width() -> int:
    widths = [
        button_width(action.key, "GFX_ccp_button_small") for action in STATE_ACTIONS
    ]
    return sum(widths) + 6 * (len(widths) - 1) + 20


def state_picker_window() -> Container:
    """Attached to the state view, so clicking a state on the map acts on it directly."""
    widths = [
        button_width(action.key, "GFX_ccp_button_small") for action in STATE_ACTIONS
    ]
    width = picker_width()
    window = Container(
        "ccp_state_picker_window",
        0,
        0,
        width=width,
        height=68,
        clipping=False,
    )
    window.add(
        Icon("ccp_picker_plate", 0, 0, sprite="GFX_ccp_plate_picker"),
        Text(
            "ccp_picker_title",
            10,
            7,
            key="CCP_STATE_PICKER_TITLE",
            width=width - 20,
            height=16,
        ),
    )
    x = 10
    for action, width_of in zip(STATE_ACTIONS, widths):
        window.add(
            Button(
                f"ccp_picker_{action.slug}",
                x,
                30,
                sprite="GFX_ccp_button_small_danger"
                if action.destructive
                else "GFX_ccp_button_small",
                key=action.key,
                tooltip=f"{action.key}_TOOLTIP",
                width=width_of,
                height=t.SMALL_BUTTON_HEIGHT,
            )
        )
        x += width_of + 6
    return window


ACTION_COLUMNS = 4
ACTION_CARD_GAP = 16
ACTION_CARD_WIDTH = (
    t.CONTENT_WIDTH - 48 - (ACTION_COLUMNS - 1) * ACTION_CARD_GAP
) // ACTION_COLUMNS
ACTION_CARD_HEIGHT = 130


ACTION_LEVEL_HEIGHT = 26
ACTION_LEVEL_GAP = 5


def _action_card(action, x: int, y: int) -> Container:
    """One action: a title, its explanation, and a button for every level it offers."""
    card = Container(
        f"ccp_action_{action.slug}",
        x,
        y,
        width=ACTION_CARD_WIDTH,
        height=ACTION_CARD_HEIGHT,
    )
    card.add(
        Icon(
            f"ccp_action_{action.slug}_plate",
            0,
            0,
            sprite="GFX_ccp_plate_action",
        ),
        Text(
            f"ccp_action_{action.slug}_title",
            14,
            9,
            key=action.key,
            width=ACTION_CARD_WIDTH - 28,
            height=34,
            font="hoi_18mbs",
        ),
        Text(
            f"ccp_action_{action.slug}_help",
            14,
            44,
            key=f"{action.key}_HELP",
            width=ACTION_CARD_WIDTH - 28,
            height=ACTION_CARD_HEIGHT - ACTION_LEVEL_HEIGHT - 58,
        ),
    )

    sprite = "GFX_ccp_button_small_danger" if action.danger else "GFX_ccp_button_small"
    widths = [
        max(
            t.SMALL_BUTTON_MIN_WIDTH,
            t.text_width(action.caption(level)) + t.SMALL_BUTTON_PADDING,
        )
        for level in action.levels
    ]
    span = sum(widths) + ACTION_LEVEL_GAP * (len(widths) - 1)
    slot = 14
    if span > ACTION_CARD_WIDTH - 28:
        # Too many levels to sit side by side; share the row evenly instead.
        each = (ACTION_CARD_WIDTH - 28 - ACTION_LEVEL_GAP * (len(widths) - 1)) // len(widths)
        widths = [each] * len(widths)

    for level, width in zip(action.levels, widths):
        card.add(
            Button(
                f"ccp_action_{action.slug}_{level_id(level)}",
                slot,
                ACTION_CARD_HEIGHT - ACTION_LEVEL_HEIGHT - 10,
                sprite=sprite,
                key=f"{action.key}_{level_id(level)}",
                tooltip=f"{action.key}_TOOLTIP",
                width=width,
                height=ACTION_LEVEL_HEIGHT,
            )
        )
        slot += width + ACTION_LEVEL_GAP
    return card


def _action_section(slug: str) -> Container:
    """A grid of country actions, each offering several amounts."""
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
        section.add(
            _action_card(
                action,
                CONTENT_X + column * (ACTION_CARD_WIDTH + ACTION_CARD_GAP),
                BODY_TOP + 30 + row * (ACTION_CARD_HEIGHT + ACTION_CARD_GAP),
            )
        )
    return section


HISTORY_LENGTH = 10
HISTORY_ROW_HEIGHT = 34
HISTORY_WIDTH = t.CONTENT_WIDTH - 48
REPEAT_WIDTH = button_width("CCP_HISTORY_REPEAT", "GFX_ccp_button_small")


def _history() -> Container:
    section = Container("ccp_section_history", 0, 0, width=t.PANEL_WIDTH, height=t.PANEL_HEIGHT)
    section.add(
        Text(
            "ccp_history_help",
            CONTENT_X,
            BODY_TOP,
            key="CCP_HISTORY_HELP",
            width=HISTORY_WIDTH - button_width("CCP_HISTORY_CLEAR") - 16,
            height=36,
        ),
        Button(
            "ccp_history_clear",
            CONTENT_X + HISTORY_WIDTH - button_width("CCP_HISTORY_CLEAR"),
            BODY_TOP,
            sprite="GFX_ccp_button_danger",
            key="CCP_HISTORY_CLEAR",
            tooltip="CCP_HISTORY_CLEAR_TOOLTIP",
            width=button_width("CCP_HISTORY_CLEAR"),
            height=t.BUTTON_HEIGHT,
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
            Icon(
                f"ccp_history_row_{slot + 1}_plate",
                0,
                0,
                sprite="GFX_ccp_plate_row_history",
            ),
            Text(
                f"ccp_history_row_{slot + 1}_text",
                12,
                7,
                key=f"CCP_HISTORY_ENTRY_{slot + 1}",
                width=HISTORY_WIDTH - REPEAT_WIDTH - 30,
                height=18,
            ),
            Button(
                f"ccp_history_repeat_{slot + 1}",
                HISTORY_WIDTH - REPEAT_WIDTH - 8,
                3,
                sprite="GFX_ccp_button_small",
                key="CCP_HISTORY_REPEAT",
                tooltip="CCP_HISTORY_REPEAT_TOOLTIP",
                width=REPEAT_WIDTH,
                height=t.SMALL_BUTTON_HEIGHT,
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
