"""Country-wide and commander actions, declared as data.

Every `body` is native script verified against the game's own
`effects_documentation.md`. Nothing here reaches for a console command, because
script cannot invoke one; where no native equivalent exists the action is simply
absent rather than present and broken.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Action:
    slug: str
    body: list[str]
    section: str
    destructive: bool = False
    danger: bool = False

    @property
    def key(self) -> str:
        return f"CCP_ACTION_{self.slug.upper()}"


def _all_owned(effect: str) -> list[str]:
    return [
        "every_owned_state = {",
        f"\t{effect}",
        "}",
    ]


NATION: list[Action] = [
    Action("stability_max", ["set_stability = 1"], "nation"),
    Action("war_support_max", ["set_war_support = 1"], "nation"),
    Action("stability_min", ["set_stability = 0"], "nation", danger=True),
    Action("war_support_min", ["set_war_support = 0"], "nation", danger=True),
    Action("research_slots", ["set_research_slots = 5"], "nation"),
    Action(
        "fuel",
        ["add_fuel = 500000"],
        "nation",
    ),
]

CONSTRUCTION: list[Action] = [
    Action(
        "infrastructure",
        _all_owned("add_building_construction = { type = infrastructure level = 5 instant_build = yes }"),
        "construction",
    ),
    Action(
        "civilian",
        _all_owned("add_building_construction = { type = industrial_complex level = 5 instant_build = yes }"),
        "construction",
    ),
    Action(
        "military",
        _all_owned("add_building_construction = { type = arms_factory level = 5 instant_build = yes }"),
        "construction",
    ),
    Action(
        "dockyard",
        [
            "every_owned_state = {",
            "\tlimit = { is_coastal = yes }",
            "\tadd_building_construction = { type = dockyard level = 3 instant_build = yes }",
            "}",
        ],
        "construction",
    ),
    Action(
        "airbase",
        _all_owned("add_building_construction = { type = air_base level = 10 instant_build = yes }"),
        "construction",
    ),
    Action(
        "radar",
        _all_owned("add_building_construction = { type = radar_station level = 3 instant_build = yes }"),
        "construction",
    ),
    Action(
        "antiair",
        _all_owned("add_building_construction = { type = anti_air_building level = 3 instant_build = yes }"),
        "construction",
    ),
    Action(
        "offsite_civilian",
        ["add_offsite_building = { type = industrial_complex level = 20 }"],
        "construction",
    ),
    Action(
        "offsite_military",
        ["add_offsite_building = { type = arms_factory level = 20 }"],
        "construction",
    ),
]

COMMANDERS: list[Action] = [
    Action(
        "army_xp",
        [
            "every_army_leader = {",
            "\tadd_skill_level = 1",
            "}",
        ],
        "commanders",
    ),
    Action(
        "navy_xp",
        [
            "every_navy_leader = {",
            "\tadd_skill_level = 1",
            "}",
        ],
        "commanders",
    ),
    Action(
        "attack",
        ["every_army_leader = {", "\tadd_attack = 1", "}"],
        "commanders",
    ),
    Action(
        "defense",
        ["every_army_leader = {", "\tadd_defense = 1", "}"],
        "commanders",
    ),
    Action(
        "planning",
        ["every_army_leader = {", "\tadd_planning = 1", "}"],
        "commanders",
    ),
    Action(
        "logistics",
        ["every_army_leader = {", "\tadd_logistics = 1", "}"],
        "commanders",
    ),
]

BY_SECTION: dict[str, list[Action]] = {
    "nation": NATION,
    "construction": CONSTRUCTION,
    "commanders": COMMANDERS,
}

ALL: list[Action] = [action for actions in BY_SECTION.values() for action in actions]
