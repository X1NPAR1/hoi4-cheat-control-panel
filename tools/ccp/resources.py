"""The resources the panel can grant, and the effect that grants each one.

`effect` is the native scripted effect verified against the game's own
`effects_documentation.md`. `safe_max` is the largest single grant the panel
offers, chosen to stay well inside what the game handles rather than to be
the largest number that fits.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    slug: str
    english: str
    turkish: str
    effect: str
    variable: str
    presets: tuple[int, ...]
    safe_max: int
    english_help: str
    turkish_help: str

    @property
    def key(self) -> str:
        return f"CCP_RES_{self.slug.upper()}"


RESOURCES: list[Resource] = [
    Resource(
        "political_power",
        "Political Power",
        "Siyasi Güç",
        "add_political_power",
        "political_power",
        (100, 500, 1000, 5000),
        1_000_000,
        "Spent on advisors, laws and decisions.",
        "Danışmanlar, yasalar ve kararlar için harcanır.",
    ),
    Resource(
        "command_power",
        "Command Power",
        "Komuta Gücü",
        "add_command_power",
        "command_power",
        (10, 25, 50, 100),
        100,
        "Spent on army abilities. The game caps command power at 100, so larger grants are wasted.",
        "Ordu yetenekleri için harcanır. Oyun komuta gücünü 100 ile sınırlar, fazlası boşa gider.",
    ),
    Resource(
        "manpower",
        "Manpower",
        "İnsan Gücü",
        "add_manpower",
        "manpower",
        (10_000, 100_000, 1_000_000, 5_000_000),
        50_000_000,
        "Used to deploy and reinforce divisions.",
        "Tümen konuşlandırmak ve takviye etmek için kullanılır.",
    ),
    Resource(
        "army_experience",
        "Army Experience",
        "Ordu Tecrübesi",
        "army_experience",
        "army_experience",
        (10, 50, 100, 500),
        100_000,
        "Spent on division templates.",
        "Tümen şablonlarında harcanır.",
    ),
    Resource(
        "navy_experience",
        "Navy Experience",
        "Donanma Tecrübesi",
        "navy_experience",
        "navy_experience",
        (10, 50, 100, 500),
        100_000,
        "Spent on ship designs.",
        "Gemi tasarımlarında harcanır.",
    ),
    Resource(
        "air_experience",
        "Air Experience",
        "Hava Tecrübesi",
        "air_experience",
        "air_experience",
        (10, 50, 100, 500),
        100_000,
        "Spent on aircraft designs.",
        "Uçak tasarımlarında harcanır.",
    ),
]

AMOUNT_MAX = 50_000_000


def preset_label(amount: int) -> str:
    if amount >= 1_000_000 and amount % 1_000_000 == 0:
        return f"+{amount // 1_000_000}M"
    if amount >= 1_000 and amount % 1_000 == 0:
        return f"+{amount // 1_000}K"
    return f"+{amount}"
