"""The state actions the panel offers.

`global.states` is a built-in array, so the list is walked at runtime like the
country list. Every action targets the player's country, which is what a cheat
panel is for, and each uses a native effect from the game's own documentation.
"""

from __future__ import annotations

from dataclasses import dataclass

PAGE_SIZE = 14


@dataclass(frozen=True)
class StateAction:
    slug: str
    body: list[str]
    destructive: bool

    @property
    def key(self) -> str:
        return f"CCP_STATE_{self.slug.upper()}"


ACTIONS: list[StateAction] = [
    StateAction(
        "take",
        [
            "set_state_owner = var:ccp_player",
            "set_state_controller = var:ccp_player",
        ],
        destructive=True,
    ),
    StateAction(
        "give",
        [
            "set_state_owner = var:ccp_target_country",
            "set_state_controller = var:ccp_target_country",
        ],
        destructive=True,
    ),
    StateAction("core", ["add_core_of = var:ccp_player"], destructive=False),
    StateAction("uncore", ["remove_core_of = var:ccp_player"], destructive=True),
    StateAction("claim", ["add_claim_by = var:ccp_player"], destructive=False),
]
