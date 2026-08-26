"""The state actions the panel offers.

`global.states` is a built-in array, so the list is walked at runtime like the
country list.

Scoping matters here. `set_state_owner` is a country effect that takes a state;
the state-scope pair is `set_state_owner_to` / `set_state_controller_to`. And the
core and claim effects accept only the documented target keywords, not a variable,
so each action runs the state from inside the acting country and refers back to
it with PREV. That is why `body` is written as a nested pair rather than a flat
list: the outer scope is the country doing the acting, the inner one is the state.
"""

from __future__ import annotations

from dataclasses import dataclass

PAGE_SIZE = 14

PLAYER = "var:ccp_player"
TARGET = "var:ccp_target_country"


@dataclass(frozen=True)
class StateAction:
    slug: str
    actor: str
    body: list[str]
    destructive: bool

    @property
    def key(self) -> str:
        return f"CCP_STATE_{self.slug.upper()}"


ACTIONS: list[StateAction] = [
    StateAction(
        "take",
        PLAYER,
        ["set_state_owner_to = PREV", "set_state_controller_to = PREV"],
        destructive=True,
    ),
    StateAction(
        "give",
        TARGET,
        ["set_state_owner_to = PREV", "set_state_controller_to = PREV"],
        destructive=True,
    ),
    StateAction("core", PLAYER, ["add_core_of = PREV"], destructive=False),
    StateAction("uncore", PLAYER, ["remove_core_of = PREV"], destructive=True),
    StateAction("claim", PLAYER, ["add_claim_by = PREV"], destructive=False),
]
