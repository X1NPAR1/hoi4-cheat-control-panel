"""Every hand-authored string the panel shows, in all six supported languages.

Keeping them in one table is what guarantees parity: a key cannot exist in one
language and not another, because there is only one place to add it, and
`all_strings` refuses to return a table with a gap in it.

`NEUTRAL` holds keys whose value is the same everywhere — digits and
localisation format strings. They are written once rather than repeated six times.
"""

from __future__ import annotations

from .languages import ALL
from .meta import MOD_VERSION
from .resources import RESOURCES, preset_label
from .sections import HOTKEYS, SECTIONS

Row = dict[str, str]


def _row(english: str, german: str, french: str, russian: str, turkish: str, dutch: str) -> Row:
    return {
        "english": english,
        "german": german,
        "french": french,
        "russian": russian,
        "turkish": turkish,
        "dutch": dutch,
    }


NEUTRAL: dict[str, str] = {
    "CCP_CARD_COUNTRY_VALUE": "[ROOT.GetNameDefCap]",
    "CCP_CARD_PP_VALUE": "[?political_power|0]",
    "CCP_CARD_CP_VALUE": "[?command_power|0]",
    "CCP_CARD_MANPOWER_VALUE": "[?manpower|0]",
    "CCP_CARD_ARMY_XP_VALUE": "[?army_experience|0]",
    "CCP_CARD_NAVY_XP_VALUE": "[?navy_experience|0]",
    "CCP_CARD_AIR_XP_VALUE": "[?air_experience|0]",
    "CCP_CARD_STABILITY_VALUE": "[?stability|%0]",
    "CCP_PAD_VALUE": "[?ccp_amount|0]",
}

TRANSLATED: dict[str, Row] = {
    "CCP_TITLE": _row(
        "CHEAT CONTROL PANEL",
        "CHEAT-KONTROLLPANEL",
        "PANNEAU DE TRICHE",
        "ПАНЕЛЬ УПРАВЛЕНИЯ ЧИТАМИ",
        "HİLE KONTROL PANELİ",
        "CHEAT-BEDIENINGSPANEEL",
    ),
    "CCP_SUBTITLE": _row(
        "Singleplayer utility for Hearts of Iron IV",
        "Einzelspieler-Werkzeug für Hearts of Iron IV",
        "Utilitaire solo pour Hearts of Iron IV",
        "Инструмент для одиночной игры в Hearts of Iron IV",
        "Hearts of Iron IV için tek oyunculu yardımcı araç",
        "Singleplayer-hulpmiddel voor Hearts of Iron IV",
    ),
    "CCP_SIDEBAR_HEADING": _row(
        "SECTIONS", "BEREICHE", "SECTIONS", "РАЗДЕЛЫ", "BÖLÜMLER", "SECTIES"
    ),
    "CCP_BUTTON_CLOSE": _row(
        "CLOSE", "SCHLIESSEN", "FERMER", "ЗАКРЫТЬ", "KAPAT", "SLUITEN"
    ),
    "CCP_BUTTON_CANCEL": _row(
        "CANCEL", "ABBRECHEN", "ANNULER", "ОТМЕНА", "İPTAL", "ANNULEREN"
    ),
    "CCP_BUTTON_CONFIRM": _row(
        "CONFIRM", "BESTÄTIGEN", "CONFIRMER", "ПОДТВЕРДИТЬ", "ONAYLA", "BEVESTIGEN"
    ),
    "CCP_BUTTON_CUSTOM": _row(
        "CUSTOM", "EIGENER", "PERSO", "СВОЁ", "ÖZEL", "EIGEN"
    ),
    "CCP_TOOLTIP_CLOSE": _row(
        "Close the panel. The hotkey reopens it at any time.",
        "Schließt das Panel. Die Taste öffnet es jederzeit wieder.",
        "Ferme le panneau. Le raccourci le rouvre à tout moment.",
        "Закрывает панель. Горячая клавиша откроет её снова.",
        "Paneli kapatır. Kısayol tuşu paneli istediğiniz an yeniden açar.",
        "Sluit het paneel. De sneltoets opent het weer.",
    ),
    "CCP_TOOLTIP_LAUNCHER": _row(
        "Open the Cheat Control Panel.\\nHotkey: [CCP_GetHotkeyName] — change it in Settings.",
        "Öffnet das Cheat-Kontrollpanel.\\nTaste: [CCP_GetHotkeyName] — änderbar unter Einstellungen.",
        "Ouvre le panneau de triche.\\nRaccourci : [CCP_GetHotkeyName] — modifiable dans Paramètres.",
        "Открывает панель управления читами.\\nКлавиша: [CCP_GetHotkeyName] — меняется в настройках.",
        "Cheat Control Panel'i açar.\\nKısayol: [CCP_GetHotkeyName] — Ayarlar'dan değiştirilebilir.",
        "Opent het cheat-bedieningspaneel.\\nSneltoets: [CCP_GetHotkeyName] — aanpasbaar bij Instellingen.",
    ),
    "CCP_FOOTER_HINT": _row(
        "[CCP_GetHotkeyName] toggles this panel · change the key in Settings",
        "[CCP_GetHotkeyName] schaltet dieses Panel um · Taste unter Einstellungen",
        "[CCP_GetHotkeyName] ouvre et ferme ce panneau · touche modifiable dans Paramètres",
        "[CCP_GetHotkeyName] открывает и закрывает панель · клавиша меняется в настройках",
        "[CCP_GetHotkeyName] bu paneli açar/kapatır · tuşu Ayarlar'dan değiştirin",
        "[CCP_GetHotkeyName] schakelt dit paneel · toets aanpasbaar bij Instellingen",
    ),
    "CCP_STATUS_IDLE": _row(
        f"Cheat Control Panel {MOD_VERSION} · Hearts of Iron IV 1.19 · singleplayer",
        f"Cheat-Kontrollpanel {MOD_VERSION} · Hearts of Iron IV 1.19 · Einzelspieler",
        f"Panneau de triche {MOD_VERSION} · Hearts of Iron IV 1.19 · solo",
        f"Панель управления читами {MOD_VERSION} · Hearts of Iron IV 1.19 · одиночная игра",
        f"Cheat Control Panel {MOD_VERSION} · Hearts of Iron IV 1.19 · tek oyunculu",
        f"Cheat-bedieningspaneel {MOD_VERSION} · Hearts of Iron IV 1.19 · singleplayer",
    ),
    "CCP_STATUS_HOTKEY": _row(
        "Hotkey set to [CCP_GetHotkeyName].",
        "Taste auf [CCP_GetHotkeyName] gesetzt.",
        "Raccourci défini sur [CCP_GetHotkeyName].",
        "Горячая клавиша: [CCP_GetHotkeyName].",
        "Kısayol [CCP_GetHotkeyName] olarak ayarlandı.",
        "Sneltoets ingesteld op [CCP_GetHotkeyName].",
    ),
    "CCP_STATUS_GRANTED": _row(
        "Granted [?ccp_granted_amount|0] [CCP_GetGrantedResource].",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] hinzugefügt.",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] ajouté.",
        "Добавлено: [?ccp_granted_amount|0] [CCP_GetGrantedResource].",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] eklendi.",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] toegevoegd.",
    ),
    "CCP_STATUS_CONFIRM_ON": _row(
        "Confirmation prompts are on for destructive actions.",
        "Bestätigungen für unumkehrbare Aktionen sind aktiv.",
        "Les confirmations sont actives pour les actions irréversibles.",
        "Подтверждение необратимых действий включено.",
        "Geri alınamaz işlemler için onay istemi açık.",
        "Bevestigingen staan aan voor onomkeerbare acties.",
    ),
    "CCP_STATUS_CONFIRM_OFF": _row(
        "Confirmation prompts are off. Destructive actions apply immediately.",
        "Bestätigungen sind aus. Unumkehrbare Aktionen wirken sofort.",
        "Les confirmations sont désactivées. Les actions irréversibles s'appliquent aussitôt.",
        "Подтверждение выключено. Необратимые действия применяются сразу.",
        "Onay istemi kapalı. Geri alınamaz işlemler anında uygulanır.",
        "Bevestigingen staan uit. Onomkeerbare acties worden meteen toegepast.",
    ),
    "CCP_CONFIRM_ON": _row(
        "CONFIRMATIONS: ON",
        "BESTÄTIGUNGEN: AN",
        "CONFIRMATIONS : ACTIVÉES",
        "ПОДТВЕРЖДЕНИЕ: ВКЛ",
        "ONAY İSTEMİ: AÇIK",
        "BEVESTIGINGEN: AAN",
    ),
    "CCP_CONFIRM_OFF": _row(
        "CONFIRMATIONS: OFF",
        "BESTÄTIGUNGEN: AUS",
        "CONFIRMATIONS : DÉSACTIVÉES",
        "ПОДТВЕРЖДЕНИЕ: ВЫКЛ",
        "ONAY İSTEMİ: KAPALI",
        "BEVESTIGINGEN: UIT",
    ),
    "CCP_SETTINGS_HOTKEY": _row(
        "HOTKEY", "TASTENKÜRZEL", "RACCOURCI", "ГОРЯЧАЯ КЛАВИША", "KISAYOL TUŞU", "SNELTOETS"
    ),
    "CCP_SETTINGS_HOTKEY_HELP": _row(
        "Choose the key that opens and closes this panel. The choice is saved with your game.",
        "Wählen Sie die Taste, die dieses Panel öffnet und schließt. Die Wahl wird im Spielstand gespeichert.",
        "Choisissez la touche qui ouvre et ferme ce panneau. Le choix est enregistré dans la partie.",
        "Выберите клавишу для открытия и закрытия панели. Выбор сохраняется вместе с игрой.",
        "Bu paneli açıp kapatan tuşu seçin. Seçim oyununuzla birlikte kaydedilir.",
        "Kies de toets die dit paneel opent en sluit. De keuze wordt met je spel opgeslagen.",
    ),
    "CCP_SETTINGS_HOTKEY_CURRENT": _row(
        "Current hotkey: [CCP_GetHotkeyName]",
        "Aktuelle Taste: [CCP_GetHotkeyName]",
        "Raccourci actuel : [CCP_GetHotkeyName]",
        "Текущая клавиша: [CCP_GetHotkeyName]",
        "Geçerli kısayol: [CCP_GetHotkeyName]",
        "Huidige sneltoets: [CCP_GetHotkeyName]",
    ),
    "CCP_SETTINGS_CONFIRM": _row(
        "CONFIRMATIONS",
        "BESTÄTIGUNGEN",
        "CONFIRMATIONS",
        "ПОДТВЕРЖДЕНИЕ",
        "ONAY İSTEMİ",
        "BEVESTIGINGEN",
    ),
    "CCP_SETTINGS_CONFIRM_HELP": _row(
        "Destructive actions ask before they apply. There is no undo, so leaving this on is safer.",
        "Unumkehrbare Aktionen fragen vorher nach. Es gibt kein Rückgängig, daher ist Anlassen sicherer.",
        "Les actions irréversibles demandent confirmation. Il n'y a pas d'annulation, mieux vaut les laisser actives.",
        "Необратимые действия запрашивают подтверждение. Отмены нет, поэтому безопаснее оставить включённым.",
        "Geri alınamaz işlemler uygulanmadan önce sorar. Geri alma özelliği yok, açık bırakmak daha güvenlidir.",
        "Onomkeerbare acties vragen eerst om bevestiging. Er is geen ongedaan maken, dus aan laten is veiliger.",
    ),
    "CCP_SETTINGS_CONFIRM_TOOLTIP": _row(
        "Toggle the confirmation prompt shown before annexations, state transfers and core removal.",
        "Schaltet die Bestätigung vor Annexionen, Staatsübergaben und dem Entfernen von Kerngebieten um.",
        "Active ou désactive la confirmation avant annexions, transferts d'État et retraits de territoire national.",
        "Включает подтверждение перед аннексией, передачей провинций и снятием коренных территорий.",
        "İlhak, eyalet devri ve core kaldırma öncesi gösterilen onay istemini açıp kapatır.",
        "Schakelt de bevestiging vóór annexaties, staatsoverdrachten en het verwijderen van kerngebied.",
    ),
    "CCP_SETTINGS_LANGUAGE": _row(
        "LANGUAGE", "SPRACHE", "LANGUE", "ЯЗЫК", "DİL", "TAAL"
    ),
    "CCP_SETTINGS_LANGUAGE_HELP": _row(
        "The panel follows the game language. English, German, French and Russian ship with the mod. Hearts of Iron IV has no Turkish or Dutch language slot, so those two are installed as an overlay — see the README.",
        "Das Panel folgt der Spielsprache. Englisch, Deutsch, Französisch und Russisch sind enthalten. Hearts of Iron IV hat keinen türkischen oder niederländischen Sprachplatz, daher werden diese beiden als Overlay installiert — siehe README.",
        "Le panneau suit la langue du jeu. Anglais, allemand, français et russe sont inclus. Hearts of Iron IV n'a pas d'emplacement turc ou néerlandais : ces deux langues s'installent en surcouche — voir le README.",
        "Панель следует языку игры. Английский, немецкий, французский и русский входят в мод. В Hearts of Iron IV нет турецкого и нидерландского, поэтому они ставятся наложением — см. README.",
        "Panel oyunun dilini takip eder. İngilizce, Almanca, Fransızca ve Rusça mod ile birlikte gelir. Hearts of Iron IV'te Türkçe ve Felemenkçe dil yuvası yok, bu ikisi kaplama olarak kurulur — README'ye bakın.",
        "Het paneel volgt de speltaal. Engels, Duits, Frans en Russisch zitten in de mod. Hearts of Iron IV heeft geen Turkse of Nederlandse taalsleuf, dus die twee worden als overlay geïnstalleerd — zie de README.",
    ),
    "CCP_CARD_COUNTRY": _row("COUNTRY", "LAND", "PAYS", "СТРАНА", "ÜLKE", "LAND"),
    "CCP_CARD_COUNTRY_TOOLTIP": _row(
        "The country you are currently playing.",
        "Das Land, das Sie gerade spielen.",
        "Le pays que vous jouez actuellement.",
        "Страна, за которую вы играете.",
        "Şu anda oynadığınız ülke.",
        "Het land dat je nu speelt.",
    ),
    "CCP_CARD_PP": _row(
        "POLITICAL POWER", "POLITISCHE MACHT", "POUVOIR POLITIQUE",
        "ПОЛИТИЧЕСКАЯ СИЛА", "SİYASİ GÜÇ", "POLITIEKE MACHT",
    ),
    "CCP_CARD_PP_TOOLTIP": _row(
        "Political power currently in your treasury.",
        "Aktuell verfügbare politische Macht.",
        "Pouvoir politique actuellement disponible.",
        "Доступная политическая сила.",
        "Hazinenizdeki mevcut siyasi güç.",
        "Beschikbare politieke macht.",
    ),
    "CCP_CARD_CP": _row(
        "COMMAND POWER", "KOMMANDOPUNKTE", "POINTS DE COMMANDEMENT",
        "ОЧКИ КОМАНДОВАНИЯ", "KOMUTA GÜCÜ", "COMMANDOPUNTEN",
    ),
    "CCP_CARD_CP_TOOLTIP": _row(
        "Command power available for army abilities.",
        "Kommandopunkte für Armeefähigkeiten.",
        "Points de commandement disponibles pour les capacités d'armée.",
        "Очки командования для армейских способностей.",
        "Ordu yetenekleri için mevcut komuta gücü.",
        "Commandopunten voor legervaardigheden.",
    ),
    "CCP_CARD_MANPOWER": _row(
        "MANPOWER", "REKRUTEN", "EFFECTIFS", "ЛЮДСКИЕ РЕСУРСЫ", "İNSAN GÜCÜ", "MANSCHAPPEN"
    ),
    "CCP_CARD_MANPOWER_TOOLTIP": _row(
        "Manpower available for deployment and reinforcement.",
        "Verfügbare Rekruten für Aufstellung und Verstärkung.",
        "Effectifs disponibles pour le déploiement et le renfort.",
        "Людские ресурсы для развёртывания и пополнения.",
        "Konuşlandırma ve takviye için mevcut insan gücü.",
        "Manschappen voor inzet en aanvulling.",
    ),
    "CCP_CARD_ARMY_XP": _row(
        "ARMY XP", "HEERES-EP", "XP TERRESTRE", "ОПЫТ АРМИИ", "ORDU TECRÜBESİ", "LEGER-XP"
    ),
    "CCP_CARD_ARMY_XP_TOOLTIP": _row(
        "Army experience, spent on division templates.",
        "Heereserfahrung, für Divisionsvorlagen.",
        "Expérience terrestre, dépensée sur les modèles de division.",
        "Опыт армии, тратится на шаблоны дивизий.",
        "Tümen şablonlarında harcanan ordu tecrübesi.",
        "Legerervaring, besteed aan divisiesjablonen.",
    ),
    "CCP_CARD_NAVY_XP": _row(
        "NAVY XP", "MARINE-EP", "XP NAVALE", "ОПЫТ ФЛОТА", "DONANMA TECRÜBESİ", "MARINE-XP"
    ),
    "CCP_CARD_NAVY_XP_TOOLTIP": _row(
        "Navy experience, spent on ship designs.",
        "Marineerfahrung, für Schiffsentwürfe.",
        "Expérience navale, dépensée sur les modèles de navire.",
        "Опыт флота, тратится на проекты кораблей.",
        "Gemi tasarımlarında harcanan donanma tecrübesi.",
        "Marine-ervaring, besteed aan scheepsontwerpen.",
    ),
    "CCP_CARD_AIR_XP": _row(
        "AIR XP", "LUFTWAFFEN-EP", "XP AÉRIENNE", "ОПЫТ АВИАЦИИ", "HAVA TECRÜBESİ", "LUCHTMACHT-XP"
    ),
    "CCP_CARD_AIR_XP_TOOLTIP": _row(
        "Air experience, spent on aircraft designs.",
        "Luftwaffenerfahrung, für Flugzeugentwürfe.",
        "Expérience aérienne, dépensée sur les modèles d'avion.",
        "Опыт авиации, тратится на проекты самолётов.",
        "Uçak tasarımlarında harcanan hava tecrübesi.",
        "Luchtmachtervaring, besteed aan vliegtuigontwerpen.",
    ),
    "CCP_CARD_STABILITY": _row(
        "STABILITY", "STABILITÄT", "STABILITÉ", "СТАБИЛЬНОСТЬ", "İSTİKRAR", "STABILITEIT"
    ),
    "CCP_CARD_STABILITY_TOOLTIP": _row(
        "National stability.",
        "Nationale Stabilität.",
        "Stabilité nationale.",
        "Стабильность страны.",
        "Ulusal istikrar.",
        "Nationale stabiliteit.",
    ),
    "CCP_CARD_FACTORIES": _row(
        "FACTORIES", "FABRIKEN", "USINES", "ЗАВОДЫ", "FABRİKALAR", "FABRIEKEN"
    ),
    "CCP_CARD_FACTORIES_VALUE": _row(
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] dock",
        "[?num_of_civilian_factories|0] zivil · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] Werft",
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] chant",
        "[?num_of_civilian_factories|0] гражд · [?num_of_military_factories|0] воен · [?num_of_naval_factories|0] верфь",
        "[?num_of_civilian_factories|0] sivil · [?num_of_military_factories|0] askeri · [?num_of_naval_factories|0] tersane",
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] werf",
    ),
    "CCP_CARD_FACTORIES_TOOLTIP": _row(
        "Civilian factories, military factories and dockyards.",
        "Zivile Fabriken, Militärfabriken und Werften.",
        "Usines civiles, usines militaires et chantiers navals.",
        "Гражданские заводы, военные заводы и верфи.",
        "Sivil fabrikalar, askeri fabrikalar ve tersaneler.",
        "Civiele fabrieken, militaire fabrieken en scheepswerven.",
    ),
    "CCP_PAD_LABEL": _row(
        "CUSTOM AMOUNT", "EIGENE MENGE", "MONTANT PERSONNALISÉ",
        "СВОЁ ЗНАЧЕНИЕ", "ÖZEL MİKTAR", "EIGEN AANTAL",
    ),
    "CCP_PAD_BACK": _row("DEL", "LÖSCH", "EFF", "СТЕР", "SİL", "WIS"),
    "CCP_PAD_CLEAR": _row("CLR", "RESET", "RAZ", "СБРОС", "TEMİZLE", "LEEG"),
    "CCP_PAD_DIGIT_TOOLTIP": _row(
        "Append this digit to the custom amount.",
        "Hängt diese Ziffer an die eigene Menge an.",
        "Ajoute ce chiffre au montant personnalisé.",
        "Добавляет цифру к введённому значению.",
        "Bu rakamı özel miktarın sonuna ekler.",
        "Voegt dit cijfer toe aan het eigen aantal.",
    ),
    "CCP_PAD_BACK_TOOLTIP": _row(
        "Remove the last digit.",
        "Entfernt die letzte Ziffer.",
        "Supprime le dernier chiffre.",
        "Удаляет последнюю цифру.",
        "Son rakamı siler.",
        "Verwijdert het laatste cijfer.",
    ),
    "CCP_PAD_CLEAR_TOOLTIP": _row(
        "Reset the custom amount to zero.",
        "Setzt die eigene Menge auf null zurück.",
        "Remet le montant personnalisé à zéro.",
        "Обнуляет введённое значение.",
        "Özel miktarı sıfırlar.",
        "Zet het eigen aantal terug op nul.",
    ),
    "CCP_PAD_HELP": _row(
        "Hearts of Iron IV cannot read a typed value back into script, so the amount is entered here instead. Each CUSTOM button grants this amount, capped at what that resource can usefully take.",
        "Hearts of Iron IV kann einen eingetippten Wert nicht ans Skript zurückgeben, daher wird die Menge hier eingegeben. Jede EIGENER-Schaltfläche vergibt diese Menge, begrenzt auf das, was die Ressource sinnvoll aufnimmt.",
        "Hearts of Iron IV ne peut pas renvoyer une valeur saisie au script ; le montant se saisit donc ici. Chaque bouton PERSO accorde ce montant, plafonné à ce que la ressource peut réellement utiliser.",
        "Hearts of Iron IV не может вернуть набранное значение в скрипт, поэтому величина вводится здесь. Каждая кнопка СВОЁ выдаёт это количество с ограничением по ресурсу.",
        "Hearts of Iron IV, yazılan bir değeri script'e geri okuyamaz; bu yüzden miktar buradan girilir. Her ÖZEL butonu bu miktarı verir ve ilgili kaynağın anlamlı üst sınırında kırpılır.",
        "Hearts of Iron IV kan een getypte waarde niet teruglezen in script, dus het aantal wordt hier ingevoerd. Elke EIGEN-knop kent dit aantal toe, begrensd op wat die grondstof zinvol aankan.",
    ),
}

SECTION_NAMES: dict[str, Row] = {
    "dashboard": _row(
        "Dashboard", "Übersicht", "Tableau de bord", "Обзор", "Genel Bakış", "Overzicht"
    ),
    "resources": _row(
        "Resources", "Ressourcen", "Ressources", "Ресурсы", "Kaynaklar", "Grondstoffen"
    ),
    "settings": _row(
        "Settings", "Einstellungen", "Paramètres", "Настройки", "Ayarlar", "Instellingen"
    ),
}

SECTION_TOOLTIPS: dict[str, Row] = {
    "dashboard": _row(
        "A live summary of the country you are playing.",
        "Eine Live-Übersicht des Landes, das Sie spielen.",
        "Un résumé en direct du pays que vous jouez.",
        "Сводка по стране, за которую вы играете.",
        "Oynadığınız ülkenin canlı özeti.",
        "Een live overzicht van het land dat je speelt.",
    ),
    "resources": _row(
        "Grant political power, command power, manpower and experience.",
        "Vergibt politische Macht, Kommandopunkte, Rekruten und Erfahrung.",
        "Accorde pouvoir politique, points de commandement, effectifs et expérience.",
        "Выдаёт политическую силу, очки командования, людские ресурсы и опыт.",
        "Siyasi güç, komuta gücü, insan gücü ve tecrübe ekleyin.",
        "Kent politieke macht, commandopunten, manschappen en ervaring toe.",
    ),
    "settings": _row(
        "Change the hotkey and the confirmation behaviour.",
        "Ändert Tastenkürzel und Bestätigungsverhalten.",
        "Modifie le raccourci et le comportement des confirmations.",
        "Меняет горячую клавишу и поведение подтверждений.",
        "Kısayol tuşunu ve onay davranışını değiştirin.",
        "Wijzigt de sneltoets en het bevestigingsgedrag.",
    ),
}

RESOURCE_NAMES: dict[str, Row] = {
    "political_power": _row(
        "Political Power", "Politische Macht", "Pouvoir politique",
        "Политическая сила", "Siyasi Güç", "Politieke macht",
    ),
    "command_power": _row(
        "Command Power", "Kommandopunkte", "Points de commandement",
        "Очки командования", "Komuta Gücü", "Commandopunten",
    ),
    "manpower": _row(
        "Manpower", "Rekruten", "Effectifs", "Людские ресурсы", "İnsan Gücü", "Manschappen"
    ),
    "army_experience": _row(
        "Army Experience", "Heereserfahrung", "Expérience terrestre",
        "Опыт армии", "Ordu Tecrübesi", "Legerervaring",
    ),
    "navy_experience": _row(
        "Navy Experience", "Marineerfahrung", "Expérience navale",
        "Опыт флота", "Donanma Tecrübesi", "Marine-ervaring",
    ),
    "air_experience": _row(
        "Air Experience", "Luftwaffenerfahrung", "Expérience aérienne",
        "Опыт авиации", "Hava Tecrübesi", "Luchtmachtervaring",
    ),
}

RESOURCE_HELP: dict[str, Row] = {
    "political_power": _row(
        "Spent on advisors, laws and decisions.",
        "Wird für Berater, Gesetze und Entscheidungen ausgegeben.",
        "Dépensé pour les conseillers, les lois et les décisions.",
        "Тратится на советников, законы и решения.",
        "Danışmanlar, yasalar ve kararlar için harcanır.",
        "Wordt besteed aan adviseurs, wetten en besluiten.",
    ),
    "command_power": _row(
        "Spent on army abilities. The game caps command power at 100, so larger grants are wasted.",
        "Für Armeefähigkeiten. Das Spiel begrenzt Kommandopunkte auf 100, mehr verfällt.",
        "Pour les capacités d'armée. Le jeu plafonne à 100, au-delà c'est perdu.",
        "Для армейских способностей. Игра ограничивает их сотней, излишек пропадает.",
        "Ordu yetenekleri için harcanır. Oyun komuta gücünü 100 ile sınırlar, fazlası boşa gider.",
        "Voor legervaardigheden. Het spel begrenst dit op 100, meer gaat verloren.",
    ),
    "manpower": _row(
        "Used to deploy and reinforce divisions.",
        "Zum Aufstellen und Verstärken von Divisionen.",
        "Sert à déployer et renforcer les divisions.",
        "Используется для развёртывания и пополнения дивизий.",
        "Tümen konuşlandırmak ve takviye etmek için kullanılır.",
        "Voor het inzetten en aanvullen van divisies.",
    ),
    "army_experience": _row(
        "Spent on division templates.",
        "Wird für Divisionsvorlagen ausgegeben.",
        "Dépensé sur les modèles de division.",
        "Тратится на шаблоны дивизий.",
        "Tümen şablonlarında harcanır.",
        "Wordt besteed aan divisiesjablonen.",
    ),
    "navy_experience": _row(
        "Spent on ship designs.",
        "Wird für Schiffsentwürfe ausgegeben.",
        "Dépensé sur les modèles de navire.",
        "Тратится на проекты кораблей.",
        "Gemi tasarımlarında harcanır.",
        "Wordt besteed aan scheepsontwerpen.",
    ),
    "air_experience": _row(
        "Spent on aircraft designs.",
        "Wird für Flugzeugentwürfe ausgegeben.",
        "Dépensé sur les modèles d'avion.",
        "Тратится на проекты самолётов.",
        "Uçak tasarımlarında harcanır.",
        "Wordt besteed aan vliegtuigontwerpen.",
    ),
}

ADD_TEMPLATE = _row(
    "Add {amount} {name}.",
    "{amount} {name} hinzufügen.",
    "Ajouter {amount} {name}.",
    "Добавить: {amount} {name}.",
    "{amount} {name} ekler.",
    "{amount} {name} toevoegen.",
)

CUSTOM_TEMPLATE = _row(
    "Add the custom amount, capped at {cap}.",
    "Fügt die eigene Menge hinzu, begrenzt auf {cap}.",
    "Ajoute le montant personnalisé, plafonné à {cap}.",
    "Добавляет введённое значение, максимум {cap}.",
    "Özel miktarı ekler, üst sınır {cap}.",
    "Voegt het eigen aantal toe, met een maximum van {cap}.",
)

HOTKEY_TEMPLATE = _row(
    "Use {key} to open and close the panel.",
    "Mit {key} das Panel öffnen und schließen.",
    "Utiliser {key} pour ouvrir et fermer le panneau.",
    "Клавиша {key} открывает и закрывает панель.",
    "Paneli açıp kapatmak için {key} tuşunu kullanın.",
    "Gebruik {key} om het paneel te openen en te sluiten.",
)


def _fill(template: Row, **values: str) -> Row:
    return {language: text.format(**values) for language, text in template.items()}


def _same(value: str) -> Row:
    return {language: value for language in ALL}


def all_strings() -> dict[str, Row]:
    strings: dict[str, Row] = {key: _same(value) for key, value in NEUTRAL.items()}
    strings.update(TRANSLATED)

    for digit in range(10):
        strings[f"CCP_PAD_DIGIT_{digit}"] = _same(str(digit))

    for section in SECTIONS:
        strings[section.key] = SECTION_NAMES[section.slug]
        strings[f"{section.key}_TOOLTIP"] = SECTION_TOOLTIPS[section.slug]

    for resource in RESOURCES:
        names = RESOURCE_NAMES[resource.slug]
        strings[resource.key] = names
        strings[f"{resource.key}_VALUE"] = _same(f"[?{resource.variable}|0]")
        strings[f"{resource.key}_TOOLTIP"] = RESOURCE_HELP[resource.slug]

        for slot, amount in enumerate(resource.presets, start=1):
            strings[f"{resource.key}_P{slot}"] = _same(preset_label(amount))
            strings[f"{resource.key}_P{slot}_TOOLTIP"] = {
                language: ADD_TEMPLATE[language].format(
                    amount=f"{amount:,}", name=names[language]
                )
                for language in ALL
            }
        strings[f"{resource.key}_CUSTOM_TOOLTIP"] = _fill(
            CUSTOM_TEMPLATE, cap=f"{resource.safe_max:,}"
        )

    for index, (_, english, _turkish) in enumerate(HOTKEYS, start=1):
        strings[f"CCP_HOTKEY_{index}"] = _same(english)
        strings[f"CCP_HOTKEY_{index}_TOOLTIP"] = _fill(HOTKEY_TEMPLATE, key=english)

    gaps = {key: sorted(set(ALL) - set(row)) for key, row in strings.items() if set(ALL) - set(row)}
    if gaps:
        raise KeyError(f"strings missing translations: {gaps}")

    return strings


def emit_localisation(language: str) -> str:
    lines = [f"l_{language}:"]
    lines += [f' {key}:0 "{row[language]}"' for key, row in sorted(all_strings().items())]
    return "\n".join(lines) + "\n"
