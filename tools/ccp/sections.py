"""The panel's navigation registry.

One list drives the sidebar, the section router, the scripted localisation for
the content heading and the localisation keys, so a section cannot exist in the
sidebar without a destination or a name.

Sections are added here as each phase implements them. Nothing is listed before
it does something.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    slug: str
    english: str
    turkish: str

    @property
    def key(self) -> str:
        return f"CCP_SECTION_{self.slug.upper()}"

    @property
    def window(self) -> str:
        return f"ccp_section_{self.slug}"


SECTIONS: list[Section] = [
    Section("dashboard", "Dashboard", "Genel Bakış"),
    Section("settings", "Settings", "Ayarlar"),
]


def section_id(slug: str) -> int:
    for index, section in enumerate(SECTIONS, start=1):
        if section.slug == slug:
            return index
    raise KeyError(slug)


HOTKEYS = [
    ("INSERT", "Insert", "Insert"),
    ("F11", "F11", "F11"),
    ("F12", "F12", "F12"),
    ("ctrl+F8", "Ctrl+F8", "Ctrl+F8"),
    ("F8", "F8 (shared with the map mode)", "F8 (harita moduyla ortak)"),
]
