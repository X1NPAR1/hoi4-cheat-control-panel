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

from dataclasses import dataclass
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


# Forts, coastal forts and supply hubs are province buildings. Without a province
# block the engine refuses add_building_construction without a word, which is why
# those three cards did nothing. The province options are the game's own.
def _build_provincial(
    kind: str, province: str, state_limit: str | None = None
) -> Callable[[int], list[str]]:
    def body(n: int) -> list[str]:
        effect = (
            f"add_building_construction = {{ type = {kind} level = {n} "
            f"instant_build = yes province = {{ {province} }} }}"
        )
        if state_limit:
            return _owned_limited(state_limit, effect)
        return _owned(effect)

    return body


def _railway(n: int) -> list[str]:
    """Rail from the capital to every owned state, as the game's own SOV script does."""
    return [
        "capital_scope = { set_variable = { ROOT.ccp_rail_from = THIS.id } }",
        "every_owned_state = {",
        "\tset_variable = { ROOT.ccp_rail_to = THIS.id }",
        "\tROOT = {",
        "\t\tbuild_railway = {",
        f"\t\t\tlevel = {n}",
        "\t\t\tfallback = yes",
        "\t\t\tstart_state = var:ROOT.ccp_rail_from",
        "\t\t\ttarget_state = var:ROOT.ccp_rail_to",
        "\t\t}",
        "\t}",
        "}",
    ]


def _spawn_in_state(template: str) -> Callable[[int], list[str]]:
    """Divisions raised in the state last picked, not in the capital.

    create_unit run from a state scope places the division in that state -- the
    game's own TOA and Paraguay scripts rely on it -- and owner = PREV is the
    country that stepped in.
    """
    return lambda n: [
        "CCP_ensure_templates = yes",
        "var:ccp_state = {",
        f"\tCCP_spawn_{template}_{n} = yes",
        "}",
    ]


def _dlc(dlc: str, lines: list[str]) -> list[str]:
    return ["if = {", f'	limit = {{ has_dlc = "{dlc}" }}', *[f"	{line}" for line in lines], "}"]


def _tech_bonus(category: str) -> Callable[[int], list[str]]:
    return lambda n: [
        "add_tech_bonus = {",
        f"	name = ccp_{category}_bonus",
        "	bonus = 1.0",
        f"	uses = {n}",
        f"	category = {category}",
        "}",
    ]


def _free_doctrines(n: int) -> list[str]:
    return [
        line
        for category in ("land_doctrine", "air_doctrine", "naval_doctrine")
        for line in (
            "add_doctrine_cost_reduction = {",
            f"	name = ccp_{category}_free",
            "	cost_reduction = 1.0",
            f"	uses = {n}",
            f"	category = {category}",
            "}",
        )
    ]


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
        (1, 2, 5, 10),
    ),
    Action(
        "legitimacy",
        "nation",
        lambda n: [f"add_legitimacy = {n}"],
        (10, 25, 50, 100),
    ),
]

# ---------------------------------------------------------------- construction

RESEARCH_SPEED: list[Action] = [
    Action("research_bonus", "nation", _tech_bonus("industry"), (1, 3, 5, 10), "x{n}"),
    # add_doctrine_cost_reduction is what reaches the doctrine trees. set_technology
    # does not, which is why the README listed doctrines as out of reach; a full
    # cost reduction makes the next N doctrines free instead.
    Action("doctrines_free", "nation", _free_doctrines, (1, 5, 10, 25), "{n}"),
    Action(
        "occupation_harsh",
        "nation",
        lambda n: _dlc("La Resistance", ["set_occupation_law = military_governor_occupation"]),
        (1,),
        "SET",
        danger=True,
    ),
    Action(
        "occupation_soft",
        "nation",
        lambda n: _dlc("La Resistance", ["set_occupation_law = local_police_force_garrison"]),
        (1,),
        "SET",
    ),
]


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
    Action(
        "fort",
        "construction",
        _build_provincial("bunker", "all_provinces = yes"),
        (1, 3, 5, 10),
    ),
    Action(
        "coastal_fort",
        "construction",
        _build_provincial(
            "coastal_bunker", "all_provinces = yes limit_to_coastal = yes", "is_coastal = yes"
        ),
        (1, 3, 5, 10),
    ),
    Action(
        "supply_hub",
        "construction",
        _build_provincial("supply_node", "all_provinces = yes limit_to_victory_point = yes"),
        (1,),
    ),
    Action("railway", "construction", _railway, (1, 2, 3, 5)),
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
    Action("state_infantry", "military", _spawn_in_state("infantry"), (1, 5, 10, 25)),
    Action("state_armor", "military", _spawn_in_state("armor"), (1, 5, 10, 25)),
    Action("state_motorized", "military", _spawn_in_state("motorized"), (1, 5, 10, 25)),
    Action(
        "delete_units",
        "military",
        lambda n: ["delete_unit = { disband = yes }"],
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

# ---------------------------------------------------------------- diplomacy

DIPLOMACY: list[Action] = [
    Action(
        "opinion_up",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            "	add_opinion_modifier = { target = ROOT modifier = ccp_goodwill }",
            "}",
        ],
        (1,),
        "SET",
    ),
    Action(
        "opinion_down",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            "	add_opinion_modifier = { target = ROOT modifier = ccp_distrust }",
            "}",
        ],
        (1,),
        "SET",
    ),
    Action(
        "intel",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            "	ROOT = {",
            "		add_intel = {",
            "			target = PREV",
            f"			civilian_intel = {n}",
            f"			army_intel = {n}",
            f"			navy_intel = {n}",
            f"			airforce_intel = {n}",
            "		}",
            "	}",
            "}",
        ],
        (25, 50, 75, 100),
        "{n}%",
    ),
    Action(
        "wargoal",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            "	ROOT = { create_wargoal = { type = annex_everything target = PREV } }",
            "}",
        ],
        (1,),
        "SET",
    ),
    Action(
        "truce",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            f"	ROOT = {{ set_truce = {{ target = PREV days = {n} }} }}",
            "}",
        ],
        (90, 180, 365, 730),
        "{n}d",
    ),
    Action(
        "faction_create",
        "diplomacy",
        lambda n: ["create_faction = CCP_FACTION_NAME"],
        (1,),
        "SET",
    ),
    Action(
        "faction_invite",
        "diplomacy",
        lambda n: ["var:ccp_target_country = { ROOT = { add_to_faction = PREV } }"],
        (1,),
        "SET",
    ),
    Action(
        "release_target",
        "diplomacy",
        lambda n: ["var:ccp_target_country = { ROOT = { release = PREV } }"],
        (1,),
        "SET",
        danger=True,
        confirm=True,
    ),
    Action(
        "free_target",
        "diplomacy",
        lambda n: ["var:ccp_target_country = { ROOT = { end_puppet = PREV } }"],
        (1,),
        "SET",
        danger=True,
        confirm=True,
    ),
]

DIPLOMACY += [
    Action(
        "collaboration",
        "diplomacy",
        lambda n: [
            "var:ccp_target_country = {",
            "	ROOT = {",
            "		add_collaboration = {",
            "			target = PREV",
            f"			value = 0.{n:02d}",
            "		}",
            "	}",
            "}",
        ],
        (10, 25, 50, 90),
        "+{n}%",
    ),
    Action(
        "guarantee",
        "diplomacy",
        lambda n: ["var:ccp_target_country = { ROOT = { give_guarantee = PREV } }"],
        (1,),
        "SET",
    ),
    Action(
        "disband_target",
        "diplomacy",
        lambda n: ["var:ccp_target_country = { delete_unit = { disband = no } }"],
        (0,),
        "ALL",
        danger=True,
        confirm=True,
    ),
]

BY_SECTION: dict[str, list[Action]] = {
    "nation": NATION + RESEARCH_SPEED,
    "politics": POLITICS,
    "construction": CONSTRUCTION,
    "stockpile": RESOURCES_SECTION,
    "military": MILITARY,
    "commanders": COMMANDERS,
    "diplomacy": DIPLOMACY,
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
