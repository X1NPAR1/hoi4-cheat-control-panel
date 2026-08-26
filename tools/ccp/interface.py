"""Builds the panel's windows from the design grid in `theme.py`."""

from __future__ import annotations

from . import theme as t
from .layout import Button, Container, Grid, Icon, Text, Widget
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
    )
    return section


def main_window() -> Container:
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
    window.add(_dashboard(), _settings())
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
