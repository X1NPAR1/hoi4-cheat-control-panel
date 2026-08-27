"""A small widget model that emits Clausewitz `.gui` files.

Authoring the interface as data rather than by hand keeps every element on the
grid defined in `theme.py`: spacing, row heights and column positions are
computed, never typed twice, so nothing drifts out of alignment.
"""

from __future__ import annotations

from dataclasses import dataclass, field

INDENT = "\t"

BANNER = (
    "# GENERATED FILE - DO NOT EDIT\n"
    "# Produced by tools/build_interface.py from tools/ccp/interface.py.\n"
)


def loc(key: str) -> str:
    """Scripted localisation is referenced by name in brackets; plain keys are not."""
    return f"[{key}]" if key.startswith("CCP_Get") else key


def _block(kind: str, body: list[str], depth: int) -> list[str]:
    pad = INDENT * depth
    return [f"{pad}{kind} = {{}}"] if not body else [
        f"{pad}{kind} = {{",
        *(f"{INDENT * (depth + 1)}{line}" for line in body),
        f"{pad}}}",
    ]


@dataclass
class Widget:
    name: str
    x: int = 0
    y: int = 0

    kind = "iconType"

    def properties(self) -> list[str]:
        return []

    def emit(self, depth: int) -> list[str]:
        body = [f'name = "{self.name}"', f"position = {{ x = {self.x} y = {self.y} }}"]
        body += self.properties()
        return _block(self.kind, body, depth)


@dataclass
class Icon(Widget):
    sprite: str = ""
    frame: int | None = None
    orientation: str | None = None

    kind = "iconType"

    def properties(self) -> list[str]:
        out = [f'spriteType = "{self.sprite}"']
        if self.frame is not None:
            out.append(f"frame = {self.frame}")
        if self.orientation:
            out.append(f"orientation = {self.orientation}")
        return out


@dataclass
class Text(Widget):
    key: str = ""
    width: int = 200
    height: int = 20
    font: str = "hoi_16mbs"
    align: str = "left"
    tooltip: str | None = None
    orientation: str | None = None

    kind = "instantTextBoxType"

    def properties(self) -> list[str]:
        out = [
            f'font = "{self.font}"',
            f'text = "{loc(self.key)}"',
            f"maxWidth = {self.width}",
            f"maxHeight = {self.height}",
            f"format = {self.align}",
        ]
        if self.tooltip:
            out.append(f'pdx_tooltip = "{self.tooltip}"')
        if self.orientation:
            out.append(f"orientation = {self.orientation}")
        return out


@dataclass
class Button(Widget):
    sprite: str = "GFX_ccp_button"
    key: str | None = None
    font: str = "hoi_16mbs"
    tooltip: str | None = None
    shortcut: str | None = None
    click_sound: str | None = "click_default"
    orientation: str | None = None
    width: int | None = None
    height: int | None = None

    kind = "buttonType"

    def properties(self) -> list[str]:
        out = [f'quadTextureSprite = "{self.sprite}"']
        if self.width is not None and self.height is not None:
            out.append(f"size = {{ x = {self.width} y = {self.height} }}")
        if self.key:
            out += [f'buttonText = "{loc(self.key)}"', f'buttonFont = "{self.font}"']
        if self.tooltip:
            out.append(f'pdx_tooltip = "{self.tooltip}"')
        if self.shortcut:
            out.append(f'shortcut = "{self.shortcut}"')
        if self.click_sound:
            out.append(f"clicksound = {self.click_sound}")
        if self.orientation:
            out.append(f"orientation = {self.orientation}")
        return out


@dataclass
class Grid(Widget):
    width: int = 100
    height: int = 100
    slot_width: int = 100
    slot_height: int = 32
    align: str = "UPPER_LEFT"
    max_horizontal: int | None = None
    max_vertical: int | None = None

    kind = "gridboxType"

    def properties(self) -> list[str]:
        out = [
            f"size = {{ width = {self.width} height = {self.height} }}",
            f"slotsize = {{ width = {self.slot_width} height = {self.slot_height} }}",
            f'format = "{self.align}"',
        ]
        if self.max_horizontal is not None:
            out.append(f"max_slots_horizontal = {self.max_horizontal}")
        if self.max_vertical is not None:
            out.append(f"max_slots_vertical = {self.max_vertical}")
        return out


@dataclass
class Container(Widget):
    width: int = 0
    height: int = 0
    orientation: str | None = None
    origo: str | None = None
    clipping: bool | None = None
    moveable: bool = False
    children: list[Widget] = field(default_factory=list)

    kind = "containerWindowType"

    def add(self, *widgets: Widget) -> "Container":
        self.children.extend(widgets)
        return self

    def leaves(self) -> list[str]:
        """Names of every drawable descendant.

        Visibility triggers apply to drawable elements, not to containers, so a
        section is hidden by hiding each of its leaves.
        """
        names: list[str] = []
        for child in self.children:
            if isinstance(child, Container):
                names += child.leaves()
            else:
                names.append(child.name)
        return names

    def emit(self, depth: int) -> list[str]:
        body = [f'name = "{self.name}"']
        if self.orientation:
            body.append(f"orientation = {self.orientation}")
        if self.origo:
            body.append(f"origo = {self.origo}")
        body.append(f"position = {{ x = {self.x} y = {self.y} }}")
        if self.width or self.height:
            body.append(f"size = {{ width = {self.width} height = {self.height} }}")
        body.append(f"moveable = {'yes' if self.moveable else 'no'}")
        if self.clipping is not None:
            body.append(f"clipping = {'yes' if self.clipping else 'no'}")

        lines = [
            f"{INDENT * depth}{self.kind} = {{",
            *(f"{INDENT * (depth + 1)}{line}" for line in body),
        ]
        for child in self.children:
            lines.append("")
            lines += child.emit(depth + 1)
        lines.append(f"{INDENT * depth}}}")
        return lines


def emit_file(*windows: Container) -> str:
    lines = [BANNER.rstrip(), "", "guiTypes = {"]
    for window in windows:
        lines.append("")
        lines += window.emit(1)
    lines += ["}", ""]
    return "\n".join(lines)
