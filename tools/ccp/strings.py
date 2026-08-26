"""Every hand-authored string the panel shows, in both supported languages.

Keeping them in one table is what guarantees parity: a key cannot exist in one
language and not the other, because there is only one place to add it.
"""

from __future__ import annotations

from .meta import MOD_VERSION
from .sections import HOTKEYS, SECTIONS

LANGUAGES = ("english", "turkish")

CORE: dict[str, tuple[str, str]] = {
    "CCP_TITLE": ("CHEAT CONTROL PANEL", "HİLE KONTROL PANELİ"),
    "CCP_SUBTITLE": (
        "Singleplayer utility for Hearts of Iron IV",
        "Hearts of Iron IV için tek oyunculu yardımcı araç",
    ),
    "CCP_SIDEBAR_HEADING": ("SECTIONS", "BÖLÜMLER"),
    "CCP_BUTTON_CLOSE": ("CLOSE", "KAPAT"),
    "CCP_BUTTON_CANCEL": ("CANCEL", "İPTAL"),
    "CCP_BUTTON_CONFIRM": ("CONFIRM", "ONAYLA"),
    "CCP_TOOLTIP_CLOSE": (
        "Close the panel. The hotkey reopens it at any time.",
        "Paneli kapatır. Kısayol tuşu paneli istediğiniz an yeniden açar.",
    ),
    "CCP_TOOLTIP_LAUNCHER": (
        "Open the Cheat Control Panel.\\nHotkey: [CCP_GetHotkeyName] — change it in Settings.",
        "Cheat Control Panel'i açar.\\nKısayol: [CCP_GetHotkeyName] — Ayarlar'dan değiştirilebilir.",
    ),
    "CCP_FOOTER_HINT": (
        "[CCP_GetHotkeyName] toggles this panel · change the key in Settings",
        "[CCP_GetHotkeyName] bu paneli açar/kapatır · tuşu Ayarlar'dan değiştirin",
    ),
    "CCP_STATUS_IDLE": (
        "Cheat Control Panel {version} · Hearts of Iron IV 1.19 · singleplayer",
        "Cheat Control Panel {version} · Hearts of Iron IV 1.19 · tek oyunculu",
    ),
    "CCP_STATUS_HOTKEY": (
        "Hotkey set to [CCP_GetHotkeyName].",
        "Kısayol [CCP_GetHotkeyName] olarak ayarlandı.",
    ),
    "CCP_STATUS_CONFIRM_ON": (
        "Confirmation prompts are on for destructive actions.",
        "Geri alınamaz işlemler için onay istemi açık.",
    ),
    "CCP_STATUS_CONFIRM_OFF": (
        "Confirmation prompts are off. Destructive actions apply immediately.",
        "Onay istemi kapalı. Geri alınamaz işlemler anında uygulanır.",
    ),
    "CCP_CONFIRM_ON": ("CONFIRMATIONS: ON", "ONAY İSTEMİ: AÇIK"),
    "CCP_CONFIRM_OFF": ("CONFIRMATIONS: OFF", "ONAY İSTEMİ: KAPALI"),
    "CCP_SETTINGS_HOTKEY": ("HOTKEY", "KISAYOL TUŞU"),
    "CCP_SETTINGS_HOTKEY_HELP": (
        "Choose the key that opens and closes this panel. The choice is saved with your game.",
        "Bu paneli açıp kapatan tuşu seçin. Seçim oyununuzla birlikte kaydedilir.",
    ),
    "CCP_SETTINGS_HOTKEY_CURRENT": (
        "Current hotkey: [CCP_GetHotkeyName]",
        "Geçerli kısayol: [CCP_GetHotkeyName]",
    ),
    "CCP_SETTINGS_CONFIRM": ("CONFIRMATIONS", "ONAY İSTEMİ"),
    "CCP_SETTINGS_CONFIRM_HELP": (
        "Destructive actions ask before they apply. There is no undo, so leaving this on is safer.",
        "Geri alınamaz işlemler uygulanmadan önce sorar. Geri alma özelliği yok, açık bırakmak daha güvenlidir.",
    ),
    "CCP_SETTINGS_CONFIRM_TOOLTIP": (
        "Toggle the confirmation prompt shown before annexations, state transfers and core removal.",
        "İlhak, eyalet devri ve core kaldırma öncesi gösterilen onay istemini açıp kapatır.",
    ),
    "CCP_CARD_COUNTRY": ("COUNTRY", "ÜLKE"),
    "CCP_CARD_COUNTRY_VALUE": ("[ROOT.GetNameDefCap]", "[ROOT.GetNameDefCap]"),
    "CCP_CARD_COUNTRY_TOOLTIP": (
        "The country you are currently playing.",
        "Şu anda oynadığınız ülke.",
    ),
    "CCP_CARD_PP": ("POLITICAL POWER", "SİYASİ GÜÇ"),
    "CCP_CARD_PP_VALUE": ("[?political_power|0]", "[?political_power|0]"),
    "CCP_CARD_PP_TOOLTIP": (
        "Political power currently in your treasury.",
        "Hazinenizdeki mevcut siyasi güç.",
    ),
    "CCP_CARD_CP": ("COMMAND POWER", "KOMUTA GÜCÜ"),
    "CCP_CARD_CP_VALUE": ("[?command_power|0]", "[?command_power|0]"),
    "CCP_CARD_CP_TOOLTIP": (
        "Command power available for army abilities.",
        "Ordu yetenekleri için mevcut komuta gücü.",
    ),
    "CCP_CARD_MANPOWER": ("MANPOWER", "İNSAN GÜCÜ"),
    "CCP_CARD_MANPOWER_VALUE": ("[?manpower|0]", "[?manpower|0]"),
    "CCP_CARD_MANPOWER_TOOLTIP": (
        "Manpower available for deployment and reinforcement.",
        "Konuşlandırma ve takviye için mevcut insan gücü.",
    ),
    "CCP_CARD_ARMY_XP": ("ARMY XP", "ORDU TECRÜBESİ"),
    "CCP_CARD_ARMY_XP_VALUE": ("[?army_experience|0]", "[?army_experience|0]"),
    "CCP_CARD_ARMY_XP_TOOLTIP": (
        "Army experience, spent on division templates.",
        "Tümen şablonlarında harcanan ordu tecrübesi.",
    ),
    "CCP_CARD_NAVY_XP": ("NAVY XP", "DONANMA TECRÜBESİ"),
    "CCP_CARD_NAVY_XP_VALUE": ("[?navy_experience|0]", "[?navy_experience|0]"),
    "CCP_CARD_NAVY_XP_TOOLTIP": (
        "Navy experience, spent on ship designs.",
        "Gemi tasarımlarında harcanan donanma tecrübesi.",
    ),
    "CCP_CARD_AIR_XP": ("AIR XP", "HAVA TECRÜBESİ"),
    "CCP_CARD_AIR_XP_VALUE": ("[?air_experience|0]", "[?air_experience|0]"),
    "CCP_CARD_AIR_XP_TOOLTIP": (
        "Air experience, spent on aircraft designs.",
        "Uçak tasarımlarında harcanan hava tecrübesi.",
    ),
    "CCP_CARD_STABILITY": ("STABILITY", "İSTİKRAR"),
    "CCP_CARD_STABILITY_VALUE": ("[?stability|%0]", "[?stability|%0]"),
    "CCP_CARD_STABILITY_TOOLTIP": (
        "National stability.",
        "Ulusal istikrar.",
    ),
    "CCP_CARD_FACTORIES": ("FACTORIES", "FABRİKALAR"),
    "CCP_CARD_FACTORIES_VALUE": (
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] dock",
        "[?num_of_civilian_factories|0] sivil · [?num_of_military_factories|0] askeri · [?num_of_naval_factories|0] tersane",
    ),
    "CCP_CARD_FACTORIES_TOOLTIP": (
        "Civilian factories, military factories and dockyards.",
        "Sivil fabrikalar, askeri fabrikalar ve tersaneler.",
    ),
}

SECTION_TOOLTIPS: dict[str, tuple[str, str]] = {
    "dashboard": (
        "A live summary of the country you are playing.",
        "Oynadığınız ülkenin canlı özeti.",
    ),
    "settings": (
        "Change the hotkey and the confirmation behaviour.",
        "Kısayol tuşunu ve onay davranışını değiştirin.",
    ),
}


def all_strings() -> dict[str, tuple[str, str]]:
    strings = {
        key: tuple(value.format(version=MOD_VERSION) for value in values)
        for key, values in CORE.items()
    }

    for section in SECTIONS:
        strings[section.key] = (section.english, section.turkish)
        tooltip = SECTION_TOOLTIPS.get(section.slug)
        if tooltip is None:
            raise KeyError(f"section `{section.slug}` has no tooltip in SECTION_TOOLTIPS")
        strings[f"{section.key}_TOOLTIP"] = tooltip

    for index, (_, english, turkish) in enumerate(HOTKEYS, start=1):
        strings[f"CCP_HOTKEY_{index}"] = (english, turkish)
        strings[f"CCP_HOTKEY_{index}_TOOLTIP"] = (
            f"Use {english} to open and close the panel.",
            f"Paneli açıp kapatmak için {turkish} tuşunu kullanın.",
        )

    return strings


def emit_localisation(language: str) -> str:
    index = LANGUAGES.index(language)
    lines = [f"l_{language}:"]
    lines += [
        f' {key}:0 "{values[index]}"' for key, values in sorted(all_strings().items())
    ]
    return "\n".join(lines) + "\n"
