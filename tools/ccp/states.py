"""The state actions the panel offers.

`global.states` is a built-in array, so the list is walked at runtime like the
country list.

The console separates `setowner` from `setcontroller`, and so does this: TAKE
transfers both at once, while OWN and CONTROL move one without the other, which
is what occupying a state you do not annex actually looks like.

Scoping decides how each action is written. Ownership, cores and claims have a
country-scope form that takes a state id, which is what the game's own scripts
use, so those run from the acting country and name the picked state by id.
Compliance and resistance have no country-scope form, so they run in the state
and name the acting country with PREV.

Nothing here reads a bare `var:name`. A variable belongs to the scope that set
it, and every one of these steps into a country or a state first; `globals.py`
qualifies the reads with ROOT, the country the panel belongs to.
"""

from __future__ import annotations

from dataclasses import dataclass

PAGE_SIZE = 14

PLAYER = "var:ccp_player"
TARGET = "var:ccp_target_country"

STATE_ID = "var:ccp_state_id"


@dataclass(frozen=True)
class StateAction:
    slug: str
    actor: str
    body: list[str]
    destructive: bool
    in_state: bool = False

    @property
    def key(self) -> str:
        return f"CCP_STATE_{self.slug.upper()}"


ACTIONS: list[StateAction] = [
    StateAction("take", PLAYER, [f"transfer_state = {STATE_ID}"], destructive=True),
    StateAction("own", PLAYER, [f"set_state_owner = {STATE_ID}"], destructive=True),
    StateAction("control", PLAYER, [f"set_state_controller = {STATE_ID}"], destructive=True),
    StateAction("give", TARGET, [f"transfer_state = {STATE_ID}"], destructive=True),
    StateAction(
        "give_control", TARGET, [f"set_state_controller = {STATE_ID}"], destructive=True
    ),
    StateAction("core", PLAYER, [f"add_state_core = {STATE_ID}"], destructive=False),
    StateAction("uncore", PLAYER, [f"remove_state_core = {STATE_ID}"], destructive=True),
    StateAction("claim", PLAYER, [f"add_state_claim = {STATE_ID}"], destructive=False),
    StateAction("unclaim", PLAYER, [f"remove_state_claim = {STATE_ID}"], destructive=True),
    StateAction("comply", PLAYER, ["add_compliance = 100"], destructive=False, in_state=True),
    StateAction("quiet", PLAYER, ["add_resistance = -100"], destructive=False, in_state=True),
]
