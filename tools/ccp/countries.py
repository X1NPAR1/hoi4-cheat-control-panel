"""The country actions the panel offers, and the effect each one applies.

Countries are the one large list the engine can walk at runtime: `global.countries`
is a built-in array, so no build-time table is needed here. Only the actions are
declared, and each names a native effect verified against the game documentation.

Every action steps into the target and refers back to the player with ROOT, which
each of these effects documents as a supported target. Passing the stored country
as a variable argument is not documented and reading a panel variable from inside
the target's scope reads nothing at all.
"""

from __future__ import annotations

from dataclasses import dataclass

PAGE_SIZE = 16


@dataclass(frozen=True)
class Action:
    slug: str
    body: list[str]
    destructive: bool

    @property
    def key(self) -> str:
        return f"CCP_COUNTRY_{self.slug.upper()}"


ACTIONS: list[Action] = [
    Action(
        "annex",
        [
            "var:ccp_pending_country = {",
            "	ROOT = { annex_country = { target = PREV transfer_troops = yes } }",
            "}",
        ],
        destructive=True,
    ),
    Action(
        "puppet",
        ["var:ccp_pending_country = { ROOT = { puppet = PREV } }"],
        destructive=True,
    ),
    Action(
        "war",
        [
            "var:ccp_pending_country = {",
            "	ROOT = { declare_war_on = { target = PREV type = annex_everything } }",
            "}",
        ],
        destructive=True,
    ),
    Action(
        "peace",
        ["var:ccp_pending_country = { ROOT = { white_peace = PREV } }"],
        destructive=False,
    ),
    Action(
        "playas",
        [
            "set_variable = { ccp_panel_open = 0 }",
            # The scope is the country being taken over and the argument is the
            # player being moved -- `SLO = { change_tag_from = ROOT }` in the game's
            # own CZE decisions. Written the other way round it hands your country
            # to them instead of giving you theirs.
            "var:ccp_pending_country = { change_tag_from = ROOT }",
        ],
        destructive=True,
    ),
]


def action_id(slug: str) -> int:
    for index, action in enumerate(ACTIONS, start=1):
        if action.slug == slug:
            return index
    raise KeyError(slug)
