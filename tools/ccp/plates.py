"""Draws the panel's flat UI plates so every surface matches the logo palette exactly."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from . import theme
from . import theme as t_theme

RGB = tuple[int, int, int]


def _vertical_shade(size: tuple[int, int], top: RGB, bottom: RGB) -> Image.Image:
    width, height = size
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    span = max(1, height - 1)
    for y in range(height):
        ratio = y / span
        colour = tuple(round(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=(*colour, 255))
    return image


def plate(
    size: tuple[int, int],
    fill: RGB,
    *,
    border: RGB | None = theme.BORDER_STEEL,
    shade: RGB | None = None,
    accent_edge: RGB | None = None,
    accent_edge_width: int = 3,
) -> Image.Image:
    """A flat surface with an optional top-to-bottom shade and a left accent edge."""
    image = _vertical_shade(size, fill, shade) if shade else Image.new("RGBA", size, (*fill, 255))
    draw = ImageDraw.Draw(image)
    if border is not None:
        draw.rectangle([0, 0, size[0] - 1, size[1] - 1], outline=(*border, 255))
    if accent_edge is not None:
        draw.rectangle([0, 0, accent_edge_width - 1, size[1] - 1], fill=(*accent_edge, 255))
    return image


def frames(*images: Image.Image) -> Image.Image:
    """Packs equally sized images side by side into one HOI4 sprite strip."""
    width = sum(image.width for image in images)
    height = max(image.height for image in images)
    strip = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    offset = 0
    for image in images:
        strip.paste(image, (offset, 0))
        offset += image.width
    return strip


def rounded(size: tuple[int, int], fill: RGB, border: RGB, shade: RGB | None = None) -> Image.Image:
    """A single-state plate meant to be stretched by a nine-slice sprite."""
    return plate(size, fill, border=border, shade=shade)


def build(out_dir: Path) -> list[tuple[str, Image.Image, int]]:
    """Every plate the interface needs, as `(filename, image, frame count)`."""
    t = theme

    panel_body = plate(
        (t.PANEL_WIDTH, t.PANEL_HEIGHT - t.HEADER_HEIGHT),
        t.BG_PANEL,
        shade=t.BG_BASE,
    )
    panel_body.putalpha(t.BODY_ALPHA)
    header = plate(
        (t.PANEL_WIDTH, t.HEADER_HEIGHT),
        t.BG_RAISED,
        shade=t.BG_PANEL,
        border=t.ACCENT_BRONZE_DIM,
    )
    sidebar = plate(
        (t.SIDEBAR_WIDTH, t.PANEL_HEIGHT - t.HEADER_HEIGHT - t.FOOTER_HEIGHT),
        t.BG_BASE,
        border=t.BORDER_STEEL,
    )
    footer = plate((t.PANEL_WIDTH, t.FOOTER_HEIGHT), t.BG_BASE, border=t.BORDER_STEEL)


    tile = (24, t.BUTTON_HEIGHT)
    button = rounded(tile, t.BG_RAISED, t.BORDER_STEEL, shade=t.BG_PANEL)
    button_danger = rounded(tile, t.BG_RAISED, t.DANGER, shade=t.BG_PANEL)
    button_confirm = rounded(tile, t.BG_RAISED, t.ACCENT_OLIVE, shade=t.BG_PANEL)

    small_tile = (20, t.SMALL_BUTTON_HEIGHT)
    button_small = rounded(small_tile, t.BG_RAISED, t.BORDER_STEEL, shade=t.BG_PANEL)
    button_small_danger = rounded(small_tile, t.BG_RAISED, t.DANGER, shade=t.BG_PANEL)

    key = rounded((20, t.KEY_HEIGHT), t.BG_RAISED, t.BORDER_STEEL, shade=t.BG_PANEL)

    readout = plate(
        (t.READOUT_WIDTH, t.READOUT_HEIGHT),
        t.BG_BASE,
        border=t.ACCENT_BRONZE_DIM,
    )

    row_plate = plate(
        (t.CONTENT_WIDTH - 48 - t.READOUT_WIDTH - 48, t.ROW_HEIGHT - 8),
        t.BG_PANEL,
        border=t.BORDER_STEEL,
    )

    list_row = rounded((20, t.LIST_ROW_HEIGHT), t.BG_PANEL, t.BORDER_STEEL)
    sidebar_tile = rounded((20, t.SIDEBAR_ITEM_HEIGHT), t.BG_BASE, t.BG_BASE)
    sidebar_active = plate(
        (t.SIDEBAR_WIDTH, t.SIDEBAR_ITEM_HEIGHT),
        t.BG_PANEL,
        border=t.ACCENT_BRONZE_DIM,
        accent_edge=t.ACCENT_BRONZE,
    )

    modal_scrim = Image.new("RGBA", (t.PANEL_WIDTH, t.PANEL_HEIGHT), (*t.BG_BASE, t.SCRIM_ALPHA))
    modal = plate(
        (t.MODAL_WIDTH, t.MODAL_HEIGHT), t.BG_PANEL, shade=t.BG_RAISED, border=t.ACCENT_BRONZE
    )

    divider = plate((t.CONTENT_WIDTH - 48, 1), t.BORDER_STEEL, border=None)
    blank = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    card = rounded((20, 20), t.BG_PANEL, t.BORDER_STEEL, shade=t.BG_RAISED)

    return [
        ("ccp_panel_body.png", panel_body, 1),
        ("ccp_panel_header.png", header, 1),
        ("ccp_panel_sidebar.png", sidebar, 1),
        ("ccp_panel_footer.png", footer, 1),
        ("ccp_modal_scrim.png", modal_scrim, 1),
        ("ccp_modal.png", modal, 1),
        ("ccp_readout.png", readout, 1),
        ("ccp_row.png", row_plate, 1),
        ("ccp_divider.png", divider, 1),
        ("ccp_blank.png", blank, 1),
        ("ccp_sidebar_item.png", sidebar_tile, 1),
        ("ccp_sidebar_active.png", sidebar_active, 1),
        ("ccp_button.png", button, 1),
        ("ccp_button_danger.png", button_danger, 1),
        ("ccp_button_confirm.png", button_confirm, 1),
        ("ccp_button_small.png", button_small, 1),
        ("ccp_button_small_danger.png", button_small_danger, 1),
        ("ccp_key.png", key, 1),
        ("ccp_list_row.png", list_row, 1),
        ("ccp_card.png", card, 1),
    ]


STRETCHABLE = {
    "ccp_sidebar_item.png",
    "ccp_button.png",
    "ccp_button_danger.png",
    "ccp_button_confirm.png",
    "ccp_button_small.png",
    "ccp_button_small_danger.png",
    "ccp_key.png",
}


def exact_plates() -> list[tuple[str, Image.Image, int]]:
    """Plates an iconType draws, each at the exact size that icon occupies."""
    from . import interface as ui

    sizes = {
        "ccp_plate_card": (ui.CARD_WIDTH, ui.CARD_HEIGHT),
        "ccp_plate_action": (ui.ACTION_CARD_WIDTH, ui.ACTION_CARD_HEIGHT),
        "ccp_plate_row_equipment": (ui.LIST_WIDTH, ui.ENTRY_HEIGHT - 2),
        "ccp_plate_row_country": (ui.COUNTRY_LIST_WIDTH, ui.COUNTRY_ENTRY_HEIGHT - 2),
        "ccp_plate_row_state": (ui.STATE_LIST_WIDTH, ui.STATE_ENTRY_HEIGHT - 2),
        "ccp_plate_row_history": (ui.HISTORY_WIDTH, ui.HISTORY_ROW_HEIGHT - 2),
        "ccp_plate_row_resource": (ui.ROW_WIDTH, t_theme.ROW_HEIGHT - 8),
        "ccp_plate_picker": (ui.picker_width(), 68),
    }
    return [
        (f"{name}.png", rounded(size, t_theme.BG_PANEL, t_theme.BORDER_STEEL, shade=t_theme.BG_RAISED), 1)
        for name, size in sizes.items()
    ]
