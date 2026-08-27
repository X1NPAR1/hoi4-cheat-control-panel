"""Country-wide actions, declared as data.

Every action carries a set of **levels** rather than a single amount, so each one
draws a row of buttons instead of a lone fixed choice. `build` turns a level into
the script that applies it.

Every effect used here was verified against the game's own
`effects_documentation.md`. Nothing reaches for a console command, because script
cannot invoke one; where no native equivalent exists the action is simply absent
rather than present and broken.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Action:
    slug: str
    section: str
    build: Callable[[int], list[str]]
    levels: tuple[int, ...]
    label: str = "+{n}"
    danger: bool = False
    confirm: bool = False

    @property
    def key(self) -> str:
        return f"CCP_ACTION_{self.slug.upper()}"

    def caption(self, level: int) -> str:
        if abs(level) >= 1_000_000 and level % 1_000_000 == 0:
            shown = f"{level // 1_000_000}M"
        elif abs(level) >= 1_000 and level % 1_000 == 0:
            shown = f"{level // 1_000}K"
        else:
            shown = str(level)
        return self.label.replace("{n}", shown)

    def level_key(self, index: int) -> str:
        return f"{self.key}_L{index + 1}"


def _owned(effect: str) -> list[str]:
    return ["every_owned_state = {", f"\t{effect}", "}"]


def _owned_limited(limit: str, effect: str) -> list[str]:
    return [
        "every_owned_state = {",
        f"\tlimit = {{ {limit} }}",
        f"\t{effect}",
        "}",
    ]


def _build(kind: str) -> Callable[[int], list[str]]:
    return lambda n: _owned(
        f"add_building_construction = {{ type = {kind} level = {n} instant_build = yes }}"
    )


def _army_leaders(effect: str) -> Callable[[int], list[str]]:
    return lambda n: ["every_army_leader = {", f"\t{effect} = {n}", "}"]


def _navy_leaders(effect: str) -> Callable[[int], list[str]]:
    return lambda n: ["every_navy_leader = {", f"\t{effect} = {n}", "}"]


# ---------------------------------------------------------------- nation

NATION: list[Action] = [
    Action("stability", "nation", lambda n: [f"add_stability = 0.{n:02d}"], (5, 10, 25, 50), "+{n}%"),
    Action(
        "stability_full",
        "nation",
        lambda n: ["set_stability = 1"],
        (100,),
        "{n}%",
    ),
    Action(
        "stability_zero",
        "nation",
        lambda n: ["set_stability = 0"],
        (0,),
        "{n}%",
        danger=True,
        confirm=True,
    ),
    Action(
        "war_support",
        "nation",
        lambda n: [f"add_war_support = 0.{n:02d}"],
        (5, 10, 25, 50),
        "+{n}%",
    ),
    Action("war_support_full", "nation", lambda n: ["set_war_support = 1"], (100,), "{n}%"),
    Action(
        "war_support_zero",
        "nation",
        lambda n: ["set_war_support = 0"],
        (0,),
        "{n}%",
        danger=True,
        confirm=True,
    ),
    Action(
        "research_slots",
        "nation",
        lambda n: [f"set_research_slots = {n}"],
        (2, 3, 4, 5),
        "{n}",
    ),
    Action("fuel", "nation", lambda n: [f"add_fuel = {n}"], (10_000, 100_000, 500_000, 1_000_000)),
    Action("cic", "nation", lambda n: [f"add_cic = {n}"], (100, 500, 1_000, 5_000)),
    Action(
        "threat",
        "nation",
        lambda n: [f"add_named_threat = {{ threat = {n} name = CCP_THREAT_SOURCE }}"],
        (5, 10, 25, 50),
    ),
    Action(
        "legitimacy",
        "nation",
        lambda n: [f"add_legitimacy = {n}"],
        (10, 25, 50, 100),
    ),
]

# ---------------------------------------------------------------- construction

CONSTRUCTION: list[Action] = [
    Action("infrastructure", "construction", _build("infrastructure"), (1, 2, 3, 5)),
    Action("civilian", "construction", _build("industrial_complex"), (1, 5, 10, 20)),
    Action("military", "construction", _build("arms_factory"), (1, 5, 10, 20)),
    Action(
        "dockyard",
        "construction",
        lambda n: _owned_limited(
            "is_coastal = yes",
            f"add_building_construction = {{ type = dockyard level = {n} instant_build = yes }}",
        ),
        (1, 3, 5, 10),
    ),
    Action("airbase", "construction", _build("air_base"), (1, 5, 10, 20)),
    Action("radar", "construction", _build("radar_station"), (1, 2, 3, 5)),
    Action("antiair", "construction", _build("anti_air_building"), (1, 2, 3, 5)),
    Action("fort", "construction", _build("bunker"), (1, 3, 5, 10)),
    Action(
        "coastal_fort",
        "construction",
        lambda n: _owned_limited(
            "is_coastal = yes",
            f"add_building_construction = {{ type = coastal_bunker level = {n} instant_build = yes }}",
        ),
        (1, 3, 5, 10),
    ),
    Action(
        "supply_hub",
        "construction",
        _build("supply_node"),
        (1,),
    ),
    Action(
        "slots",
        "construction",
        lambda n: _owned(f"add_extra_state_shared_building_slots = {n}"),
        (1, 3, 5, 10),
    ),
    Action(
        "offsite_civilian",
        "construction",
        lambda n: [f"add_offsite_building = {{ type = industrial_complex level = {n} }}"],
        (5, 10, 20, 50),
    ),
    Action(
        "offsite_military",
        "construction",
        lambda n: [f"add_offsite_building = {{ type = arms_factory level = {n} }}"],
        (5, 10, 20, 50),
    ),
    Action(
        "mines",
        "construction",
        lambda n: _owned_limited("is_coastal = yes", f"add_mines = {n}"),
        (10, 25, 50, 100),
    ),
]

# ---------------------------------------------------------------- resources in states

RESOURCES_SECTION: list[Action] = [
    Action(
        f"resource_{name}",
        "stockpile",
        (lambda kind: lambda n: _owned(f"add_resource = {{ type = {kind} amount = {n} }}"))(name),
        (1, 5, 10, 25),
    )
    for name in ("oil", "aluminium", "rubber", "tungsten", "steel", "chromium", "coal")
]

# ---------------------------------------------------------------- politics

POLITICS: list[Action] = [
    Action(
        f"ruling_{ideology}",
        "politics",
        (
            lambda party: lambda n: [
                f"set_politics = {{ ruling_party = {party} elections_allowed = yes }}"
            ]
        )(ideology),
        (1,),
        "SET",
        danger=True,
        confirm=True,
    )
    for ideology in ("democratic", "communism", "fascism", "neutrality")
] + [
    Action(
        f"popularity_{ideology}",
        "politics",
        (
            lambda party: lambda n: [
                f"add_popularity = {{ ideology = {party} popularity = 0.{n:02d} }}"
            ]
        )(ideology),
        (5, 10, 25, 50),
        "+{n}%",
    )
    for ideology in ("democratic", "communism", "fascism", "neutrality")
] + [
    Action(
        "civil_war",
        "politics",
        lambda n: [
            "start_civil_war = {",
            "\tideology = communism",
            f"\tsize = 0.{n:02d}",
            "}",
        ],
        (25, 50, 75),
        "{n}%",
        danger=True,
        confirm=True,
    ),
    Action(
        "autonomy",
        "politics",
        lambda n: [f"add_autonomy_ratio = {{ value = 0.{n:02d} }}"],
        (10, 25, 50),
        "+{n}%",
    ),
    Action(
        "autonomy_down",
        "politics",
        lambda n: [f"add_autonomy_ratio = {{ value = -0.{n:02d} }}"],
        (10, 25, 50),
        "-{n}%",
    ),
]

# ---------------------------------------------------------------- military

MILITARY: list[Action] = [
    Action(
        "nukes",
        "military",
        lambda n: [f"add_nuclear_bombs = {n}"],
        (1, 5, 25, 100),
    ),
    Action(
        "divisions_infantry",
        "military",
        (
            lambda template: lambda n: [
                "CCP_ensure_templates = yes",
                "capital_scope = {",
                f"\tCCP_spawn_{template}_{n} = yes",
                "}",
            ]
        )("infantry"),
        (1, 5, 10, 25),
    ),
    Action(
        "divisions_armor",
        "military",
        (
            lambda template: lambda n: [
                "CCP_ensure_templates = yes",
                "capital_scope = {",
                f"\tCCP_spawn_{template}_{n} = yes",
                "}",
            ]
        )("armor"),
        (1, 5, 10, 25),
    ),
    Action(
        "divisions_motorized",
        "military",
        (
            lambda template: lambda n: [
                "CCP_ensure_templates = yes",
                "capital_scope = {",
                f"\tCCP_spawn_{template}_{n} = yes",
                "}",
            ]
        )("motorized"),
        (1, 5, 10, 25),
    ),
    Action(
        "delete_units",
        "military",
        lambda n: ["every_army_leader = { delete_unit = yes }"],
        (0,),
        "ALL",
        danger=True,
        confirm=True,
    ),
    Action(
        "army_xp",
        "military",
        lambda n: [f"army_experience = {n}"],
        (100, 500, 1_000, 5_000),
    ),
    Action(
        "navy_xp",
        "military",
        lambda n: [f"navy_experience = {n}"],
        (100, 500, 1_000, 5_000),
    ),
    Action(
        "air_xp",
        "military",
        lambda n: [f"air_experience = {n}"],
        (100, 500, 1_000, 5_000),
    ),
]

# ---------------------------------------------------------------- commanders

COMMANDERS: list[Action] = [
    Action("skill", "commanders", _army_leaders("add_skill_level"), (1, 2, 3, 5)),
    Action("attack", "commanders", _army_leaders("add_attack"), (1, 2, 3, 5)),
    Action("defense", "commanders", _army_leaders("add_defense"), (1, 2, 3, 5)),
    Action("planning", "commanders", _army_leaders("add_planning"), (1, 2, 3, 5)),
    Action("logistics", "commanders", _army_leaders("add_logistics"), (1, 2, 3, 5)),
    Action("admiral_skill", "commanders", _navy_leaders("add_skill_level"), (1, 2, 3, 5)),
]

# ---------------------------------------------------------------- research helpers

RESEARCH_TOOLS: list[Action] = [
    Action(
        "research_speed",
        "research_tools",
        lambda n: [
            f"add_timed_idea = {{ idea = ccp_research_boost days = {n} }}",
        ],
        (90, 180, 365, 730),
        "{n}d",
    ),
    Action(
        "doctrine_cost",
        "research_tools",
        lambda n: [f"add_doctrine_cost_reduction = {{ name = ccp_doctrine cost_reduction = 0.{n:02d} uses = 100 category = land_doctrine }}"],
        (50, 75, 99),
        "-{n}%",
    ),
]

BY_SECTION: dict[str, list[Action]] = {
    "nation": NATION,
    "politics": POLITICS,
    "construction": CONSTRUCTION,
    "stockpile": RESOURCES_SECTION,
    "military": MILITARY,
    "commanders": COMMANDERS,
}

ALL: list[Action] = [action for actions in BY_SECTION.values() for action in actions]

# name, line battalions, support companies. Sub-unit identifiers verified against
# common/units in the installed game.
SPAWN_TEMPLATES: dict[str, tuple[str, tuple[tuple[str, int], ...], tuple[str, ...]]] = {
    "infantry": (
        "CCP Infantry",
        (("infantry", 9), ("artillery_brigade", 3)),
        ("engineer", "artillery", "recon"),
    ),
    "armor": (
        "CCP Armor",
        (("medium_armor", 6), ("mechanized", 4)),
        ("engineer", "maintenance_company", "logistics_company"),
    ),
    "motorized": (
        "CCP Motorized",
        (("motorized", 9), ("anti_tank_brigade", 2)),
        ("engineer", "recon", "logistics_company"),
    ),
}

SPAWN_COUNTS = (1, 5, 10, 25)


def level_id(level: int) -> str:
    """A level turned into a script-safe suffix; negatives read as `m`."""
    return f"m{abs(level)}" if level < 0 else str(level)


def action_levels() -> list[tuple[Action, int]]:
    """Every action paired with each of its levels, in a stable order."""
    return [(action, level) for action in ALL for level in action.levels]


def generic_id(action: Action, level: int) -> int:
    """Identifier for an action that goes through the confirmation prompt."""
    confirmable = [pair for pair in action_levels() if pair[0].confirm]
    return confirmable.index((action, level)) + 1
