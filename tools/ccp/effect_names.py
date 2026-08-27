"""The set of effects the game defines, read from its own documentation.

Used by the release checklist so a typo or a renamed effect is caught at build
time rather than by a button that silently does nothing in game.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

HEADING = re.compile(r"^## ([a-z_][a-z0-9_]*)$", re.MULTILINE)

# Written by the panel itself or provided by the engine as scopes and keywords
# rather than as effects.
# Keys from the scripted GUI schema and from `set_rule`, neither of which is an
# effect but both of which appear on the left of an assignment.
GUI_AND_RULE_KEYS = frozenset(
    {
        "context_type",
        "window_name",
        "parent_window_token",
        "parent_window_window",
        "parent_scripted_gui",
        "visible",
        "effects",
        "triggers",
        "properties",
        "dynamic_lists",
        "dirty",
        "entry_container",
        "change_scope",
        "index",
        "scripted_gui",
        "ai_enabled",
        "ai_check",
        "ai_weights",
        "map_mode",
        "frame",
        "image",
        "x",
        "y",
        "can_create_factions",
        "can_join_factions",
        "can_declare_war_on_same_ideology",
        "can_guarantee_other_ideologies",
        "can_puppet",
        "can_send_volunteers",
        "can_boost_other_ideologies",
        "can_access_market",
        "can_create_collaboration_government",
        "can_not_declare_war",
        "can_use_kamikaze_pilots",
        "can_generate_female_aces",
        "desc",
        # scripted localisation and opinion modifier schemas
        "defined_text",
        "localization_key",
        "text",
        "trigger",
        "opinion_modifiers",
        "trade",
        "decay",
        "days",
        "months",
        "years",
    }
)

SCOPES_AND_KEYWORDS = frozenset(
    {
        "if",
        "else",
        "else_if",
        "limit",
        "hidden_effect",
        "random",
        "while_loop_effect",
        "for_loop_effect",
        "capital_scope",
        "owner",
        "controller",
        "every_owned_state",
        "every_state",
        "every_country",
        "every_army_leader",
        "every_navy_leader",
        "every_unit_leader",
        "division",
        "regiments",
        "support",
        "name",
        "value",
        "array",
        "var",
        "type",
        "target",
        "amount",
        "level",
        "days",
        "size",
        "ideology",
        "ruling_party",
        "elections_allowed",
        "popularity",
        "instant_build",
        "disband",
        "start",
        "end",
        "min",
        "max",
        "threat",
        "civilian_intel",
        "army_intel",
        "navy_intel",
        "airforce_intel",
        "modifier",
        "region",
        "state",
        "id",
        "popup",
        "cost_reduction",
        "uses",
        "category",
        "idea",
        "always",
    }
)


@lru_cache(maxsize=2)
def known_identifiers(game_dir: Path) -> frozenset[str]:
    """Names that are game data rather than effects.

    A technology key inside `set_technology`, a sub-unit inside a division
    template and a building type inside `add_building_construction` all look like
    assignments, so the vocabulary check needs to know they are legitimate.
    """
    from .equipment import load_catalogue as load_equipment
    from .technology import load_catalogue as load_technologies

    names: set[str] = set()
    names |= {item.key for item in load_technologies(game_dir)}
    names |= {item.key for item in load_equipment(game_dir)}
    names |= {"oil", "aluminium", "rubber", "tungsten", "steel", "chromium", "coal"}
    names |= {"democratic", "communism", "fascism", "neutrality"}

    units = game_dir / "common" / "units"
    if units.is_dir():
        depth_pattern = re.compile(r"^\s*([a-z_]+)\s*=\s*\{")
        for path in units.glob("*.txt"):
            depth = 0
            for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                match = depth_pattern.match(line)
                if depth == 1 and match:
                    names.add(match.group(1))
                depth += line.count("{") - line.count("}")

    buildings = game_dir / "common" / "buildings"
    if buildings.is_dir():
        for path in buildings.glob("*.txt"):
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            names |= set(re.findall(r"^		([a-z_]+)\s*=\s*\{", text, re.MULTILINE))

    return frozenset(names)


@lru_cache(maxsize=2)
def known_effects(game_dir: Path) -> frozenset[str]:
    path = game_dir / "documentation" / "effects_documentation.md"
    if not path.is_file():
        return frozenset()
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    effects = frozenset(HEADING.findall(text))

    triggers_path = game_dir / "documentation" / "triggers_documentation.md"
    triggers = frozenset()
    if triggers_path.is_file():
        triggers = frozenset(
            HEADING.findall(triggers_path.read_text(encoding="utf-8-sig", errors="replace"))
        )

    return (
        effects
        | triggers
        | SCOPES_AND_KEYWORDS
        | GUI_AND_RULE_KEYS
        | known_identifiers(game_dir)
    )
