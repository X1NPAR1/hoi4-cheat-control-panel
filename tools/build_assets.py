"""Derives every image the mod ships, plus its sprite definitions, from one source.

    python tools/build_assets.py

The Workshop thumbnail and the in-panel logo come from logo.png; the interface
plates are drawn from the palette in tools/ccp/theme.py, which was sampled from
that same logo. mod/interface/ccp_gfx.gfx is emitted from the same list, so a
sprite name, its texture and its frame count can never drift apart.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp import theme
from ccp.plates import STRETCHABLE, build as build_plates, frames as frame_strip, plate

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "logo.png"
GFX_DIR = REPO_ROOT / "mod" / "gfx" / "interface" / "ccp"
GFX_FILE = REPO_ROOT / "mod" / "interface" / "ccp_gfx.gfx"

THUMBNAIL_SIZE = 512
PANEL_LOGO_HEIGHT = 40
LAUNCHER_BUTTON_SIZE = 46
LAUNCHER_LOGO_SIZE = 38

BANNER = (
    "# GENERATED FILE - DO NOT EDIT\n"
    "# Produced by tools/build_assets.py alongside the textures it references.\n"
)


def sprite_name(filename: str) -> str:
    return f"GFX_{Path(filename).stem}"


def emit_gfx(entries: list[tuple[str, int]], sizes: dict[str, tuple[int, int]]) -> str:
    """Plates that carry a border are nine-sliced so they stretch to any size."""
    lines = [BANNER.rstrip(), "", "spriteTypes = {"]
    for filename, frames in entries:
        width, height = sizes[filename]
        if filename in STRETCHABLE:
            lines += [
                "\tcorneredTileSpriteType = {",
                f'\t\tname = "{sprite_name(filename)}"',
                f"\t\tsize = {{ x = {width} y = {height} }}",
                f'\t\ttextureFile = "gfx/interface/ccp/{filename}"',
                "\t\tborderSize = { x = 6 y = 6 }",
                "\t\ttilingCenter = yes",
                '\t\teffectFile = "gfx/FX/buttonstate.lua"',
                "\t}",
            ]
        else:
            lines += [
                "\tspriteType = {",
                f'\t\tname = "{sprite_name(filename)}"',
                f'\t\ttexturefile = "gfx/interface/ccp/{filename}"',
                f"\t\tnoOfFrames = {frames}",
                "\t}",
            ]
    lines += ["}", ""]
    return "\n".join(lines)


def _launcher_button(source: Image.Image) -> Image.Image:
    """A four-state top-left button carrying the logo, the panel's always-visible entry point."""
    size = (LAUNCHER_BUTTON_SIZE, LAUNCHER_BUTTON_SIZE)
    borders = [theme.BORDER_STEEL, theme.ACCENT_BRONZE, theme.ACCENT_BRONZE, theme.BORDER_STEEL]
    fills = [theme.BG_PANEL, theme.BG_RAISED, theme.BG_BASE, theme.BG_BASE]

    badge = source.resize((LAUNCHER_LOGO_SIZE, LAUNCHER_LOGO_SIZE), Image.LANCZOS)
    offset = (LAUNCHER_BUTTON_SIZE - LAUNCHER_LOGO_SIZE) // 2

    states = []
    for fill, border in zip(fills, borders):
        state = plate(size, fill, border=border, shade=theme.BG_BASE)
        state.alpha_composite(badge, (offset, offset))
        states.append(state)
    return frame_strip(*states)


def main() -> int:
    if not SOURCE.is_file():
        print(f"{SOURCE} not found", file=sys.stderr)
        return 2

    GFX_DIR.mkdir(parents=True, exist_ok=True)
    GFX_FILE.parent.mkdir(parents=True, exist_ok=True)

    source = Image.open(SOURCE).convert("RGBA")

    thumbnail_path = REPO_ROOT / "mod" / "thumbnail.png"
    source.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.LANCZOS).convert("RGB").save(
        thumbnail_path, "PNG", optimize=True
    )

    logo_scale = PANEL_LOGO_HEIGHT / source.height
    logo = source.resize(
        (max(1, round(source.width * logo_scale)), PANEL_LOGO_HEIGHT), Image.LANCZOS
    )
    logo.save(GFX_DIR / "ccp_logo.png", "PNG", optimize=True)

    launcher = _launcher_button(source)
    launcher.save(GFX_DIR / "ccp_launcher_button.png", "PNG", optimize=True)

    entries: list[tuple[str, int]] = [
        ("ccp_logo.png", 1),
        ("ccp_launcher_button.png", 4),
    ]
    for filename, image, frames in build_plates(GFX_DIR):
        image.save(GFX_DIR / filename, "PNG", optimize=True)
        entries.append((filename, frames))

    sizes = {
        filename: Image.open(GFX_DIR / filename).size for filename, _ in entries
    }
    GFX_FILE.write_text(emit_gfx(entries, sizes), encoding="utf-8", newline="\n")

    print(f"  {thumbnail_path.relative_to(REPO_ROOT).as_posix():<48} {THUMBNAIL_SIZE}x{THUMBNAIL_SIZE}")
    for filename, frames in entries:
        image = Image.open(GFX_DIR / filename)
        size = (GFX_DIR / filename).stat().st_size
        print(
            f"  {('mod/gfx/interface/ccp/' + filename):<48} "
            f"{image.width}x{image.height}  {frames} frame(s)  {size / 1024:.0f} KB"
        )
    print(f"  {GFX_FILE.relative_to(REPO_ROOT).as_posix():<48} {len(entries)} sprite(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
