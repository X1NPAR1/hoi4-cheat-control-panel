"""Puts the few variables that cross scopes into the global namespace.

Most of the panel runs in the player's country scope and can use ordinary
country variables. A handful cannot:

* a country list entry is scoped to a country,
* a state list entry to a state,
* the map picker to the state that was clicked.

A country variable does not exist in those scopes, so a read there returns zero
and the widget hides itself. Only the variables read or written from one of those
places are globalised, by name.

Everything else stays local on purpose. Arrays in particular must not be
globalised: a scripted GUI's `dynamic_lists` block takes a plain array name, and
prefixing it stops the list from populating at all.
"""

from __future__ import annotations

import re

GLOBAL_NAMES = frozenset(
    {
        # read by list entries and by the map picker, which are not player-scoped
        "ccp_section",
        "ccp_panel_open",
        "ccp_state_picker_on",
        "ccp_confirm_destructive",
        # scopes the panel remembers so no action has to guess what ROOT means
        "ccp_player",
        "ccp_target_country",
        "ccp_state",
        # the pending action is set from a country entry and applied from the modal
        "ccp_pending_action",
        "ccp_pending_country",
        "ccp_modal_open",
        # written from any scope, shown in the footer
        "ccp_status",
    }
)

# Scopes the panel stores. `var:name` is how script enters a stored scope, and the
# engine rejects `var:global.name` as a malformed token, so these keep a country
# copy alongside the global one: a trigger in a foreign scope reads `global.name`,
# an effect in the player's scope enters `var:name`.
SCOPE_NAMES = frozenset(
    {
        "ccp_player",
        "ccp_target_country",
        "ccp_state",
        "ccp_pending_country",
    }
)

_NAME = re.compile(r"\b(?<!global\.)(?<!var:)(?<!ROOT\.)(ccp_[a-z0-9_]+)")

_ASSIGN = re.compile(r"^(\s*)set_variable = \{ global\.(ccp_[a-z0-9_]+) = (.+?) \}\s*$")


def _mirror(line: str) -> list[str]:
    """A global scope assignment also writes the country copy that `var:` needs.

    The copy goes on ROOT, the country the panel belongs to, because the click
    that stores a scope often happens inside a list entry: writing it locally
    there would put it on the listed country instead of the player.
    """
    match = _ASSIGN.match(line)
    if match is None or match.group(2) not in SCOPE_NAMES:
        return [line]
    indent, name, value = match.groups()
    if value != "THIS":
        raise ValueError(f"a stored scope must be assigned from THIS, not {value!r}")
    return [line, f"{indent}ROOT = {{ set_variable = {{ {name} = PREV }} }}"]


_READ = re.compile(r"var:(?!ROOT\.)(ccp_[a-z0-9_]+)")


def _qualify_reads(text: str) -> str:
    """Name the scope a stored variable is read from.

    A variable belongs to the scope that set it. Bare `var:name` therefore reads
    nothing once an effect has stepped into another country or a state, and the
    block it guards is skipped without a word in error.log. The panel keeps its
    variables on ROOT, so every read says so.
    """
    return _READ.sub(lambda m: f"var:ROOT.{m.group(1)}", text)


def _swap(text: str) -> str:
    return _NAME.sub(
        lambda m: f"global.{m.group(1)}" if m.group(1) in GLOBAL_NAMES else m.group(0),
        text,
    )


def globalise_script(text: str) -> str:
    """Qualify the cross-scope variables, leaving quoted names alone.

    Quoted words are widget and window names, not variables, so they are copied
    through untouched.
    """
    out: list[str] = []
    for line in text.splitlines():
        if '"' in line:
            parts = line.split('"')
            parts[::2] = [_swap(part) for part in parts[::2]]
            swapped = '"'.join(parts)
        else:
            swapped = _swap(line)
        out.extend(_mirror(_qualify_reads(swapped)))
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def globalise_localisation(text: str) -> str:
    """The same for `[?variable]` reads inside localisation values."""
    return re.sub(
        r"\[\?(ccp_[a-z0-9_]+)",
        lambda m: f"[?global.{m.group(1)}" if m.group(1) in GLOBAL_NAMES else m.group(0),
        text,
    )
