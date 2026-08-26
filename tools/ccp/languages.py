"""Which languages the panel ships in, and how each one reaches the player.

Hearts of Iron IV recognises exactly ten localisation folders, listed in the
game's own `localisation/languages.yml`: english, braz_por, french, german,
polish, russian, spanish, japanese, simp_chinese and korean.

**Turkish and Dutch are not among them.** A `localisation/turkish/` folder is
ignored by the engine, so shipping one would be dead weight that never displays.

So the panel ships the requested languages the engine supports as normal
localisation, and delivers the two it does not as overlays: the same strings
written into the `english` folder, which `tools/set_panel_language.py` installs
on request. That is how Turkish translations for this game are distributed
generally, and it composes with a Turkish game patch rather than fighting it.
"""

from __future__ import annotations

NATIVE = ("english", "german", "french", "russian")
OVERLAY = ("turkish", "dutch")

ALL = NATIVE + OVERLAY

DISPLAY_NAMES = {
    "english": "English",
    "german": "Deutsch",
    "french": "Français",
    "russian": "Русский",
    "turkish": "Türkçe",
    "dutch": "Nederlands",
}
