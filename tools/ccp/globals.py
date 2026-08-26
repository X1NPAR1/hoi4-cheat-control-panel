"""Rewrites the panel's own variables into the global namespace.

The panel's state — which section is open, the amount on the pad, the current page —
is read from places whose scope is not the player. A country list entry is scoped to
a country, a state list entry to a state, and the map picker to the state that was
clicked. A country-scoped variable simply does not exist there, so every one of
those reads returned zero and the rows hid themselves.

Panel state therefore lives on `global.`, which every scope can read. Temp
variables stay local: they exist only inside the effect that sets them, so
globalising them would be wrong.
"""

from __future__ import annotations

import re

TEMP_NAMES = {
    "ccp_page_first",
    "ccp_page_last",
    "ccp_page_remainder",
    "ccp_slot",
    "ccp_grant",
    "ccp_pad_last",
    "ccp_first",
    "ccp_last",
}

# The value and index a dynamic list exposes to its entry are engine-provided
# temporaries, not panel state.
LIST_LOCALS = {"v", "i"}

_TEMP_EFFECT = re.compile(r"\b\w*temp_variable\b")

_READ = re.compile(r"\bvar:(ccp_[a-z0-9_]+)")
_ARRAY_INDEX = re.compile(r"\b(ccp_[a-z0-9_]+)\^")
_FIELD = re.compile(
    r"\b(check_variable|set_variable|add_to_variable|subtract_from_variable"
    r"|multiply_variable|divide_variable|modulo_variable|round_variable"
    r"|clear_array|resize_array|clamp_variable|dirty)\s*=\s*(\{\s*)?(var\s*=\s*)?(ccp_[a-z0-9_]+)"
)
_ARRAY_FIELD = re.compile(r"\barray\s*=\s*(ccp_[a-z0-9_]+)")
_LOC_READ = re.compile(r"\[\?(ccp_[a-z0-9_]+)")
# Any remaining `= ccp_name` is a read: the names being written were already
# rewritten above, and quoted names are widget references, not variables.
_BARE_READ = re.compile(r"=\s*(ccp_[a-z0-9_]+)")


def _keep_local(name: str) -> bool:
    return name in TEMP_NAMES or name in LIST_LOCALS


def _read(match: re.Match) -> str:
    name = match.group(1)
    return match.group(0) if _keep_local(name) else f"= global.{name}"


def globalise_script(text: str) -> str:
    """Prefix panel variables with `global.` everywhere except temp variables."""
    out: list[str] = []
    for line in text.splitlines():
        if _TEMP_EFFECT.search(line):
            # The temp variable being written stays local; what it reads may not be.
            line = _READ.sub(
                lambda m: m.group(0) if _keep_local(m.group(1)) else f"var:global.{m.group(1)}",
                line,
            )
            line = _BARE_READ.sub(_read, line)
            line = _ARRAY_INDEX.sub(
                lambda m: m.group(0) if _keep_local(m.group(1)) else f"global.{m.group(1)}^",
                line,
            )
            out.append(line)
            continue

        def field(match: re.Match) -> str:
            name = match.group(4)
            if _keep_local(name):
                return match.group(0)
            return match.group(0)[: -len(name)] + f"global.{name}"

        line = _FIELD.sub(field, line)
        line = _ARRAY_FIELD.sub(
            lambda m: m.group(0) if _keep_local(m.group(1)) else f"array = global.{m.group(1)}",
            line,
        )
        line = _READ.sub(
            lambda m: m.group(0) if _keep_local(m.group(1)) else f"var:global.{m.group(1)}",
            line,
        )
        line = _ARRAY_INDEX.sub(
            lambda m: m.group(0) if _keep_local(m.group(1)) else f"global.{m.group(1)}^",
            line,
        )
        line = _BARE_READ.sub(_read, line)
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def globalise_localisation(text: str) -> str:
    """The same for `[?variable]` reads inside localisation values."""
    return _LOC_READ.sub(
        lambda m: m.group(0) if _keep_local(m.group(1)) else f"[?global.{m.group(1)}",
        text,
    )
