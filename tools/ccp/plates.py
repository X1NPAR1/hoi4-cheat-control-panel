"""Draws the panel's flat UI plates so every surface matches the logo palette exactly."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from . import theme

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


def build(out_dir: Path) -> list[tuple[str, Image.Image, int]]:
    """Every plate the interface needs, as `(filename, image, frame count)`."""
    t = theme

    panel_body = plate(
        (t.PANEL_WIDTH, t.PANEL_HEIGHT - t.HEADER_HEIGHT),
        t.BG_PANEL,
        shade=t.BG_BASE,
    )
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

    sidebar_size = (t.SIDEBAR_ITEM_WIDTH, t.SIDEBAR_ITEM_HEIGHT)
    sidebar_item = frames(
        plate(sidebar_size, t.BG_BASE, border=None),
        plate(sidebar_size, t.BG_RAISED, border=None, accent_edge=t.ACCENT_BRONZE_DIM),
        plate(sidebar_size, t.BG_PANEL, border=None, accent_edge=t.ACCENT_BRONZE),
    )

    button_size = (t.BUTTON_WIDTH, t.BUTTON_HEIGHT)
    button = frames(
        plate(button_size, t.BG_RAISED, shade=t.BG_PANEL, border=t.BORDER_STEEL),
        plate(button_size, t.ACCENT_BRONZE_DIM, shade=t.BG_RAISED, border=t.ACCENT_BRONZE),
        plate(button_size, t.BG_PANEL, shade=t.BG_BASE, border=t.ACCENT_BRONZE),
        plate(button_size, t.BG_BASE, border=t.BORDER_STEEL),
    )
    button_danger = frames(
        plate(button_size, t.BG_RAISED, shade=t.BG_PANEL, border=t.DANGER),
        plate(button_size, t.DANGER, shade=t.BG_RAISED, border=t.DANGER),
        plate(button_size, t.BG_PANEL, shade=t.BG_BASE, border=t.DANGER),
        plate(button_size, t.BG_BASE, border=t.BORDER_STEEL),
    )
    button_confirm = frames(
        plate(button_size, t.BG_RAISED, shade=t.BG_PANEL, border=t.ACCENT_OLIVE),
        plate(button_size, t.ACCENT_OLIVE, shade=t.BG_RAISED, border=t.ACCENT_OLIVE),
        plate(button_size, t.BG_PANEL, shade=t.BG_BASE, border=t.ACCENT_OLIVE),
        plate(button_size, t.BG_BASE, border=t.BORDER_STEEL),
    )

    chip_size = (t.CHIP_WIDTH, t.CHIP_HEIGHT)
    chip = frames(
        plate(chip_size, t.BG_BASE, border=t.BORDER_STEEL),
        plate(chip_size, t.BG_RAISED, border=t.ACCENT_BRONZE),
        plate(chip_size, t.ACCENT_BRONZE_DIM, border=t.ACCENT_BRONZE),
        plate(chip_size, t.BG_BASE, border=t.BORDER_STEEL),
    )

    row_size = (t.LIST_ROW_WIDTH, t.LIST_ROW_HEIGHT)
    list_row = frames(
        plate(row_size, t.BG_PANEL, border=None),
        plate(row_size, t.BG_RAISED, border=None, accent_edge=t.ACCENT_BRONZE_DIM, accent_edge_width=2),
        plate(row_size, t.BG_RAISED, border=None, accent_edge=t.ACCENT_BRONZE, accent_edge_width=2),
    )

    modal_scrim = Image.new("RGBA", (t.PANEL_WIDTH, t.PANEL_HEIGHT), (*t.BG_BASE, 210))
    modal = plate(
        (t.MODAL_WIDTH, t.MODAL_HEIGHT), t.BG_PANEL, shade=t.BG_RAISED, border=t.ACCENT_BRONZE
    )

    divider = plate((t.CONTENT_WIDTH - 48, 1), t.BORDER_STEEL, border=None)
    blank = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    card = plate((320, 96), t.BG_PANEL, shade=t.BG_RAISED, border=t.BORDER_STEEL)

    return [
        ("ccp_panel_body.png", panel_body, 1),
        ("ccp_panel_header.png", header, 1),
        ("ccp_panel_sidebar.png", sidebar, 1),
        ("ccp_panel_footer.png", footer, 1),
        ("ccp_sidebar_item.png", sidebar_item, 3),
        ("ccp_button.png", button, 4),
        ("ccp_button_danger.png", button_danger, 4),
        ("ccp_button_confirm.png", button_confirm, 4),
        ("ccp_chip.png", chip, 4),
        ("ccp_list_row.png", list_row, 3),
        ("ccp_modal_scrim.png", modal_scrim, 1),
        ("ccp_modal.png", modal, 1),
        ("ccp_divider.png", divider, 1),
        ("ccp_blank.png", blank, 1),
        ("ccp_card.png", card, 1),
    ]
