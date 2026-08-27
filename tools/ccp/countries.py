"""The country actions the panel offers, and the effect each one applies.

Countries are the one large list the engine can walk at runtime: `global.countries`
is a built-in array, so no build-time table is needed here. Only the actions are
declared, and each names a native effect verified against the game documentation.
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
        ["annex_country = { target = var:ccp_pending_country }"],
        destructive=True,
    ),
    Action(
        "puppet",
        ["var:ccp_pending_country = { var:ccp_player = { puppet = PREV } }"],
        destructive=True,
    ),
    Action(
        "war",
        [
            "declare_war_on = {",
            "\ttarget = var:ccp_pending_country",
            "\ttype = annex_everything",
            "}",
        ],
        destructive=True,
    ),
    Action(
        "peace",
        ["var:ccp_pending_country = { var:ccp_player = { white_peace = PREV } }"],
        destructive=False,
    ),
    Action(
        "playas",
        [
            "set_variable = { ccp_panel_open = 0 }",
            "var:ccp_pending_country = { var:ccp_player = { change_tag_from = PREV } }",
        ],
        destructive=True,
    ),
]


def action_id(slug: str) -> int:
    for index, action in enumerate(ACTIONS, start=1):
        if action.slug == slug:
            return index
    raise KeyError(slug)
