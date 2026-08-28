"""Which languages the panel ships in.

Hearts of Iron IV recognises exactly ten localisation folders, listed in the
game's own `localisation/languages.yml`: english, braz_por, french, german,
polish, russian, spanish, japanese, simp_chinese and korean.

Turkish and Dutch are not among them, so they cannot be shipped as languages.
They used to travel as an overlay written into the `english` folder, and that
was a mistake: the overlay reached the Workshop once and gave every English
subscriber Turkish menus. There is no way to offer those languages that the
engine will keep separate from English, so the panel does not offer them.
"""

from __future__ import annotations

NATIVE = ("english", "german", "french", "russian")

ALL = NATIVE

DISPLAY_NAMES = {
    "english": "English",
    "german": "Deutsch",
    "french": "Français",
    "russian": "Русский",
}
