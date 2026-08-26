"""Reads the localisation keys the base game defines.

An entry the game cannot name is one the player is not meant to see: legacy
technologies kept for save compatibility, hidden placeholders and the like. The
catalogues filter on this so the panel never shows a raw internal identifier.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

KEY = re.compile(r"^\s*([A-Za-z0-9_.@\-]+):\s*\d*\s*\"", re.MULTILINE)


@lru_cache(maxsize=4)
def english_keys(game_dir: Path) -> frozenset[str]:
    keys: set[str] = set()
    roots = [
        game_dir / "localisation" / "english",
        game_dir / "integrated_dlc",
        game_dir / "dlc",
    ]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*_l_english.yml"):
            keys |= set(KEY.findall(path.read_text(encoding="utf-8-sig", errors="replace")))
    return frozenset(keys)
