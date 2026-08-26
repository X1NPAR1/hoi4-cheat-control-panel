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
    "CCP_EQUIPMENT_CATEGORIES": _row(
        "CATEGORIES", "KATEGORIEN", "CATÉGORIES", "КАТЕГОРИИ", "KATEGORİLER", "CATEGORIEËN"
    ),
    "CCP_EQUIPMENT_CATEGORY_TOOLTIP": _row(
        "Show the equipment in this category.",
        "Zeigt die Ausrüstung dieser Kategorie.",
        "Affiche l'équipement de cette catégorie.",
        "Показать снаряжение этой категории.",
        "Bu kategorideki teçhizatı gösterir.",
        "Toont de uitrusting in deze categorie.",
    ),
    "CCP_EQUIPMENT_ADD": _row("ADD", "HINZU", "AJOUTER", "ДОБАВ", "EKLE", "TOEVOEG"),
    "CCP_EQUIPMENT_ADD_TOOLTIP": _row(
        "Add the custom amount of this equipment to your stockpile.",
        "Fügt die eingestellte Menge dieser Ausrüstung dem Lager hinzu.",
        "Ajoute au stock la quantité définie de cet équipement.",
        "Добавляет на склад заданное количество этого снаряжения.",
        "Bu teçhizattan belirlenen miktarı stoğunuza ekler.",
        "Voegt het ingestelde aantal van deze uitrusting toe aan je voorraad.",
    ),
    "CCP_EQUIPMENT_LATEST": _row("LATEST", "NEUSTE", "RÉCENT", "НОВОЕ", "SON", "NIEUWSTE"),
    "CCP_EQUIPMENT_LATEST_TOOLTIP": _row(
        "Add the newest variant of this equipment line instead of this one.",
        "Fügt statt dieser die neuste Variante dieser Ausrüstungslinie hinzu.",
        "Ajoute la variante la plus récente de cette lignée plutôt que celle-ci.",
        "Добавляет новейший вариант этой линейки вместо выбранного.",
        "Bunun yerine bu teçhizat serisinin en yeni sürümünü ekler.",
        "Voegt de nieuwste variant van deze reeks toe in plaats van deze.",
    ),
    "CCP_EQUIPMENT_PREV": _row("PREV", "ZURÜCK", "PRÉC", "НАЗАД", "ÖNCEKİ", "VORIGE"),
    "CCP_EQUIPMENT_PREV_TOOLTIP": _row(
        "Show the previous page of this category.",
        "Zeigt die vorherige Seite dieser Kategorie.",
        "Affiche la page précédente de cette catégorie.",
        "Показать предыдущую страницу категории.",
        "Bu kategorinin önceki sayfasını gösterir.",
        "Toont de vorige pagina van deze categorie.",
    ),
    "CCP_EQUIPMENT_NEXT": _row("NEXT", "WEITER", "SUIV", "ДАЛЕЕ", "SONRAKİ", "VOLGENDE"),
    "CCP_EQUIPMENT_NEXT_TOOLTIP": _row(
        "Show the next page of this category.",
        "Zeigt die nächste Seite dieser Kategorie.",
        "Affiche la page suivante de cette catégorie.",
        "Показать следующую страницу категории.",
        "Bu kategorinin sonraki sayfasını gösterir.",
        "Toont de volgende pagina van deze categorie.",
    ),
    "CCP_EQUIPMENT_PAGE": _row(
        "Page [?ccp_equipment_page_shown|+0] of [?ccp_equipment_pages_shown|+0]",
        "Seite [?ccp_equipment_page_shown|+0] von [?ccp_equipment_pages_shown|+0]",
        "Page [?ccp_equipment_page_shown|+0] sur [?ccp_equipment_pages_shown|+0]",
        "Страница [?ccp_equipment_page_shown|+0] из [?ccp_equipment_pages_shown|+0]",
        "Sayfa [?ccp_equipment_page_shown|+0] / [?ccp_equipment_pages_shown|+0]",
        "Pagina [?ccp_equipment_page_shown|+0] van [?ccp_equipment_pages_shown|+0]",
    ),
    "CCP_EQUIPMENT_UNKNOWN": _row(
        "Unknown equipment", "Unbekannte Ausrüstung", "Équipement inconnu",
        "Неизвестное снаряжение", "Bilinmeyen teçhizat", "Onbekende uitrusting",
    ),
    "CCP_STATUS_EQUIPMENT": _row(
        "Added [?ccp_amount|0] × [CCP_GetEquipmentSelectedName].",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] hinzugefügt.",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] ajouté.",
        "Добавлено: [?ccp_amount|0] × [CCP_GetEquipmentSelectedName].",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] eklendi.",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] toegevoegd.",
    ),
    "CCP_RESEARCH_GRANT": _row(
        "RESEARCH", "ERFORSCHEN", "RECHERCHER", "ИЗУЧИТЬ", "ARAŞTIR", "ONDERZOEK"
    ),
    "CCP_RESEARCH_GRANT_TOOLTIP": _row(
        "Complete this technology immediately.",
        "Schliesst diese Technologie sofort ab.",
        "Termine cette technologie immédiatement.",
        "Мгновенно завершает эту технологию.",
        "Bu teknolojiyi anında tamamlar.",
        "Voltooit deze technologie onmiddellijk.",
    ),
    "CCP_RESEARCH_ALL": _row(
        "RESEARCH FOLDER", "ORDNER ERFORSCHEN", "TOUT LE DOSSIER",
        "ВСЮ ПАПКУ", "KLASÖRÜ ARAŞTIR", "HELE MAP",
    ),
    "CCP_RESEARCH_ALL_TOOLTIP": _row(
        "Complete every technology in the selected folder.",
        "Schliesst jede Technologie im gewählten Ordner ab.",
        "Termine toutes les technologies du dossier sélectionné.",
        "Завершает все технологии выбранной папки.",
        "Seçili klasördeki tüm teknolojileri tamamlar.",
        "Voltooit elke technologie in de gekozen map.",
    ),
    "CCP_RESEARCH_ALL_HELP": _row(
        "Doctrines use a separate system and cannot be granted with this effect.",
        "Doktrinen nutzen ein eigenes System und lassen sich damit nicht vergeben.",
        "Les doctrines utilisent un système distinct et ne peuvent pas être accordées ici.",
        "Доктрины используют отдельную систему и здесь недоступны.",
        "Doktrinler ayrı bir sistem kullanır ve buradan verilemez.",
        "Doctrines gebruiken een apart systeem en kunnen hier niet worden toegekend.",
    ),
    "CCP_RESEARCH_PAGE": _row(
        "Page [?ccp_research_page_shown|+0] of [?ccp_research_pages_shown|+0]",
        "Seite [?ccp_research_page_shown|+0] von [?ccp_research_pages_shown|+0]",
        "Page [?ccp_research_page_shown|+0] sur [?ccp_research_pages_shown|+0]",
        "Страница [?ccp_research_page_shown|+0] из [?ccp_research_pages_shown|+0]",
        "Sayfa [?ccp_research_page_shown|+0] / [?ccp_research_pages_shown|+0]",
        "Pagina [?ccp_research_page_shown|+0] van [?ccp_research_pages_shown|+0]",
    ),
    "CCP_RESEARCH_UNKNOWN": _row(
        "Unknown technology", "Unbekannte Technologie", "Technologie inconnue",
        "Неизвестная технология", "Bilinmeyen teknoloji", "Onbekende technologie",
    ),
    "CCP_STATUS_TECH": _row(
        "Researched [CCP_GetTechnologySelectedName].",
        "[CCP_GetTechnologySelectedName] erforscht.",
        "[CCP_GetTechnologySelectedName] recherché.",
        "Изучено: [CCP_GetTechnologySelectedName].",
        "[CCP_GetTechnologySelectedName] araştırıldı.",
        "[CCP_GetTechnologySelectedName] onderzocht.",
    ),
    "CCP_STATUS_FOLDER": _row(
        "Researched every technology in [CCP_GetResearchFolderName].",
        "Jede Technologie in [CCP_GetResearchFolderName] erforscht.",
        "Toutes les technologies de [CCP_GetResearchFolderName] recherchées.",
        "Изучены все технологии в разделе [CCP_GetResearchFolderName].",
        "[CCP_GetResearchFolderName] içindeki tüm teknolojiler araştırıldı.",
        "Elke technologie in [CCP_GetResearchFolderName] onderzocht.",
    ),
    "CCP_COUNTRY_HELP": _row(
        "Every country that exists in the current game. Destructive actions ask first unless you turned confirmations off.",
        "Jedes im laufenden Spiel existierende Land. Unumkehrbare Aktionen fragen nach, sofern Bestätigungen aktiv sind.",
        "Tous les pays existants dans la partie. Les actions irréversibles demandent confirmation si elle est activée.",
        "Все существующие в текущей игре страны. Необратимые действия запрашивают подтверждение, если оно включено.",
        "Mevcut oyunda var olan tüm ülkeler. Onay istemi açıksa geri alınamaz işlemler önce sorar.",
        "Elk land dat in het huidige spel bestaat. Onomkeerbare acties vragen eerst, tenzij je bevestigingen hebt uitgezet.",
    ),
    "CCP_COUNTRY_ENTRY_NAME": _row(
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
    ),
    "CCP_COUNTRY_PAGE": _row(
        "Page [?ccp_country_page_shown|+0] of [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] countries",
        "Seite [?ccp_country_page_shown|+0] von [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] Länder",
        "Page [?ccp_country_page_shown|+0] sur [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] pays",
        "Страница [?ccp_country_page_shown|+0] из [?ccp_country_pages_shown|+0] · стран: [?ccp_country_count|0]",
        "Sayfa [?ccp_country_page_shown|+0] / [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] ülke",
        "Pagina [?ccp_country_page_shown|+0] van [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] landen",
    ),
    "CCP_COUNTRY_ANNEX": _row("ANNEX", "ANNEKT.", "ANNEXER", "АННЕКС", "İLHAK", "ANNEX"),
    "CCP_COUNTRY_ANNEX_TOOLTIP": _row(
        "Annex this country. There is no undo.",
        "Annektiert dieses Land. Es gibt kein Rückgängig.",
        "Annexe ce pays. Aucune annulation possible.",
        "Аннексирует страну. Отменить нельзя.",
        "Bu ülkeyi ilhak eder. Geri alınamaz.",
        "Annexeert dit land. Er is geen ongedaan maken.",
    ),
    "CCP_COUNTRY_PUPPET": _row("PUPPET", "MARION.", "VASSAL", "МАРИОН", "KUKLA", "VAZAL"),
    "CCP_COUNTRY_PUPPET_TOOLTIP": _row(
        "Make this country your puppet.",
        "Macht dieses Land zu Ihrem Marionettenstaat.",
        "Fait de ce pays votre vassal.",
        "Делает страну вашей марионеткой.",
        "Bu ülkeyi kuklanız yapar.",
        "Maakt dit land je vazal.",
    ),
    "CCP_COUNTRY_WAR": _row("WAR", "KRIEG", "GUERRE", "ВОЙНА", "SAVAŞ", "OORLOG"),
    "CCP_COUNTRY_WAR_TOOLTIP": _row(
        "Declare war on this country with an annexation war goal.",
        "Erklärt diesem Land den Krieg mit dem Kriegsziel Annexion.",
        "Déclare la guerre à ce pays avec un objectif annexion.",
        "Объявляет войну с целью аннексии.",
        "Bu ülkeye ilhak savaş hedefiyle savaş ilan eder.",
        "Verklaart dit land de oorlog met annexatie als oorlogsdoel.",
    ),
    "CCP_COUNTRY_PEACE": _row("PEACE", "FRIEDEN", "PAIX", "МИР", "BARIŞ", "VREDE"),
    "CCP_COUNTRY_PEACE_TOOLTIP": _row(
        "White peace with this country, if you are at war with it.",
        "Weißer Frieden mit diesem Land, sofern Sie im Krieg sind.",
        "Paix blanche avec ce pays, si vous êtes en guerre.",
        "Белый мир с этой страной, если вы воюете.",
        "Savaştaysanız bu ülkeyle beyaz barış yapar.",
        "Witte vrede met dit land, als je in oorlog bent.",
    ),
    "CCP_COUNTRY_PLAYAS": _row("PLAY AS", "SPIELEN", "INCARNER", "ИГРАТЬ", "OYNA", "SPELEN"),
    "CCP_COUNTRY_PLAYAS_TOOLTIP": _row(
        "Continue the game as this country. The panel closes so the switch can take effect.",
        "Spielt als dieses Land weiter. Das Panel schliesst sich, damit der Wechsel greift.",
        "Poursuit la partie avec ce pays. Le panneau se ferme pour appliquer le changement.",
        "Продолжить игру за эту страну. Панель закроется, чтобы переход сработал.",
        "Oyuna bu ülkeyle devam eder. Geçişin uygulanması için panel kapanır.",
        "Speelt verder als dit land. Het paneel sluit zodat de wissel doorgaat.",
    ),
    "CCP_MODAL_TITLE": _row(
        "ARE YOU SURE?", "SIND SIE SICHER?", "CONFIRMER ?",
        "ВЫ УВЕРЕНЫ?", "EMİN MİSİNİZ?", "WEET JE HET ZEKER?",
    ),
    "CCP_MODAL_BODY": _row(
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nThis cannot be undone. The engine offers no way to restore the previous state.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nDies lässt sich nicht rückgängig machen. Die Engine bietet keine Wiederherstellung.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nCeci est irréversible. Le moteur ne permet aucune restauration.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nЭто необратимо. Движок не позволяет восстановить прежнее состояние.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nBu geri alınamaz. Engine önceki duruma dönmek için bir yol sunmuyor.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nDit kan niet ongedaan worden gemaakt. De engine biedt geen herstel.",
    ),
    "CCP_TOOLTIP_CANCEL": _row(
        "Close this prompt without doing anything.",
        "Schliesst die Abfrage, ohne etwas zu tun.",
        "Ferme cette invite sans rien faire.",
        "Закрывает запрос, ничего не делая.",
        "Hiçbir şey yapmadan bu istemi kapatır.",
        "Sluit deze vraag zonder iets te doen.",
    ),
    "CCP_TOOLTIP_CONFIRM": _row(
        "Apply the action. This cannot be undone.",
        "Führt die Aktion aus. Nicht rückgängig zu machen.",
        "Applique action. Irréversible.",
        "Применяет действие. Отменить нельзя.",
        "İşlemi uygular. Geri alınamaz.",
        "Voert de actie uit. Niet ongedaan te maken.",
    ),
    "CCP_STATUS_COUNTRY": _row(
        "[CCP_GetPendingAction] applied.",
        "[CCP_GetPendingAction] ausgeführt.",
        "[CCP_GetPendingAction] appliqué.",
        "Выполнено: [CCP_GetPendingAction].",
        "[CCP_GetPendingAction] uygulandı.",
        "[CCP_GetPendingAction] uitgevoerd.",
    ),
    "CCP_STATUS_CANCELLED": _row(
        "Action cancelled. Nothing was changed.",
        "Aktion abgebrochen. Nichts wurde geändert.",
        "Action annulée. Rien modifié.",
        "Действие отменено. Ничего не изменилось.",
        "İşlem iptal edildi. Hiçbir şey değişmedi.",
        "Actie geannuleerd. Er is niets gewijzigd.",
    ),
    "CCP_STATE_HELP": _row(
        "Every state in the game. You can also turn on map picking and left-click a state directly.",
        "Jeder Staat im Spiel. Alternativ die Kartenauswahl aktivieren und einen Staat anklicken.",
        "Tous les États du jeu. Vous pouvez aussi activer la sélection sur la carte et cliquer un État.",
        "Все провинции в игре. Можно также включить выбор на карте и кликнуть по провинции.",
        "Oyundaki tüm eyaletler. Harita seçimini açıp bir eyalete doğrudan tıklayabilirsiniz de.",
        "Elke staat in het spel. Je kunt ook kaartselectie aanzetten en een staat aanklikken.",
    ),
    "CCP_STATE_PICKER_TOOLTIP": _row(
        "When map picking is on, left-clicking a state shows these actions on the state view.",
        "Bei aktiver Kartenauswahl erscheinen diese Aktionen beim Anklicken eines Staates.",
        "Avec la sélection carte activée, cliquer un État affiche ces actions sur sa vue.",
        "При включённом выборе на карте клик по провинции показывает эти действия.",
        "Harita seçimi açıkken bir eyalete tıklamak bu işlemleri eyalet görünümünde gösterir.",
        "Met kaartselectie aan toont een klik op een staat deze acties in de staatweergave.",
    ),
    "CCP_STATE_PICKER_ON": _row(
        "MAP PICKING: ON", "KARTENAUSWAHL: AN", "SÉLECTION CARTE : ON",
        "ВЫБОР НА КАРТЕ: ВКЛ", "HARİTA SEÇİMİ: AÇIK", "KAARTSELECTIE: AAN",
    ),
    "CCP_STATE_PICKER_OFF": _row(
        "MAP PICKING: OFF", "KARTENAUSWAHL: AUS", "SÉLECTION CARTE : OFF",
        "ВЫБОР НА КАРТЕ: ВЫКЛ", "HARİTA SEÇİMİ: KAPALI", "KAARTSELECTIE: UIT",
    ),
    "CCP_STATE_PICKER_TITLE": _row(
        "CHEAT CONTROL PANEL", "CHEAT-KONTROLLPANEL", "PANNEAU DE TRICHE",
        "ПАНЕЛЬ ЧИТОВ", "HİLE KONTROL PANELİ", "CHEAT-PANEEL",
    ),
    "CCP_STATE_ENTRY_NAME": _row(
        "[THIS.GetName]", "[THIS.GetName]", "[THIS.GetName]",
        "[THIS.GetName]", "[THIS.GetName]", "[THIS.GetName]",
    ),
    "CCP_STATE_ENTRY_OWNER": _row(
        "Owner [THIS.Owner.GetNameDefCap] · controller [THIS.Controller.GetNameDefCap]",
        "Besitzer [THIS.Owner.GetNameDefCap] · Kontrolle [THIS.Controller.GetNameDefCap]",
        "Propriétaire [THIS.Owner.GetNameDefCap] · contrôle [THIS.Controller.GetNameDefCap]",
        "Владелец [THIS.Owner.GetNameDefCap] · контроль [THIS.Controller.GetNameDefCap]",
        "Sahip [THIS.Owner.GetNameDefCap] · kontrol [THIS.Controller.GetNameDefCap]",
        "Eigenaar [THIS.Owner.GetNameDefCap] · controle [THIS.Controller.GetNameDefCap]",
    ),
    "CCP_STATE_PAGE": _row(
        "Page [?ccp_state_page_shown|+0] of [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] states",
        "Seite [?ccp_state_page_shown|+0] von [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] Staaten",
        "Page [?ccp_state_page_shown|+0] sur [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] États",
        "Страница [?ccp_state_page_shown|+0] из [?ccp_state_pages_shown|+0] · провинций: [?ccp_state_count|0]",
        "Sayfa [?ccp_state_page_shown|+0] / [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] eyalet",
        "Pagina [?ccp_state_page_shown|+0] van [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] staten",
    ),
    "CCP_STATE_TAKE": _row("TAKE", "NEHMEN", "PRENDRE", "ЗАБРАТЬ", "AL", "NEEM"),
    "CCP_STATE_TAKE_TOOLTIP": _row(
        "Become owner and controller of this state.",
        "Macht Sie zum Besitzer und Kontrolleur dieses Staates.",
        "Vous devenez propriétaire et contrôleur de cet État.",
        "Вы становитесь владельцем и контролёром провинции.",
        "Bu eyaletin sahibi ve kontrolörü olursunuz.",
        "Je wordt eigenaar en controleur van deze staat.",
    ),
    "CCP_STATE_CORE": _row("CORE", "KERN", "CŒUR", "ЯДРО", "CORE", "KERN"),
    "CCP_STATE_CORE_TOOLTIP": _row(
        "Add your core to this state.",
        "Fügt Ihr Kerngebiet zu diesem Staat hinzu.",
        "Ajoute votre territoire national sur cet État.",
        "Добавляет вашу коренную территорию.",
        "Bu eyalete core ekler.",
        "Voegt jouw kerngebied toe aan deze staat.",
    ),
    "CCP_STATE_UNCORE": _row("UNCORE", "KERN WEG", "RETIRER", "СНЯТЬ", "CORE SİL", "KERN WEG"),
    "CCP_STATE_UNCORE_TOOLTIP": _row(
        "Remove your core from this state. There is no undo.",
        "Entfernt Ihr Kerngebiet. Es gibt kein Rückgängig.",
        "Retire votre territoire national. Aucune annulation.",
        "Снимает вашу коренную территорию. Отменить нельзя.",
        "Core kaydınızı kaldırır. Geri alınamaz.",
        "Verwijdert jouw kerngebied. Er is geen ongedaan maken.",
    ),
    "CCP_STATE_CLAIM": _row("CLAIM", "ANSPRUCH", "REVENDIQ", "ПРИТЯЗ", "HAK TALEBİ", "CLAIM"),
    "CCP_STATE_CLAIM_TOOLTIP": _row(
        "Add your claim to this state.",
        "Erhebt Anspruch auf diesen Staat.",
        "Revendique cet État.",
        "Выдвигает притязание на провинцию.",
        "Bu eyalet üzerinde hak talebi oluşturur.",
        "Legt een claim op deze staat.",
    ),
    "CCP_STATUS_STATE": _row(
        "State updated.",
        "Staat aktualisiert.",
        "État mis à jour.",
        "Провинция обновлена.",
        "Eyalet güncellendi.",
        "Staat bijgewerkt.",
    ),
    "CCP_NATION_HELP": _row(
        "One-click changes to your country as a whole.",
        "Änderungen an Ihrem Land mit einem Klick.",
        "Modifications de votre pays en un clic.",
        "Изменения вашей страны одним нажатием.",
        "Ülkenizin geneline tek tıkla yapılan değişiklikler.",
        "Wijzigingen aan je land met één klik.",
    ),
    "CCP_CONSTRUCTION_HELP": _row(
        "Buildings are added to every state you own and finish instantly.",
        "Gebäude werden in jedem Ihrer Staaten ergänzt und sofort fertiggestellt.",
        "Les bâtiments sont ajoutés à tous vos États et achevés instantanément.",
        "Здания добавляются во все ваши провинции и достраиваются мгновенно.",
        "Binalar sahip olduğunuz her eyalete eklenir ve anında tamamlanır.",
        "Gebouwen worden aan elke staat die je bezit toegevoegd en zijn meteen klaar.",
    ),
    "CCP_COMMANDERS_HELP": _row(
        "Applies to every commander you currently have, not to future ones.",
        "Gilt für alle derzeitigen Befehlshaber, nicht für künftige.",
        "S'applique à tous vos commandants actuels, pas aux futurs.",
        "Действует на текущих командующих, но не на будущих.",
        "Şu anki tüm komutanlarınıza uygulanır, gelecektekilere değil.",
        "Geldt voor al je huidige bevelhebbers, niet voor toekomstige.",
    ),
    "CCP_STATUS_ACTION": _row(
        "[CCP_GetLastAction] applied.",
        "[CCP_GetLastAction] ausgeführt.",
        "[CCP_GetLastAction] appliqué.",
        "Выполнено: [CCP_GetLastAction].",
        "[CCP_GetLastAction] uygulandı.",
        "[CCP_GetLastAction] uitgevoerd.",
    ),
    "CCP_ACTION_STABILITY_MAX": _row(
        "STABILITY 100%", "STABILITÄT 100%", "STABILITÉ 100%", "СТАБИЛЬНОСТЬ 100%", "İSTİKRAR %100", "STABILITEIT 100%"
    ),
    "CCP_ACTION_STABILITY_MAX_HELP": _row(
        "Set national stability to its maximum.",
        "Setzt die Stabilität auf das Maximum.",
        "Porte la stabilité au maximum.",
        "Устанавливает максимальную стабильность.",
        "Ulusal istikrarı en yükseğe çeker.",
        "Zet de stabiliteit op het maximum.",
    ),
    "CCP_ACTION_STABILITY_MAX_TOOLTIP": _row(
        "Set national stability to its maximum.",
        "Setzt die Stabilität auf das Maximum.",
        "Porte la stabilité au maximum.",
        "Устанавливает максимальную стабильность.",
        "Ulusal istikrarı en yükseğe çeker.",
        "Zet de stabiliteit op het maximum.",
    ),
    "CCP_ACTION_WAR_SUPPORT_MAX": _row(
        "WAR SUPPORT 100%", "KRIEGSUNTERST. 100%", "SOUTIEN 100%", "ПОДДЕРЖКА 100%", "SAVAŞ DESTEĞİ %100", "OORLOGSSTEUN 100%"
    ),
    "CCP_ACTION_WAR_SUPPORT_MAX_HELP": _row(
        "Set war support to its maximum.",
        "Setzt die Kriegsunterstützung auf das Maximum.",
        "Porte le soutien à la guerre au maximum.",
        "Устанавливает максимальную поддержку войны.",
        "Savaş desteğini en yükseğe çeker.",
        "Zet de oorlogssteun op het maximum.",
    ),
    "CCP_ACTION_WAR_SUPPORT_MAX_TOOLTIP": _row(
        "Set war support to its maximum.",
        "Setzt die Kriegsunterstützung auf das Maximum.",
        "Porte le soutien à la guerre au maximum.",
        "Устанавливает максимальную поддержку войны.",
        "Savaş desteğini en yükseğe çeker.",
        "Zet de oorlogssteun op het maximum.",
    ),
    "CCP_ACTION_STABILITY_MIN": _row(
        "STABILITY 0%", "STABILITÄT 0%", "STABILITÉ 0%", "СТАБИЛЬНОСТЬ 0%", "İSTİKRAR %0", "STABILITEIT 0%"
    ),
    "CCP_ACTION_STABILITY_MIN_HELP": _row(
        "Drop stability to zero. Useful for triggering civil wars.",
        "Senkt die Stabilität auf null. Nützlich, um Bürgerkriege auszulösen.",
        "Réduit la stabilité à zéro. Utile pour déclencher une guerre civile.",
        "Обнуляет стабильность. Полезно для гражданской войны.",
        "İstikrarı sıfıra düşürür. İç savaş tetiklemek için kullanışlı.",
        "Zet de stabiliteit op nul. Handig om burgeroorlogen uit te lokken.",
    ),
    "CCP_ACTION_STABILITY_MIN_TOOLTIP": _row(
        "Drop stability to zero. Useful for triggering civil wars.",
        "Senkt die Stabilität auf null. Nützlich, um Bürgerkriege auszulösen.",
        "Réduit la stabilité à zéro. Utile pour déclencher une guerre civile.",
        "Обнуляет стабильность. Полезно для гражданской войны.",
        "İstikrarı sıfıra düşürür. İç savaş tetiklemek için kullanışlı.",
        "Zet de stabiliteit op nul. Handig om burgeroorlogen uit te lokken.",
    ),
    "CCP_ACTION_WAR_SUPPORT_MIN": _row(
        "WAR SUPPORT 0%", "KRIEGSUNTERST. 0%", "SOUTIEN 0%", "ПОДДЕРЖКА 0%", "SAVAŞ DESTEĞİ %0", "OORLOGSSTEUN 0%"
    ),
    "CCP_ACTION_WAR_SUPPORT_MIN_HELP": _row(
        "Drop war support to zero.",
        "Senkt die Kriegsunterstützung auf null.",
        "Réduit le soutien à la guerre à zéro.",
        "Обнуляет поддержку войны.",
        "Savaş desteğini sıfıra düşürür.",
        "Zet de oorlogssteun op nul.",
    ),
    "CCP_ACTION_WAR_SUPPORT_MIN_TOOLTIP": _row(
        "Drop war support to zero.",
        "Senkt die Kriegsunterstützung auf null.",
        "Réduit le soutien à la guerre à zéro.",
        "Обнуляет поддержку войны.",
        "Savaş desteğini sıfıra düşürür.",
        "Zet de oorlogssteun op nul.",
    ),
    "CCP_ACTION_RESEARCH_SLOTS": _row(
        "5 RESEARCH SLOTS", "5 FORSCHUNGSPLÄTZE", "5 EMPLACEMENTS", "5 СЛОТОВ", "5 ARAŞTIRMA YUVASI", "5 ONDERZOEKSPLEKKEN"
    ),
    "CCP_ACTION_RESEARCH_SLOTS_HELP": _row(
        "Set your research slots to five, the maximum the game uses.",
        "Setzt Ihre Forschungsplätze auf fünf, das Maximum des Spiels.",
        "Porte vos emplacements de recherche à cinq, le maximum du jeu.",
        "Устанавливает пять слотов исследований — максимум в игре.",
        "Araştırma yuvalarınızı oyunun kullandığı en yüksek sayı olan beşe çıkarır.",
        "Zet je onderzoeksplekken op vijf, het maximum in het spel.",
    ),
    "CCP_ACTION_RESEARCH_SLOTS_TOOLTIP": _row(
        "Set your research slots to five, the maximum the game uses.",
        "Setzt Ihre Forschungsplätze auf fünf, das Maximum des Spiels.",
        "Porte vos emplacements de recherche à cinq, le maximum du jeu.",
        "Устанавливает пять слотов исследований — максимум в игре.",
        "Araştırma yuvalarınızı oyunun kullandığı en yüksek sayı olan beşe çıkarır.",
        "Zet je onderzoeksplekken op vijf, het maximum in het spel.",
    ),
    "CCP_ACTION_FUEL": _row(
        "+500K FUEL", "+500K TREIBSTOFF", "+500K CARBURANT", "+500K ТОПЛИВА", "+500K YAKIT", "+500K BRANDSTOF"
    ),
    "CCP_ACTION_FUEL_HELP": _row(
        "Add half a million fuel to your reserves.",
        "Fügt eine halbe Million Treibstoff hinzu.",
        "Ajoute un demi-million de carburant.",
        "Добавляет полмиллиона топлива.",
        "Rezervlerinize yarım milyon yakıt ekler.",
        "Voegt een half miljoen brandstof toe.",
    ),
    "CCP_ACTION_FUEL_TOOLTIP": _row(
        "Add half a million fuel to your reserves.",
        "Fügt eine halbe Million Treibstoff hinzu.",
        "Ajoute un demi-million de carburant.",
        "Добавляет полмиллиона топлива.",
        "Rezervlerinize yarım milyon yakıt ekler.",
        "Voegt een half miljoen brandstof toe.",
    ),
    "CCP_ACTION_INFRASTRUCTURE": _row(
        "+5 INFRASTRUCTURE", "+5 INFRASTRUKTUR", "+5 INFRASTRUCTURE", "+5 ИНФРАСТРУКТУРЫ", "+5 ALTYAPI", "+5 INFRASTRUCTUUR"
    ),
    "CCP_ACTION_INFRASTRUCTURE_HELP": _row(
        "Add five infrastructure to every state you own, built instantly.",
        "Fügt jedem Ihrer Staaten fünf Infrastruktur hinzu, sofort gebaut.",
        "Ajoute cinq d'infrastructure à chacun de vos États, construits instantanément.",
        "Добавляет пять уровней инфраструктуры во все ваши провинции мгновенно.",
        "Sahip olduğunuz her eyalete anında beş altyapı ekler.",
        "Voegt vijf infrastructuur toe aan elke staat die je bezit, direct gebouwd.",
    ),
    "CCP_ACTION_INFRASTRUCTURE_TOOLTIP": _row(
        "Add five infrastructure to every state you own, built instantly.",
        "Fügt jedem Ihrer Staaten fünf Infrastruktur hinzu, sofort gebaut.",
        "Ajoute cinq d'infrastructure à chacun de vos États, construits instantanément.",
        "Добавляет пять уровней инфраструктуры во все ваши провинции мгновенно.",
        "Sahip olduğunuz her eyalete anında beş altyapı ekler.",
        "Voegt vijf infrastructuur toe aan elke staat die je bezit, direct gebouwd.",
    ),
    "CCP_ACTION_CIVILIAN": _row(
        "+5 CIVILIAN", "+5 ZIVILFABRIKEN", "+5 USINES CIVILES", "+5 ГРАЖД. ЗАВОДОВ", "+5 SİVİL FABRİKA", "+5 CIVIELE FABRIEKEN"
    ),
    "CCP_ACTION_CIVILIAN_HELP": _row(
        "Add five civilian factories to every state you own.",
        "Fügt jedem Ihrer Staaten fünf Zivilfabriken hinzu.",
        "Ajoute cinq usines civiles à chacun de vos États.",
        "Добавляет пять гражданских заводов в каждую вашу провинцию.",
        "Her eyaletinize beş sivil fabrika ekler.",
        "Voegt vijf civiele fabrieken toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_CIVILIAN_TOOLTIP": _row(
        "Add five civilian factories to every state you own.",
        "Fügt jedem Ihrer Staaten fünf Zivilfabriken hinzu.",
        "Ajoute cinq usines civiles à chacun de vos États.",
        "Добавляет пять гражданских заводов в каждую вашу провинцию.",
        "Her eyaletinize beş sivil fabrika ekler.",
        "Voegt vijf civiele fabrieken toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_MILITARY": _row(
        "+5 MILITARY", "+5 MILITÄRFABRIKEN", "+5 USINES MILIT.", "+5 ВОЕН. ЗАВОДОВ", "+5 ASKERİ FABRİKA", "+5 MILITAIRE FABR."
    ),
    "CCP_ACTION_MILITARY_HELP": _row(
        "Add five military factories to every state you own.",
        "Fügt jedem Ihrer Staaten fünf Militärfabriken hinzu.",
        "Ajoute cinq usines militaires à chacun de vos États.",
        "Добавляет пять военных заводов в каждую вашу провинцию.",
        "Her eyaletinize beş askeri fabrika ekler.",
        "Voegt vijf militaire fabrieken toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_MILITARY_TOOLTIP": _row(
        "Add five military factories to every state you own.",
        "Fügt jedem Ihrer Staaten fünf Militärfabriken hinzu.",
        "Ajoute cinq usines militaires à chacun de vos États.",
        "Добавляет пять военных заводов в каждую вашу провинцию.",
        "Her eyaletinize beş askeri fabrika ekler.",
        "Voegt vijf militaire fabrieken toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_DOCKYARD": _row(
        "+3 DOCKYARDS", "+3 WERFTEN", "+3 CHANTIERS", "+3 ВЕРФИ", "+3 TERSANE", "+3 SCHEEPSWERVEN"
    ),
    "CCP_ACTION_DOCKYARD_HELP": _row(
        "Add three dockyards to every coastal state you own.",
        "Fügt jedem Ihrer Küstenstaaten drei Werften hinzu.",
        "Ajoute trois chantiers navals à chacun de vos États côtiers.",
        "Добавляет три верфи в каждую вашу прибрежную провинцию.",
        "Sahip olduğunuz her kıyı eyaletine üç tersane ekler.",
        "Voegt drie scheepswerven toe aan elke kuststaat die je bezit.",
    ),
    "CCP_ACTION_DOCKYARD_TOOLTIP": _row(
        "Add three dockyards to every coastal state you own.",
        "Fügt jedem Ihrer Küstenstaaten drei Werften hinzu.",
        "Ajoute trois chantiers navals à chacun de vos États côtiers.",
        "Добавляет три верфи в каждую вашу прибрежную провинцию.",
        "Sahip olduğunuz her kıyı eyaletine üç tersane ekler.",
        "Voegt drie scheepswerven toe aan elke kuststaat die je bezit.",
    ),
    "CCP_ACTION_AIRBASE": _row(
        "+10 AIR BASE", "+10 FLUGPLATZ", "+10 BASE AÉR.", "+10 АЭРОДРОМ", "+10 HAVA ÜSSÜ", "+10 VLIEGBASIS"
    ),
    "CCP_ACTION_AIRBASE_HELP": _row(
        "Add ten air base levels to every state you own.",
        "Fügt jedem Ihrer Staaten zehn Flugplatzstufen hinzu.",
        "Ajoute dix niveaux de base aérienne à chacun de vos États.",
        "Добавляет десять уровней аэродрома в каждую вашу провинцию.",
        "Her eyaletinize on seviye hava üssü ekler.",
        "Voegt tien vliegbasisniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_AIRBASE_TOOLTIP": _row(
        "Add ten air base levels to every state you own.",
        "Fügt jedem Ihrer Staaten zehn Flugplatzstufen hinzu.",
        "Ajoute dix niveaux de base aérienne à chacun de vos États.",
        "Добавляет десять уровней аэродрома в каждую вашу провинцию.",
        "Her eyaletinize on seviye hava üssü ekler.",
        "Voegt tien vliegbasisniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_RADAR": _row(
        "+3 RADAR", "+3 RADAR", "+3 RADAR", "+3 РАДАР", "+3 RADAR", "+3 RADAR"
    ),
    "CCP_ACTION_RADAR_HELP": _row(
        "Add three radar levels to every state you own.",
        "Fügt jedem Ihrer Staaten drei Radarstufen hinzu.",
        "Ajoute trois niveaux de radar à chacun de vos États.",
        "Добавляет три уровня радара в каждую вашу провинцию.",
        "Her eyaletinize üç seviye radar ekler.",
        "Voegt drie radarniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_RADAR_TOOLTIP": _row(
        "Add three radar levels to every state you own.",
        "Fügt jedem Ihrer Staaten drei Radarstufen hinzu.",
        "Ajoute trois niveaux de radar à chacun de vos États.",
        "Добавляет три уровня радара в каждую вашу провинцию.",
        "Her eyaletinize üç seviye radar ekler.",
        "Voegt drie radarniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_ANTIAIR": _row(
        "+3 ANTI-AIR", "+3 FLUGABWEHR", "+3 ANTIAÉRIEN", "+3 ПВО", "+3 UÇAKSAVAR", "+3 LUCHTAFWEER"
    ),
    "CCP_ACTION_ANTIAIR_HELP": _row(
        "Add three anti-air levels to every state you own.",
        "Fügt jedem Ihrer Staaten drei Flugabwehrstufen hinzu.",
        "Ajoute trois niveaux antiaériens à chacun de vos États.",
        "Добавляет три уровня ПВО в каждую вашу провинцию.",
        "Her eyaletinize üç seviye uçaksavar ekler.",
        "Voegt drie luchtafweerniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_ANTIAIR_TOOLTIP": _row(
        "Add three anti-air levels to every state you own.",
        "Fügt jedem Ihrer Staaten drei Flugabwehrstufen hinzu.",
        "Ajoute trois niveaux antiaériens à chacun de vos États.",
        "Добавляет три уровня ПВО в каждую вашу провинцию.",
        "Her eyaletinize üç seviye uçaksavar ekler.",
        "Voegt drie luchtafweerniveaus toe aan elke staat die je bezit.",
    ),
    "CCP_ACTION_OFFSITE_CIVILIAN": _row(
        "+20 OFFSITE CIV", "+20 EXTERN ZIVIL", "+20 HORS SITE CIV", "+20 ВНЕ КАРТЫ ГРАЖД", "+20 HARİCİ SİVİL", "+20 EXTERN CIVIEL"
    ),
    "CCP_ACTION_OFFSITE_CIVILIAN_HELP": _row(
        "Add twenty civilian factories that sit outside the map and cannot be bombed.",
        "Fügt zwanzig Zivilfabriken hinzu, die ausserhalb der Karte liegen und nicht bombardiert werden können.",
        "Ajoute vingt usines civiles hors carte, à l'abri des bombardements.",
        "Добавляет двадцать гражданских заводов вне карты — их нельзя бомбить.",
        "Harita dışında duran ve bombalanamayan yirmi sivil fabrika ekler.",
        "Voegt twintig civiele fabrieken buiten de kaart toe die niet gebombardeerd kunnen worden.",
    ),
    "CCP_ACTION_OFFSITE_CIVILIAN_TOOLTIP": _row(
        "Add twenty civilian factories that sit outside the map and cannot be bombed.",
        "Fügt zwanzig Zivilfabriken hinzu, die ausserhalb der Karte liegen und nicht bombardiert werden können.",
        "Ajoute vingt usines civiles hors carte, à l'abri des bombardements.",
        "Добавляет двадцать гражданских заводов вне карты — их нельзя бомбить.",
        "Harita dışında duran ve bombalanamayan yirmi sivil fabrika ekler.",
        "Voegt twintig civiele fabrieken buiten de kaart toe die niet gebombardeerd kunnen worden.",
    ),
    "CCP_ACTION_OFFSITE_MILITARY": _row(
        "+20 OFFSITE MIL", "+20 EXTERN MILITÄR", "+20 HORS SITE MIL", "+20 ВНЕ КАРТЫ ВОЕН", "+20 HARİCİ ASKERİ", "+20 EXTERN MILITAIR"
    ),
    "CCP_ACTION_OFFSITE_MILITARY_HELP": _row(
        "Add twenty military factories that sit outside the map and cannot be bombed.",
        "Fügt zwanzig Militärfabriken hinzu, die ausserhalb der Karte liegen und nicht bombardiert werden können.",
        "Ajoute vingt usines militaires hors carte, à l'abri des bombardements.",
        "Добавляет двадцать военных заводов вне карты — их нельзя бомбить.",
        "Harita dışında duran ve bombalanamayan yirmi askeri fabrika ekler.",
        "Voegt twintig militaire fabrieken buiten de kaart toe die niet gebombardeerd kunnen worden.",
    ),
    "CCP_ACTION_OFFSITE_MILITARY_TOOLTIP": _row(
        "Add twenty military factories that sit outside the map and cannot be bombed.",
        "Fügt zwanzig Militärfabriken hinzu, die ausserhalb der Karte liegen und nicht bombardiert werden können.",
        "Ajoute vingt usines militaires hors carte, à l'abri des bombardements.",
        "Добавляет двадцать военных заводов вне карты — их нельзя бомбить.",
        "Harita dışında duran ve bombalanamayan yirmi askeri fabrika ekler.",
        "Voegt twintig militaire fabrieken buiten de kaart toe die niet gebombardeerd kunnen worden.",
    ),
    "CCP_ACTION_ARMY_XP": _row(
        "+1 GENERAL SKILL", "+1 GENERALSSTUFE", "+1 NIVEAU GÉNÉRAL", "+1 УРОВЕНЬ ГЕН.", "+1 GENERAL SEVİYESİ", "+1 GENERAALNIVEAU"
    ),
    "CCP_ACTION_ARMY_XP_HELP": _row(
        "Raise every general one skill level.",
        "Erhöht jeden General um eine Fähigkeitsstufe.",
        "Augmente chaque général d'un niveau de compétence.",
        "Повышает каждого генерала на один уровень навыка.",
        "Her generalin beceri seviyesini bir artırır.",
        "Verhoogt elke generaal met één vaardigheidsniveau.",
    ),
    "CCP_ACTION_ARMY_XP_TOOLTIP": _row(
        "Raise every general one skill level.",
        "Erhöht jeden General um eine Fähigkeitsstufe.",
        "Augmente chaque général d'un niveau de compétence.",
        "Повышает каждого генерала на один уровень навыка.",
        "Her generalin beceri seviyesini bir artırır.",
        "Verhoogt elke generaal met één vaardigheidsniveau.",
    ),
    "CCP_ACTION_NAVY_XP": _row(
        "+1 ADMIRAL SKILL", "+1 ADMIRALSSTUFE", "+1 NIVEAU AMIRAL", "+1 УРОВЕНЬ АДМ.", "+1 AMİRAL SEVİYESİ", "+1 ADMIRAALNIVEAU"
    ),
    "CCP_ACTION_NAVY_XP_HELP": _row(
        "Raise every admiral one skill level.",
        "Erhöht jeden Admiral um eine Fähigkeitsstufe.",
        "Augmente chaque amiral d'un niveau de compétence.",
        "Повышает каждого адмирала на один уровень навыка.",
        "Her amiralin beceri seviyesini bir artırır.",
        "Verhoogt elke admiraal met één vaardigheidsniveau.",
    ),
    "CCP_ACTION_NAVY_XP_TOOLTIP": _row(
        "Raise every admiral one skill level.",
        "Erhöht jeden Admiral um eine Fähigkeitsstufe.",
        "Augmente chaque amiral d'un niveau de compétence.",
        "Повышает каждого адмирала на один уровень навыка.",
        "Her amiralin beceri seviyesini bir artırır.",
        "Verhoogt elke admiraal met één vaardigheidsniveau.",
    ),
    "CCP_ACTION_ATTACK": _row(
        "+1 ATTACK", "+1 ANGRIFF", "+1 ATTAQUE", "+1 АТАКА", "+1 SALDIRI", "+1 AANVAL"
    ),
    "CCP_ACTION_ATTACK_HELP": _row(
        "Raise the attack skill of every general.",
        "Erhöht den Angriffswert jedes Generals.",
        "Augmente la compétence d'attaque de chaque général.",
        "Повышает навык атаки каждого генерала.",
        "Her generalin saldırı becerisini artırır.",
        "Verhoogt de aanvalsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_ATTACK_TOOLTIP": _row(
        "Raise the attack skill of every general.",
        "Erhöht den Angriffswert jedes Generals.",
        "Augmente la compétence d'attaque de chaque général.",
        "Повышает навык атаки каждого генерала.",
        "Her generalin saldırı becerisini artırır.",
        "Verhoogt de aanvalsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_DEFENSE": _row(
        "+1 DEFENSE", "+1 VERTEIDIGUNG", "+1 DÉFENSE", "+1 ЗАЩИТА", "+1 SAVUNMA", "+1 VERDEDIGING"
    ),
    "CCP_ACTION_DEFENSE_HELP": _row(
        "Raise the defence skill of every general.",
        "Erhöht den Verteidigungswert jedes Generals.",
        "Augmente la compétence de défense de chaque général.",
        "Повышает навык защиты каждого генерала.",
        "Her generalin savunma becerisini artırır.",
        "Verhoogt de verdedigingsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_DEFENSE_TOOLTIP": _row(
        "Raise the defence skill of every general.",
        "Erhöht den Verteidigungswert jedes Generals.",
        "Augmente la compétence de défense de chaque général.",
        "Повышает навык защиты каждого генерала.",
        "Her generalin savunma becerisini artırır.",
        "Verhoogt de verdedigingsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_PLANNING": _row(
        "+1 PLANNING", "+1 PLANUNG", "+1 PLANIFICATION", "+1 ПЛАНИРОВАНИЕ", "+1 PLANLAMA", "+1 PLANNING"
    ),
    "CCP_ACTION_PLANNING_HELP": _row(
        "Raise the planning skill of every general.",
        "Erhöht den Planungswert jedes Generals.",
        "Augmente la compétence de planification de chaque général.",
        "Повышает навык планирования каждого генерала.",
        "Her generalin planlama becerisini artırır.",
        "Verhoogt de planningsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_PLANNING_TOOLTIP": _row(
        "Raise the planning skill of every general.",
        "Erhöht den Planungswert jedes Generals.",
        "Augmente la compétence de planification de chaque général.",
        "Повышает навык планирования каждого генерала.",
        "Her generalin planlama becerisini artırır.",
        "Verhoogt de planningsvaardigheid van elke generaal.",
    ),
    "CCP_ACTION_LOGISTICS": _row(
        "+1 LOGISTICS", "+1 LOGISTIK", "+1 LOGISTIQUE", "+1 ЛОГИСТИКА", "+1 LOJİSTİK", "+1 LOGISTIEK"
    ),
    "CCP_ACTION_LOGISTICS_HELP": _row(
        "Raise the logistics skill of every general.",
        "Erhöht den Logistikwert jedes Generals.",
        "Augmente la compétence logistique de chaque général.",
        "Повышает навык логистики каждого генерала.",
        "Her generalin lojistik becerisini artırır.",
        "Verhoogt de logistieke vaardigheid van elke generaal.",
    ),
    "CCP_ACTION_LOGISTICS_TOOLTIP": _row(
        "Raise the logistics skill of every general.",
        "Erhöht den Logistikwert jedes Generals.",
        "Augmente la compétence logistique de chaque général.",
        "Повышает навык логистики каждого генерала.",
        "Her generalin lojistik becerisini artırır.",
        "Verhoogt de logistieke vaardigheid van elke generaal.",
    ),
    "CCP_HISTORY_HELP": _row(
        "This panel calls the game's own effects rather than typing console commands, so what is recorded here is the action, not a command line. Repeat runs it again exactly as before.",
        "Dieses Panel ruft die Spieleffekte direkt auf, statt Konsolenbefehle zu tippen; aufgezeichnet wird daher die Aktion, keine Befehlszeile. Wiederholen führt sie erneut aus.",
        "Ce panneau appelle les effets du jeu au lieu de taper des commandes console : ce qui est enregistré est l'action, pas une ligne de commande. Répéter la relance à l'identique.",
        "Панель вызывает эффекты игры напрямую, а не набирает консольные команды, поэтому здесь записано действие, а не строка команды. Повтор выполняет его снова.",
        "Bu panel konsol komutu yazmak yerine oyunun kendi efektlerini çağırır; burada kaydedilen şey komut satırı değil, işlemin kendisidir. Tekrarla aynı işlemi yeniden çalıştırır.",
        "Dit paneel roept de effecten van het spel aan in plaats van consolecommando's te typen, dus wat hier staat is de actie, geen commandoregel. Herhalen voert die opnieuw uit.",
    ),
    "CCP_HISTORY_EMPTY": _row(
        "Empty", "Leer", "Vide", "Пусто", "Boş", "Leeg"
    ),
    "CCP_HISTORY_CLEAR": _row("CLEAR", "LEEREN", "VIDER", "ОЧИСТИТЬ", "TEMİZLE", "WISSEN"),
    "CCP_HISTORY_CLEAR_TOOLTIP": _row(
        "Empty the history. Nothing that was already applied is undone.",
        "Leert den Verlauf. Bereits Ausgeführtes wird nicht rückgängig gemacht.",
        "Vide l'historique. Rien de déjà appliqué n'est annulé.",
        "Очищает историю. Уже выполненное не отменяется.",
        "Geçmişi boşaltır. Zaten uygulanmış hiçbir şey geri alınmaz.",
        "Leegt de geschiedenis. Reeds uitgevoerde acties worden niet ongedaan gemaakt.",
    ),
    "CCP_HISTORY_REPEAT": _row("REPEAT", "ERNEUT", "RÉPÉTER", "ПОВТОР", "TEKRARLA", "HERHAAL"),
    "CCP_HISTORY_REPEAT_TOOLTIP": _row(
        "Run this action again.",
        "Führt diese Aktion erneut aus.",
        "Relance cette action.",
        "Выполняет действие снова.",
        "Bu işlemi yeniden çalıştırır.",
        "Voert deze actie opnieuw uit.",
    ),
    "CCP_SETTINGS_COMPAT": _row(
        "COMPATIBILITY", "KOMPATIBILITÄT", "COMPATIBILITÉ", "СОВМЕСТИМОСТЬ", "UYUMLULUK", "COMPATIBILITEIT"
    ),
    "CCP_SETTINGS_COMPAT_HELP": _row(
        "This mod overrides no vanilla file and every name it defines is prefixed ccp_, so it sits alongside other mods rather than fighting them. It is built for singleplayer: the engine gives script no way to detect a multiplayer session, so nothing here can be hidden automatically, and country switching, annexation and state transfers can desync a multiplayer game.",
        "Dieser Mod überschreibt keine Vanilla-Datei und alle Bezeichner beginnen mit ccp_, er steht also neben anderen Mods, statt mit ihnen zu kollidieren. Er ist für den Einzelspieler gedacht: Skript kann eine Mehrspielerpartie nicht erkennen, also lässt sich hier nichts automatisch ausblenden, und Länderwechsel, Annexionen und Staatsübergaben können eine Mehrspielerpartie desynchronisieren.",
        "Ce mod ne remplace aucun fichier vanilla et tous ses identifiants commencent par ccp_ ; il cohabite donc avec les autres mods. Il est conçu pour le solo : le script ne peut pas détecter une partie multijoueur, rien ne peut donc être masqué automatiquement, et changer de pays, annexer ou transférer des États peut désynchroniser une partie multijoueur.",
        "Мод не переопределяет ванильные файлы, а все его имена начинаются с ccp_, поэтому он уживается с другими модами. Он рассчитан на одиночную игру: скрипт не может определить сетевую сессию, поэтому ничего нельзя скрыть автоматически, а смена страны, аннексия и передача провинций могут вызвать рассинхрон в сетевой игре.",
        "Bu mod hiçbir vanilla dosyasını ezmez ve tanımladığı her ad ccp_ ile başlar; bu yüzden diğer modlarla çakışmak yerine yanlarında durur. Tek oyunculu için tasarlandı: engine, script'e çok oyunculu oturumu tespit etme imkânı vermiyor, dolayısıyla burada hiçbir şey otomatik gizlenemez ve ülke değiştirme, ilhak ve eyalet devri çok oyunculu bir oyunu desenkronize edebilir.",
        "Deze mod overschrijft geen enkel vanilla-bestand en elke naam begint met ccp_, dus hij staat naast andere mods in plaats van ermee te botsen. Hij is voor singleplayer gemaakt: script kan een multiplayersessie niet detecteren, dus niets kan automatisch worden verborgen, en van land wisselen, annexeren en staten overdragen kunnen een multiplayerspel desynchroniseren.",
    ),
    "CCP_IRONMAN_ON": _row(
        "This is an Ironman game. Achievements are already disabled by running any mod, and there is no way to undo what this panel does.",
        "Dies ist eine Ironman-Partie. Erfolge sind durch jeden Mod bereits deaktiviert, und nichts, was dieses Panel tut, lässt sich rückgängig machen.",
        "Cette partie est en Ironman. Les succès sont déjà désactivés par tout mod, et rien de ce que fait ce panneau n'est réversible.",
        "Это игра в режиме Ironman. Достижения уже отключены любым модом, а действия панели необратимы.",
        "Bu bir Ironman oyunu. Herhangi bir mod çalıştırmak başarımları zaten kapatır ve bu panelin yaptıklarının geri dönüşü yoktur.",
        "Dit is een Ironman-spel. Prestaties zijn al uitgeschakeld door elke mod, en wat dit paneel doet is onomkeerbaar.",
    ),
    "CCP_IRONMAN_OFF": _row(
        "Not an Ironman game. Save before large changes if you want a way back.",
        "Keine Ironman-Partie. Vor grossen Änderungen speichern, falls Sie zurückwollen.",
        "Partie hors Ironman. Sauvegardez avant les grandes modifications si vous voulez pouvoir revenir.",
        "Не игра Ironman. Сохранитесь перед крупными изменениями, если хотите иметь путь назад.",
        "Ironman oyunu değil. Geri dönmek isterseniz büyük değişikliklerden önce kaydedin.",
        "Geen Ironman-spel. Sla op vóór grote wijzigingen als je terug wilt kunnen.",
    ),
    "CCP_STATUS_OVERFLOW": _row(
        "Manpower is already near the limit the game can store. Adding more would turn it negative, so nothing was added.",
        "Die Rekruten sind bereits nahe am speicherbaren Maximum. Mehr würde den Wert negativ machen, daher wurde nichts hinzugefügt.",
        "Les effectifs sont déjà proches de la limite que le jeu peut stocker. En ajouter rendrait la valeur négative, rien n a donc été ajouté.",
        "Людские ресурсы уже близки к пределу хранения. Добавление сделало бы значение отрицательным, поэтому ничего не добавлено.",
        "İnsan gücü, oyunun saklayabileceği sınıra çoktan yaklaştı. Daha fazlası değeri negatife çevirir, bu yüzden hiçbir şey eklenmedi.",
        "Manschappen zitten al tegen de opslaggrens aan. Meer toevoegen zou de waarde negatief maken, dus er is niets toegevoegd.",
    ),
    "CCP_EQUIPMENT_ALL": _row(
        "ADD WHOLE CATEGORY",
        "GANZE KATEGORIE",
        "TOUTE LA CATÉGORIE",
        "ВСЮ КАТЕГОРИЮ",
        "TÜM KATEGORİYİ EKLE",
        "HELE CATEGORIE",
    ),
    "CCP_EQUIPMENT_ALL_TOOLTIP": _row(
        "Add the amount above of every item in this category, not just the visible page.",
        "Fügt von jedem Eintrag dieser Kategorie die oben eingestellte Menge hinzu, nicht nur der sichtbaren Seite.",
        "Ajoute la quantité ci-dessus de chaque élément de cette catégorie, pas seulement la page affichée.",
        "Добавляет указанное выше количество каждого предмета категории, а не только видимой страницы.",
        "Bu kategorideki her öğeden yukarıdaki miktarı ekler; yalnızca görünen sayfayı değil.",
        "Voegt van elk item in deze categorie het bovenstaande aantal toe, niet alleen de zichtbare pagina.",
    ),
    "CCP_EQUIPMENT_ALL_HELP": _row(
        "Uses the amount from the pad on the right.",
        "Nutzt die Menge aus dem Feld rechts.",
        "Utilise la quantité du pavé de droite.",
        "Использует количество из панели справа.",
        "Sağdaki tuş takımındaki miktarı kullanır.",
        "Gebruikt het aantal uit het paneel rechts.",
    ),
    "CCP_EQUIPMENT_STOCK_TOOLTIP": _row(
        "How many of this equipment your country holds right now.",
        "Wie viele dieser Ausrüstung Ihr Land derzeit besitzt.",
        "Combien de cet équipement votre pays possède actuellement.",
        "Сколько этого снаряжения у вашей страны сейчас.",
        "Ülkenizin şu anda elinde bu teçhizattan kaç adet olduğu.",
        "Hoeveel van deze uitrusting je land nu heeft.",
    ),
    "CCP_STATUS_CATEGORY": _row(
        "Added [?ccp_amount|0] of every item in [CCP_GetEquipmentCategoryName].",
        "Von jedem Eintrag in [CCP_GetEquipmentCategoryName] wurden [?ccp_amount|0] hinzugefügt.",
        "[?ccp_amount|0] de chaque élément de [CCP_GetEquipmentCategoryName] ajoutés.",
        "Добавлено по [?ccp_amount|0] каждого предмета в разделе [CCP_GetEquipmentCategoryName].",
        "[CCP_GetEquipmentCategoryName] içindeki her öğeden [?ccp_amount|0] adet eklendi.",
        "Van elk item in [CCP_GetEquipmentCategoryName] zijn er [?ccp_amount|0] toegevoegd.",
    ),
    "CCP_STATUS_SELECTION": _row(
        "Nothing was selected, so nothing was added. Pick a category first, then use a row.",
        "Es war nichts ausgewählt, also wurde nichts hinzugefügt. Erst eine Kategorie wählen, dann eine Zeile.",
        "Rien n était sélectionné, donc rien n a été ajouté. Choisissez d abord une catégorie, puis une ligne.",
        "Ничего не было выбрано, поэтому ничего не добавлено. Сначала выберите категорию, затем строку.",
        "Hiçbir şey seçili değildi, bu yüzden hiçbir şey eklenmedi. Önce bir kategori seçin, sonra bir satır kullanın.",
        "Er was niets geselecteerd, dus er is niets toegevoegd. Kies eerst een categorie en dan een rij.",
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
    "equipment": _row(
        "Equipment", "Ausrüstung", "Équipement", "Снаряжение", "Teçhizat", "Uitrusting"
    ),
    "research": _row(
        "Research", "Forschung", "Recherche", "Исследования", "Araştırma", "Onderzoek"
    ),
    "country": _row(
        "Countries", "Länder", "Pays", "Страны", "Ülkeler", "Landen"
    ),
    "states": _row(
        "States", "Staaten", "États", "Провинции", "Eyaletler", "Staten"
    ),
    "nation": _row(
        "Nation", "Nation", "Nation", "Держава", "Ulus", "Natie"
    ),
    "construction": _row(
        "Construction", "Bau", "Construction", "Строительство", "İnşaat", "Bouw"
    ),
    "commanders": _row(
        "Commanders", "Befehlshaber", "Commandants", "Командующие", "Komutanlar", "Bevelhebbers"
    ),
    "history": _row(
        "History", "Verlauf", "Historique", "История", "Geçmiş", "Geschiedenis"
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
    "equipment": _row(
        "Add any equipment in your installation to the stockpile.",
        "Fügt dem Lager jede in Ihrer Installation vorhandene Ausrüstung hinzu.",
        "Ajoute au stock n'importe quel équipement présent dans votre installation.",
        "Добавляет на склад любое снаряжение из вашей установки.",
        "Kurulumunuzdaki her teçhizatı stoğa ekler.",
        "Voegt elke uitrusting uit je installatie toe aan de voorraad.",
    ),
    "research": _row(
        "Grant technologies one at a time or a whole research folder at once.",
        "Vergibt Technologien einzeln oder einen ganzen Forschungsordner auf einmal.",
        "Accorde des technologies une par une ou un dossier de recherche entier.",
        "Выдаёт технологии по одной или целую папку исследований сразу.",
        "Teknolojileri tek tek ya da bir araştırma klasörünü topluca verir.",
        "Kent technologieën één voor één of een hele onderzoeksmap in één keer toe.",
    ),
    "country": _row(
        "Annex, puppet, declare war on or switch to any country in the game.",
        "Annektieren, zum Marionettenstaat machen, Krieg erklären oder zu einem Land wechseln.",
        "Annexer, vassaliser, déclarer la guerre ou incarner un pays.",
        "Аннексировать, сделать марионеткой, объявить войну или переключиться на любую страну.",
        "Herhangi bir ülkeyi ilhak edin, kukla yapın, savaş ilan edin veya o ülkeye geçin.",
        "Annexeer, maak vazal, verklaar de oorlog of speel verder als een ander land.",
    ),
    "states": _row(
        "Take states, add or remove cores, and add claims.",
        "Staaten übernehmen, Kerngebiete setzen oder entfernen und Ansprüche erheben.",
        "Prendre des États, ajouter ou retirer des territoires nationaux, revendiquer.",
        "Забирать провинции, добавлять и снимать коренные территории, выдвигать притязания.",
        "Eyalet alın, core ekleyip kaldırın ve hak talebi oluşturun.",
        "Neem staten over, voeg kerngebied toe of verwijder het, en claim.",
    ),
    "nation": _row(
        "Stability, war support, research slots and fuel.",
        "Stabilität, Kriegsunterstützung, Forschungsplätze und Treibstoff.",
        "Stabilité, soutien à la guerre, emplacements de recherche et carburant.",
        "Стабильность, поддержка войны, слоты исследований и топливо.",
        "İstikrar, savaş desteği, araştırma yuvaları ve yakıt.",
        "Stabiliteit, oorlogssteun, onderzoeksplekken en brandstof.",
    ),
    "construction": _row(
        "Build instantly across every state you own.",
        "Baut sofort in jedem Ihrer Staaten.",
        "Construit instantanément dans tous vos États.",
        "Мгновенно строит во всех ваших провинциях.",
        "Sahip olduğunuz her eyalette anında inşa eder.",
        "Bouwt direct in elke staat die je bezit.",
    ),
    "commanders": _row(
        "Raise the skills of every general and admiral you have.",
        "Erhöht die Fähigkeiten aller Ihrer Generäle und Admirale.",
        "Améliore les compétences de tous vos généraux et amiraux.",
        "Повышает навыки всех ваших генералов и адмиралов.",
        "Tüm generallerinizin ve amirallerinizin becerilerini artırır.",
        "Verhoogt de vaardigheden van al je generaals en admiraals.",
    ),
    "history": _row(
        "The last ten actions this panel applied, each repeatable.",
        "Die letzten zehn Aktionen dieses Panels, jede wiederholbar.",
        "Les dix dernières actions du panneau, toutes répétables.",
        "Последние десять действий панели, каждое можно повторить.",
        "Panelin uyguladığı son on işlem, her biri tekrarlanabilir.",
        "De laatste tien acties van dit paneel, elk herhaalbaar.",
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


HISTORY_LENGTH = 10


def all_strings() -> dict[str, Row]:
    strings: dict[str, Row] = {key: _same(value) for key, value in NEUTRAL.items()}
    strings.update(TRANSLATED)

    for slot in range(1, HISTORY_LENGTH + 1):
        strings[f"CCP_HISTORY_ENTRY_{slot}"] = _same(f"[CCP_GetHistory{slot}]")

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


def _one_line(key: str, value: str) -> str:
    """A localisation entry must occupy exactly one line.

    Hearts of Iron IV stops reading a file at the first line it cannot parse, so a
    real newline inside a value silently drops every key after it. Line breaks are
    written as the two-character escape the engine reads, and a stray quotation
    mark is rejected here rather than shipped broken.
    """
    if '"' in value:
        raise ValueError(f"{key}: localisation values cannot contain a quotation mark")
    flattened = value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", chr(92) + "n")
    return f' {key}:0 "{flattened}"'


def emit_localisation(language: str) -> str:
    lines = [f"l_{language}:"]
    lines += [_one_line(key, row[language]) for key, row in sorted(all_strings().items())]
    return "\n".join(lines) + "\n"
