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
from .action_strings import help_for, title_for
from .actions import ALL as COUNTRY_ACTIONS, level_id
from .resources import RESOURCES, preset_label
from .sections import HOTKEYS, SECTIONS

Row = dict[str, str]


def _row(english: str, german: str, french: str, russian: str) -> Row:
    return {
        "english": english,
        "german": german,
        "french": french,
        "russian": russian,
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
        "ПАНЕЛЬ УПРАВЛЕНИЯ ЧИТАМИ"
    ),
    "CCP_SUBTITLE": _row(
        "Singleplayer utility for Hearts of Iron IV",
        "Einzelspieler-Werkzeug für Hearts of Iron IV",
        "Utilitaire solo pour Hearts of Iron IV",
        "Инструмент для одиночной игры в Hearts of Iron IV"
    ),
    "CCP_SIDEBAR_HEADING": _row(
        "SECTIONS", "BEREICHE", "SECTIONS", "РАЗДЕЛЫ"
    ),
    "CCP_BUTTON_CLOSE": _row(
        "CLOSE", "SCHLIESSEN", "FERMER", "ЗАКРЫТЬ"
    ),
    "CCP_BUTTON_CANCEL": _row(
        "CANCEL", "ABBRECHEN", "ANNULER", "ОТМЕНА"
    ),
    "CCP_BUTTON_CONFIRM": _row(
        "CONFIRM", "BESTÄTIGEN", "CONFIRMER", "ПОДТВЕРДИТЬ"
    ),
    "CCP_BUTTON_CUSTOM": _row(
        "CUSTOM", "EIGENER", "PERSO", "СВОЁ"
    ),
    "CCP_TOOLTIP_CLOSE": _row(
        "Close the panel (Esc). The hotkey reopens it at any time.",
        "Schließt das Panel (Esc). Die Taste öffnet es jederzeit wieder.",
        "Ferme le panneau (Échap). Le raccourci le rouvre à tout moment.",
        "Закрывает панель (Esc). Горячая клавиша откроет её снова."
    ),
    "CCP_TOOLTIP_LAUNCHER": _row(
        "Open the Cheat Control Panel.\\nHotkey: [CCP_GetHotkeyName] — change it in Settings.",
        "Öffnet das Cheat-Kontrollpanel.\\nTaste: [CCP_GetHotkeyName] — änderbar unter Einstellungen.",
        "Ouvre le panneau de triche.\\nRaccourci : [CCP_GetHotkeyName] — modifiable dans Paramètres.",
        "Открывает панель управления читами.\\nКлавиша: [CCP_GetHotkeyName] — меняется в настройках."
    ),
    "CCP_FOOTER_HINT": _row(
        "[CCP_GetHotkeyName] toggles this panel · change the key in Settings",
        "[CCP_GetHotkeyName] schaltet dieses Panel um · Taste unter Einstellungen",
        "[CCP_GetHotkeyName] ouvre et ferme ce panneau · touche modifiable dans Paramètres",
        "[CCP_GetHotkeyName] открывает и закрывает панель · клавиша меняется в настройках"
    ),
    "CCP_STATUS_IDLE": _row(
        f"Cheat Control Panel {MOD_VERSION} · Hearts of Iron IV 1.19 · singleplayer",
        f"Cheat-Kontrollpanel {MOD_VERSION} · Hearts of Iron IV 1.19 · Einzelspieler",
        f"Panneau de triche {MOD_VERSION} · Hearts of Iron IV 1.19 · solo",
        f"Панель управления читами {MOD_VERSION} · Hearts of Iron IV 1.19 · одиночная игра"
    ),
    "CCP_STATUS_HOTKEY": _row(
        "Hotkey set to [CCP_GetHotkeyName].",
        "Taste auf [CCP_GetHotkeyName] gesetzt.",
        "Raccourci défini sur [CCP_GetHotkeyName].",
        "Горячая клавиша: [CCP_GetHotkeyName]."
    ),
    "CCP_STATUS_GRANTED": _row(
        "Granted [?ccp_granted_amount|0] [CCP_GetGrantedResource].",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] hinzugefügt.",
        "[?ccp_granted_amount|0] [CCP_GetGrantedResource] ajouté.",
        "Добавлено: [?ccp_granted_amount|0] [CCP_GetGrantedResource]."
    ),
    "CCP_STATUS_CONFIRM_ON": _row(
        "Confirmation prompts are on for destructive actions.",
        "Bestätigungen für unumkehrbare Aktionen sind aktiv.",
        "Les confirmations sont actives pour les actions irréversibles.",
        "Подтверждение необратимых действий включено."
    ),
    "CCP_STATUS_CONFIRM_OFF": _row(
        "Confirmation prompts are off. Destructive actions apply immediately.",
        "Bestätigungen sind aus. Unumkehrbare Aktionen wirken sofort.",
        "Les confirmations sont désactivées. Les actions irréversibles s'appliquent aussitôt.",
        "Подтверждение выключено. Необратимые действия применяются сразу."
    ),
    "CCP_CONFIRM_ON": _row(
        "CONFIRMATIONS: ON",
        "BESTÄTIGUNGEN: AN",
        "CONFIRMATIONS : ACTIVÉES",
        "ПОДТВЕРЖДЕНИЕ: ВКЛ"
    ),
    "CCP_CONFIRM_OFF": _row(
        "CONFIRMATIONS: OFF",
        "BESTÄTIGUNGEN: AUS",
        "CONFIRMATIONS : DÉSACTIVÉES",
        "ПОДТВЕРЖДЕНИЕ: ВЫКЛ"
    ),
    "CCP_SETTINGS_HOTKEY": _row(
        "HOTKEY", "TASTENKÜRZEL", "RACCOURCI", "ГОРЯЧАЯ КЛАВИША"
    ),
    "CCP_SETTINGS_HOTKEY_HELP": _row(
        "Choose the key that opens and closes this panel. The choice is saved with your game.",
        "Wählen Sie die Taste, die dieses Panel öffnet und schließt. Die Wahl wird im Spielstand gespeichert.",
        "Choisissez la touche qui ouvre et ferme ce panneau. Le choix est enregistré dans la partie.",
        "Выберите клавишу для открытия и закрытия панели. Выбор сохраняется вместе с игрой."
    ),
    "CCP_SETTINGS_HOTKEY_CURRENT": _row(
        "Current hotkey: [CCP_GetHotkeyName]",
        "Aktuelle Taste: [CCP_GetHotkeyName]",
        "Raccourci actuel : [CCP_GetHotkeyName]",
        "Текущая клавиша: [CCP_GetHotkeyName]"
    ),
    "CCP_SETTINGS_CONFIRM": _row(
        "CONFIRMATIONS",
        "BESTÄTIGUNGEN",
        "CONFIRMATIONS",
        "ПОДТВЕРЖДЕНИЕ"
    ),
    "CCP_SETTINGS_CONFIRM_HELP": _row(
        "Destructive actions ask before they apply. There is no undo, so leaving this on is safer.",
        "Unumkehrbare Aktionen fragen vorher nach. Es gibt kein Rückgängig, daher ist Anlassen sicherer.",
        "Les actions irréversibles demandent confirmation. Il n'y a pas d'annulation, mieux vaut les laisser actives.",
        "Необратимые действия запрашивают подтверждение. Отмены нет, поэтому безопаснее оставить включённым."
    ),
    "CCP_SETTINGS_CONFIRM_TOOLTIP": _row(
        "Toggle the confirmation prompt shown before annexations, state transfers and core removal.",
        "Schaltet die Bestätigung vor Annexionen, Staatsübergaben und dem Entfernen von Kerngebieten um.",
        "Active ou désactive la confirmation avant annexions, transferts d'État et retraits de territoire national.",
        "Включает подтверждение перед аннексией, передачей провинций и снятием коренных территорий."
    ),
    "CCP_SETTINGS_LANGUAGE": _row(
        "LANGUAGE", "SPRACHE", "LANGUE", "ЯЗЫК"
    ),
    "CCP_SETTINGS_LANGUAGE_HELP": _row(
        "The panel follows the game language. English, German, French and Russian ship with the mod. Hearts of Iron IV has no Turkish or Dutch language slot, so those two are installed as an overlay — see the README.",
        "Das Panel folgt der Spielsprache. Englisch, Deutsch, Französisch und Russisch sind enthalten. Hearts of Iron IV hat keinen türkischen oder niederländischen Sprachplatz, daher werden diese beiden als Overlay installiert — siehe README.",
        "Le panneau suit la langue du jeu. Anglais, allemand, français et russe sont inclus. Hearts of Iron IV n'a pas d'emplacement turc ou néerlandais : ces deux langues s'installent en surcouche — voir le README.",
        "Панель следует языку игры. Английский, немецкий, французский и русский входят в мод. В Hearts of Iron IV нет турецкого и нидерландского, поэтому они ставятся наложением — см. README."
    ),
    "CCP_CARD_COUNTRY": _row("COUNTRY", "LAND", "PAYS", "СТРАНА"),
    "CCP_CARD_COUNTRY_TOOLTIP": _row(
        "The country you are currently playing.",
        "Das Land, das Sie gerade spielen.",
        "Le pays que vous jouez actuellement.",
        "Страна, за которую вы играете."
    ),
    "CCP_CARD_PP": _row(
        "POLITICAL POWER", "POLITISCHE MACHT", "POUVOIR POLITIQUE",
        "ПОЛИТИЧЕСКАЯ СИЛА"
    ),
    "CCP_CARD_PP_TOOLTIP": _row(
        "Political power currently in your treasury.",
        "Aktuell verfügbare politische Macht.",
        "Pouvoir politique actuellement disponible.",
        "Доступная политическая сила."
    ),
    "CCP_CARD_CP": _row(
        "COMMAND POWER", "KOMMANDOPUNKTE", "POINTS DE COMMANDEMENT",
        "ОЧКИ КОМАНДОВАНИЯ"
    ),
    "CCP_CARD_CP_TOOLTIP": _row(
        "Command power available for army abilities.",
        "Kommandopunkte für Armeefähigkeiten.",
        "Points de commandement disponibles pour les capacités d'armée.",
        "Очки командования для армейских способностей."
    ),
    "CCP_CARD_MANPOWER": _row(
        "MANPOWER", "REKRUTEN", "EFFECTIFS", "ЛЮДСКИЕ РЕСУРСЫ"
    ),
    "CCP_CARD_MANPOWER_TOOLTIP": _row(
        "Manpower available for deployment and reinforcement.",
        "Verfügbare Rekruten für Aufstellung und Verstärkung.",
        "Effectifs disponibles pour le déploiement et le renfort.",
        "Людские ресурсы для развёртывания и пополнения."
    ),
    "CCP_CARD_ARMY_XP": _row(
        "ARMY XP", "HEERES-EP", "XP TERRESTRE", "ОПЫТ АРМИИ"
    ),
    "CCP_CARD_ARMY_XP_TOOLTIP": _row(
        "Army experience, spent on division templates.",
        "Heereserfahrung, für Divisionsvorlagen.",
        "Expérience terrestre, dépensée sur les modèles de division.",
        "Опыт армии, тратится на шаблоны дивизий."
    ),
    "CCP_CARD_NAVY_XP": _row(
        "NAVY XP", "MARINE-EP", "XP NAVALE", "ОПЫТ ФЛОТА"
    ),
    "CCP_CARD_NAVY_XP_TOOLTIP": _row(
        "Navy experience, spent on ship designs.",
        "Marineerfahrung, für Schiffsentwürfe.",
        "Expérience navale, dépensée sur les modèles de navire.",
        "Опыт флота, тратится на проекты кораблей."
    ),
    "CCP_CARD_AIR_XP": _row(
        "AIR XP", "LUFTWAFFEN-EP", "XP AÉRIENNE", "ОПЫТ АВИАЦИИ"
    ),
    "CCP_CARD_AIR_XP_TOOLTIP": _row(
        "Air experience, spent on aircraft designs.",
        "Luftwaffenerfahrung, für Flugzeugentwürfe.",
        "Expérience aérienne, dépensée sur les modèles d'avion.",
        "Опыт авиации, тратится на проекты самолётов."
    ),
    "CCP_CARD_STABILITY": _row(
        "STABILITY", "STABILITÄT", "STABILITÉ", "СТАБИЛЬНОСТЬ"
    ),
    "CCP_CARD_STABILITY_TOOLTIP": _row(
        "National stability.",
        "Nationale Stabilität.",
        "Stabilité nationale.",
        "Стабильность страны."
    ),
    "CCP_CARD_FACTORIES": _row(
        "FACTORIES", "FABRIKEN", "USINES", "ЗАВОДЫ"
    ),
    "CCP_CARD_FACTORIES_VALUE": _row(
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] dock",
        "[?num_of_civilian_factories|0] zivil · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] Werft",
        "[?num_of_civilian_factories|0] civ · [?num_of_military_factories|0] mil · [?num_of_naval_factories|0] chant",
        "[?num_of_civilian_factories|0] гражд · [?num_of_military_factories|0] воен · [?num_of_naval_factories|0] верфь"
    ),
    "CCP_CARD_FACTORIES_TOOLTIP": _row(
        "Civilian factories, military factories and dockyards.",
        "Zivile Fabriken, Militärfabriken und Werften.",
        "Usines civiles, usines militaires et chantiers navals.",
        "Гражданские заводы, военные заводы и верфи."
    ),
    "CCP_EQUIPMENT_CATEGORIES": _row(
        "CATEGORIES", "KATEGORIEN", "CATÉGORIES", "КАТЕГОРИИ"
    ),
    "CCP_EQUIPMENT_CATEGORY_TOOLTIP": _row(
        "Show the equipment in this category.",
        "Zeigt die Ausrüstung dieser Kategorie.",
        "Affiche l'équipement de cette catégorie.",
        "Показать снаряжение этой категории."
    ),
    "CCP_EQUIPMENT_ADD": _row("ADD", "HINZU", "AJOUTER", "ДОБАВ"),
    "CCP_EQUIPMENT_READY": _row(
        "Ready to add.", "Bereit zum Hinzufügen.", "Prêt à ajouter.",
        "Готово к добавлению."
    ),
    "CCP_EQUIPMENT_ADD_TOOLTIP": _row(
        "Add the custom amount of this equipment to your stockpile.\n[CCP_GetEquipmentRequirement]",
        "Fügt die eingestellte Menge dieser Ausrüstung dem Lager hinzu.\n[CCP_GetEquipmentRequirement]",
        "Ajoute au stock la quantité définie de cet équipement.\n[CCP_GetEquipmentRequirement]",
        "Добавляет на склад заданное количество этого снаряжения.\n[CCP_GetEquipmentRequirement]"
    ),
    "CCP_EQUIPMENT_LATEST": _row("LATEST", "NEUSTE", "RÉCENT", "НОВОЕ"),
    "CCP_EQUIPMENT_LATEST_TOOLTIP": _row(
        "Add the newest variant of this equipment line instead of this one.",
        "Fügt statt dieser die neuste Variante dieser Ausrüstungslinie hinzu.",
        "Ajoute la variante la plus récente de cette lignée plutôt que celle-ci.",
        "Добавляет новейший вариант этой линейки вместо выбранного."
    ),
    "CCP_EQUIPMENT_PREV": _row("PREV", "ZURÜCK", "PRÉC", "НАЗАД"),
    "CCP_EQUIPMENT_PREV_TOOLTIP": _row(
        "Show the previous page of this category.",
        "Zeigt die vorherige Seite dieser Kategorie.",
        "Affiche la page précédente de cette catégorie.",
        "Показать предыдущую страницу категории."
    ),
    "CCP_EQUIPMENT_NEXT": _row("NEXT", "WEITER", "SUIV", "ДАЛЕЕ"),
    "CCP_EQUIPMENT_NEXT_TOOLTIP": _row(
        "Show the next page of this category.",
        "Zeigt die nächste Seite dieser Kategorie.",
        "Affiche la page suivante de cette catégorie.",
        "Показать следующую страницу категории."
    ),
    "CCP_EQUIPMENT_PAGE": _row(
        "Page [?ccp_equipment_page_shown|+0] of [?ccp_equipment_pages_shown|+0]",
        "Seite [?ccp_equipment_page_shown|+0] von [?ccp_equipment_pages_shown|+0]",
        "Page [?ccp_equipment_page_shown|+0] sur [?ccp_equipment_pages_shown|+0]",
        "Страница [?ccp_equipment_page_shown|+0] из [?ccp_equipment_pages_shown|+0]"
    ),
    "CCP_EQUIPMENT_UNKNOWN": _row(
        "Unknown equipment", "Unbekannte Ausrüstung", "Équipement inconnu",
        "Неизвестное снаряжение"
    ),
    "CCP_STATUS_EQUIPMENT": _row(
        "Added [?ccp_amount|0] × [CCP_GetEquipmentSelectedName].",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] hinzugefügt.",
        "[?ccp_amount|0] × [CCP_GetEquipmentSelectedName] ajouté.",
        "Добавлено: [?ccp_amount|0] × [CCP_GetEquipmentSelectedName]."
    ),
    "CCP_RESEARCH_GRANT": _row(
        "RESEARCH", "ERFORSCHEN", "RECHERCHER", "ИЗУЧИТЬ"
    ),
    "CCP_RESEARCH_GRANT_TOOLTIP": _row(
        "Complete this technology immediately.",
        "Schliesst diese Technologie sofort ab.",
        "Termine cette technologie immédiatement.",
        "Мгновенно завершает эту технологию."
    ),
    "CCP_RESEARCH_ALL": _row(
        "THIS CATEGORY",
        "DIESE KATEGORIE",
        "CETTE CATÉGORIE",
        "ЭТУ КАТЕГОРИЮ"
    ),
    "CCP_RESEARCH_ALL_TOOLTIP": _row(
        "Complete every technology in the selected category, across all its pages.",
        "Schliesst jede Technologie der gewählten Kategorie ab, über alle Seiten hinweg.",
        "Termine toutes les technologies de la catégorie choisie, sur toutes ses pages.",
        "Завершает все технологии выбранной категории на всех её страницах."
    ),
    "CCP_RESEARCH_ALL_HELP": _row(
        "Doctrines use a separate system and cannot be granted with this effect.",
        "Doktrinen nutzen ein eigenes System und lassen sich damit nicht vergeben.",
        "Les doctrines utilisent un système distinct et ne peuvent pas être accordées ici.",
        "Доктрины используют отдельную систему и здесь недоступны."
    ),
    "CCP_RESEARCH_PAGE": _row(
        "Page [?ccp_research_page_shown|+0] of [?ccp_research_pages_shown|+0]",
        "Seite [?ccp_research_page_shown|+0] von [?ccp_research_pages_shown|+0]",
        "Page [?ccp_research_page_shown|+0] sur [?ccp_research_pages_shown|+0]",
        "Страница [?ccp_research_page_shown|+0] из [?ccp_research_pages_shown|+0]"
    ),
    "CCP_RESEARCH_UNKNOWN": _row(
        "Unknown technology", "Unbekannte Technologie", "Technologie inconnue",
        "Неизвестная технология"
    ),
    "CCP_STATUS_TECH": _row(
        "Researched [CCP_GetTechnologySelectedName].",
        "[CCP_GetTechnologySelectedName] erforscht.",
        "[CCP_GetTechnologySelectedName] recherché.",
        "Изучено: [CCP_GetTechnologySelectedName]."
    ),
    "CCP_STATUS_FOLDER": _row(
        "Researched every technology in [CCP_GetResearchFolderName].",
        "Jede Technologie in [CCP_GetResearchFolderName] erforscht.",
        "Toutes les technologies de [CCP_GetResearchFolderName] recherchées.",
        "Изучены все технологии в разделе [CCP_GetResearchFolderName]."
    ),
    "CCP_COUNTRY_HELP": _row(
        "Every country that exists in the current game. Destructive actions ask first unless you turned confirmations off.",
        "Jedes im laufenden Spiel existierende Land. Unumkehrbare Aktionen fragen nach, sofern Bestätigungen aktiv sind.",
        "Tous les pays existants dans la partie. Les actions irréversibles demandent confirmation si elle est activée.",
        "Все существующие в текущей игре страны. Необратимые действия запрашивают подтверждение, если оно включено."
    ),
    "CCP_COUNTRY_ENTRY_NAME": _row(
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])",
        "[THIS.GetNameDefCap] ([THIS.GetTag])"
    ),
    "CCP_COUNTRY_PAGE": _row(
        "Page [?ccp_country_page_shown|+0] of [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] countries",
        "Seite [?ccp_country_page_shown|+0] von [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] Länder",
        "Page [?ccp_country_page_shown|+0] sur [?ccp_country_pages_shown|+0] · [?ccp_country_count|0] pays",
        "Страница [?ccp_country_page_shown|+0] из [?ccp_country_pages_shown|+0] · стран: [?ccp_country_count|0]"
    ),
    "CCP_COUNTRY_ANNEX": _row("ANNEX", "ANNEKT.", "ANNEXER", "АННЕКС"),
    "CCP_COUNTRY_ANNEX_TOOLTIP": _row(
        "Annex this country. There is no undo.",
        "Annektiert dieses Land. Es gibt kein Rückgängig.",
        "Annexe ce pays. Aucune annulation possible.",
        "Аннексирует страну. Отменить нельзя."
    ),
    "CCP_COUNTRY_PUPPET": _row("PUPPET", "MARION.", "VASSAL", "МАРИОН"),
    "CCP_COUNTRY_PUPPET_TOOLTIP": _row(
        "Make this country your puppet.",
        "Macht dieses Land zu Ihrem Marionettenstaat.",
        "Fait de ce pays votre vassal.",
        "Делает страну вашей марионеткой."
    ),
    "CCP_COUNTRY_WAR": _row("WAR", "KRIEG", "GUERRE", "ВОЙНА"),
    "CCP_COUNTRY_WAR_TOOLTIP": _row(
        "Declare war on this country with an annexation war goal.",
        "Erklärt diesem Land den Krieg mit dem Kriegsziel Annexion.",
        "Déclare la guerre à ce pays avec un objectif annexion.",
        "Объявляет войну с целью аннексии."
    ),
    "CCP_COUNTRY_PEACE": _row("PEACE", "FRIEDEN", "PAIX", "МИР"),
    "CCP_COUNTRY_PEACE_TOOLTIP": _row(
        "White peace with this country, if you are at war with it.",
        "Weißer Frieden mit diesem Land, sofern Sie im Krieg sind.",
        "Paix blanche avec ce pays, si vous êtes en guerre.",
        "Белый мир с этой страной, если вы воюете."
    ),
    "CCP_COUNTRY_PLAYAS": _row("PLAY AS", "SPIELEN", "INCARNER", "ИГРАТЬ"),
    "CCP_COUNTRY_PLAYAS_TOOLTIP": _row(
        "Continue the game as this country. The panel closes so the switch can take effect.",
        "Spielt als dieses Land weiter. Das Panel schliesst sich, damit der Wechsel greift.",
        "Poursuit la partie avec ce pays. Le panneau se ferme pour appliquer le changement.",
        "Продолжить игру за эту страну. Панель закроется, чтобы переход сработал."
    ),
    "CCP_MODAL_TITLE": _row(
        "ARE YOU SURE?", "SIND SIE SICHER?", "CONFIRMER ?",
        "ВЫ УВЕРЕНЫ?"
    ),
    "CCP_MODAL_BODY": _row(
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nThis cannot be undone. The engine offers no way to restore the previous state.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nDies lässt sich nicht rückgängig machen. Die Engine bietet keine Wiederherstellung.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nCeci est irréversible. Le moteur ne permet aucune restauration.",
        "[CCP_GetPendingAction] · [?ccp_pending_country.GetNameDefCap]\n\nЭто необратимо. Движок не позволяет восстановить прежнее состояние."
    ),
    "CCP_TOOLTIP_CANCEL": _row(
        "Close this prompt without doing anything.",
        "Schliesst die Abfrage, ohne etwas zu tun.",
        "Ferme cette invite sans rien faire.",
        "Закрывает запрос, ничего не делая."
    ),
    "CCP_TOOLTIP_CONFIRM": _row(
        "Apply the action. This cannot be undone.",
        "Führt die Aktion aus. Nicht rückgängig zu machen.",
        "Applique action. Irréversible.",
        "Применяет действие. Отменить нельзя."
    ),
    "CCP_STATUS_COUNTRY": _row(
        "[CCP_GetPendingAction] applied.",
        "[CCP_GetPendingAction] ausgeführt.",
        "[CCP_GetPendingAction] appliqué.",
        "Выполнено: [CCP_GetPendingAction]."
    ),
    "CCP_STATUS_CANCELLED": _row(
        "Action cancelled. Nothing was changed.",
        "Aktion abgebrochen. Nichts wurde geändert.",
        "Action annulée. Rien modifié.",
        "Действие отменено. Ничего не изменилось."
    ),
    "CCP_STATE_HELP": _row(
        "Every state in the game. You can also turn on map picking and left-click a state directly.",
        "Jeder Staat im Spiel. Alternativ die Kartenauswahl aktivieren und einen Staat anklicken.",
        "Tous les États du jeu. Vous pouvez aussi activer la sélection sur la carte et cliquer un État.",
        "Все провинции в игре. Можно также включить выбор на карте и кликнуть по провинции."
    ),
    "CCP_STATE_PICKER_TOOLTIP": _row(
        "When map picking is on, left-clicking a state shows these actions on the state view.",
        "Bei aktiver Kartenauswahl erscheinen diese Aktionen beim Anklicken eines Staates.",
        "Avec la sélection carte activée, cliquer un État affiche ces actions sur sa vue.",
        "При включённом выборе на карте клик по провинции показывает эти действия."
    ),
    "CCP_STATE_PICKER_ON": _row(
        "MAP PICKING: ON", "KARTENAUSWAHL: AN", "SÉLECTION CARTE : ON",
        "ВЫБОР НА КАРТЕ: ВКЛ"
    ),
    "CCP_STATE_PICKER_OFF": _row(
        "MAP PICKING: OFF", "KARTENAUSWAHL: AUS", "SÉLECTION CARTE : OFF",
        "ВЫБОР НА КАРТЕ: ВЫКЛ"
    ),
    "CCP_STATE_PICKER_TITLE": _row(
        "CHEAT CONTROL PANEL", "CHEAT-KONTROLLPANEL", "PANNEAU DE TRICHE",
        "ПАНЕЛЬ ЧИТОВ"
    ),
    "CCP_STATE_ENTRY_NAME": _row(
        "[THIS.GetName]", "[THIS.GetName]", "[THIS.GetName]",
        "[THIS.GetName]"
    ),
    "CCP_STATE_ENTRY_OWNER": _row(
        "Owner [THIS.Owner.GetNameDefCap] · controller [THIS.Controller.GetNameDefCap]",
        "Besitzer [THIS.Owner.GetNameDefCap] · Kontrolle [THIS.Controller.GetNameDefCap]",
        "Propriétaire [THIS.Owner.GetNameDefCap] · contrôle [THIS.Controller.GetNameDefCap]",
        "Владелец [THIS.Owner.GetNameDefCap] · контроль [THIS.Controller.GetNameDefCap]"
    ),
    "CCP_STATE_PAGE": _row(
        "Page [?ccp_state_page_shown|+0] of [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] states",
        "Seite [?ccp_state_page_shown|+0] von [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] Staaten",
        "Page [?ccp_state_page_shown|+0] sur [?ccp_state_pages_shown|+0] · [?ccp_state_count|0] États",
        "Страница [?ccp_state_page_shown|+0] из [?ccp_state_pages_shown|+0] · провинций: [?ccp_state_count|0]"
    ),
    "CCP_STATE_TAKE": _row("TAKE", "NEHMEN", "PRENDRE", "ЗАБРАТЬ"),
    "CCP_STATE_TAKE_TOOLTIP": _row(
        "Become owner and controller of this state.",
        "Macht Sie zum Besitzer und Kontrolleur dieses Staates.",
        "Vous devenez propriétaire et contrôleur de cet État.",
        "Вы становитесь владельцем и контролёром провинции."
    ),
    "CCP_STATE_OWN": _row("OWN", "BESITZ", "POSSÉDER", "ВЛАДЕТЬ"),
    "CCP_STATE_OWN_TOOLTIP": _row(
        "Become owner of this state and leave the controller alone. This is the console setowner.",
        "Macht Sie zum Besitzer, ohne den Kontrolleur zu ändern. Das ist das Konsolen-setowner.",
        "Vous devenez propriétaire sans changer le contrôleur. C est le setowner de la console.",
        "Вы становитесь владельцем, контролёр не меняется. Это консольное setowner."
    ),
    "CCP_STATE_CONTROL": _row(
        "CONTROL", "KONTROLLE", "CONTRÔLE", "КОНТРОЛЬ"
    ),
    "CCP_STATE_CONTROL_TOOLTIP": _row(
        "Take control of this state and leave the owner alone. This is the console setcontroller.",
        "Übernimmt die Kontrolle, ohne den Besitzer zu ändern. Das ist das Konsolen-setcontroller.",
        "Vous prenez le contrôle sans changer le propriétaire. C est le setcontroller de la console.",
        "Вы получаете контроль, владелец не меняется. Это консольное setcontroller."
    ),
    "CCP_STATE_GIVE_CONTROL": _row(
        "CEDE CTRL", "KTRL ABGEBEN", "CÉDER CTRL", "ОТДАТЬ КТРЛ"
    ),
    "CCP_STATE_GIVE_CONTROL_TOOLTIP": _row(
        "Hand control of this state to the country picked in the Countries section; the owner does not change.",
        "Übergibt die Kontrolle an das im Bereich Länder gewählte Land; der Besitzer bleibt.",
        "Cède le contrôle au pays choisi dans la section Pays ; le propriétaire ne change pas.",
        "Передаёт контроль стране, выбранной в разделе Страны; владелец не меняется."
    ),
    "CCP_STATE_CORE": _row("CORE", "KERN", "CŒUR", "ЯДРО"),
    "CCP_STATE_CORE_TOOLTIP": _row(
        "Add your core to this state.",
        "Fügt Ihr Kerngebiet zu diesem Staat hinzu.",
        "Ajoute votre territoire national sur cet État.",
        "Добавляет вашу коренную территорию."
    ),
    "CCP_STATE_UNCORE": _row("UNCORE", "KERN WEG", "RETIRER", "СНЯТЬ"),
    "CCP_STATE_UNCORE_TOOLTIP": _row(
        "Remove your core from this state. There is no undo.",
        "Entfernt Ihr Kerngebiet. Es gibt kein Rückgängig.",
        "Retire votre territoire national. Aucune annulation.",
        "Снимает вашу коренную территорию. Отменить нельзя."
    ),
    "CCP_STATE_CLAIM": _row("CLAIM", "ANSPRUCH", "REVENDIQ", "ПРИТЯЗ"),
    "CCP_STATE_CLAIM_TOOLTIP": _row(
        "Add your claim to this state.",
        "Erhebt Anspruch auf diesen Staat.",
        "Revendique cet État.",
        "Выдвигает притязание на провинцию."
    ),
    "CCP_STATUS_STATE": _row(
        "State updated.",
        "Staat aktualisiert.",
        "État mis à jour.",
        "Провинция обновлена."
    ),
    "CCP_NATION_HELP": _row(
        "One-click changes to your country as a whole.",
        "Änderungen an Ihrem Land mit einem Klick.",
        "Modifications de votre pays en un clic.",
        "Изменения вашей страны одним нажатием."
    ),
    "CCP_CONSTRUCTION_HELP": _row(
        "Buildings are added to every state you own and finish instantly.",
        "Gebäude werden in jedem Ihrer Staaten ergänzt und sofort fertiggestellt.",
        "Les bâtiments sont ajoutés à tous vos États et achevés instantanément.",
        "Здания добавляются во все ваши провинции и достраиваются мгновенно."
    ),
    "CCP_COMMANDERS_HELP": _row(
        "Applies to every commander you currently have, not to future ones.",
        "Gilt für alle derzeitigen Befehlshaber, nicht für künftige.",
        "S'applique à tous vos commandants actuels, pas aux futurs.",
        "Действует на текущих командующих, но не на будущих."
    ),
    "CCP_STATUS_ACTION": _row(
        "[CCP_GetLastAction] applied.",
        "[CCP_GetLastAction] ausgeführt.",
        "[CCP_GetLastAction] appliqué.",
        "Выполнено: [CCP_GetLastAction]."
    ),
    "CCP_HISTORY_HELP": _row(
        "This panel calls the game's own effects rather than typing console commands, so what is recorded here is the action, not a command line. Repeat runs it again exactly as before.",
        "Dieses Panel ruft die Spieleffekte direkt auf, statt Konsolenbefehle zu tippen; aufgezeichnet wird daher die Aktion, keine Befehlszeile. Wiederholen führt sie erneut aus.",
        "Ce panneau appelle les effets du jeu au lieu de taper des commandes console : ce qui est enregistré est l'action, pas une ligne de commande. Répéter la relance à l'identique.",
        "Панель вызывает эффекты игры напрямую, а не набирает консольные команды, поэтому здесь записано действие, а не строка команды. Повтор выполняет его снова."
    ),
    "CCP_HISTORY_EMPTY": _row(
        "Empty", "Leer", "Vide", "Пусто"
    ),
    "CCP_HISTORY_CLEAR": _row("CLEAR", "LEEREN", "VIDER", "ОЧИСТИТЬ"),
    "CCP_HISTORY_CLEAR_TOOLTIP": _row(
        "Empty the history. Nothing that was already applied is undone.",
        "Leert den Verlauf. Bereits Ausgeführtes wird nicht rückgängig gemacht.",
        "Vide l'historique. Rien de déjà appliqué n'est annulé.",
        "Очищает историю. Уже выполненное не отменяется."
    ),
    "CCP_HISTORY_REPEAT": _row("REPEAT", "ERNEUT", "RÉPÉTER", "ПОВТОР"),
    "CCP_HISTORY_REPEAT_TOOLTIP": _row(
        "Run this action again.",
        "Führt diese Aktion erneut aus.",
        "Relance cette action.",
        "Выполняет действие снова."
    ),
    "CCP_SETTINGS_COMPAT": _row(
        "COMPATIBILITY", "KOMPATIBILITÄT", "COMPATIBILITÉ", "СОВМЕСТИМОСТЬ"
    ),
    "CCP_SETTINGS_COMPAT_HELP": _row(
        "This mod overrides no vanilla file and every name it defines is prefixed ccp_, so it sits alongside other mods rather than fighting them. It is built for singleplayer: the engine gives script no way to detect a multiplayer session, so nothing here can be hidden automatically, and country switching, annexation and state transfers can desync a multiplayer game.",
        "Dieser Mod überschreibt keine Vanilla-Datei und alle Bezeichner beginnen mit ccp_, er steht also neben anderen Mods, statt mit ihnen zu kollidieren. Er ist für den Einzelspieler gedacht: Skript kann eine Mehrspielerpartie nicht erkennen, also lässt sich hier nichts automatisch ausblenden, und Länderwechsel, Annexionen und Staatsübergaben können eine Mehrspielerpartie desynchronisieren.",
        "Ce mod ne remplace aucun fichier vanilla et tous ses identifiants commencent par ccp_ ; il cohabite donc avec les autres mods. Il est conçu pour le solo : le script ne peut pas détecter une partie multijoueur, rien ne peut donc être masqué automatiquement, et changer de pays, annexer ou transférer des États peut désynchroniser une partie multijoueur.",
        "Мод не переопределяет ванильные файлы, а все его имена начинаются с ccp_, поэтому он уживается с другими модами. Он рассчитан на одиночную игру: скрипт не может определить сетевую сессию, поэтому ничего нельзя скрыть автоматически, а смена страны, аннексия и передача провинций могут вызвать рассинхрон в сетевой игре."
    ),
    "CCP_IRONMAN_ON": _row(
        "This is an Ironman game. Achievements are already disabled by running any mod, and there is no way to undo what this panel does.",
        "Dies ist eine Ironman-Partie. Erfolge sind durch jeden Mod bereits deaktiviert, und nichts, was dieses Panel tut, lässt sich rückgängig machen.",
        "Cette partie est en Ironman. Les succès sont déjà désactivés par tout mod, et rien de ce que fait ce panneau n'est réversible.",
        "Это игра в режиме Ironman. Достижения уже отключены любым модом, а действия панели необратимы."
    ),
    "CCP_IRONMAN_OFF": _row(
        "Not an Ironman game. Save before large changes if you want a way back.",
        "Keine Ironman-Partie. Vor grossen Änderungen speichern, falls Sie zurückwollen.",
        "Partie hors Ironman. Sauvegardez avant les grandes modifications si vous voulez pouvoir revenir.",
        "Не игра Ironman. Сохранитесь перед крупными изменениями, если хотите иметь путь назад."
    ),
    "CCP_STATUS_OVERFLOW": _row(
        "Manpower is already near the limit the game can store. Adding more would turn it negative, so nothing was added.",
        "Die Rekruten sind bereits nahe am speicherbaren Maximum. Mehr würde den Wert negativ machen, daher wurde nichts hinzugefügt.",
        "Les effectifs sont déjà proches de la limite que le jeu peut stocker. En ajouter rendrait la valeur négative, rien n a donc été ajouté.",
        "Людские ресурсы уже близки к пределу хранения. Добавление сделало бы значение отрицательным, поэтому ничего не добавлено."
    ),
    "CCP_EQUIPMENT_ALL": _row(
        "ADD WHOLE CATEGORY",
        "GANZE KATEGORIE",
        "TOUTE LA CATÉGORIE",
        "ВСЮ КАТЕГОРИЮ"
    ),
    "CCP_EQUIPMENT_ALL_TOOLTIP": _row(
        "Add the amount above of every item in this category, not just the visible page.",
        "Fügt von jedem Eintrag dieser Kategorie die oben eingestellte Menge hinzu, nicht nur der sichtbaren Seite.",
        "Ajoute la quantité ci-dessus de chaque élément de cette catégorie, pas seulement la page affichée.",
        "Добавляет указанное выше количество каждого предмета категории, а не только видимой страницы."
    ),
    "CCP_EQUIPMENT_ALL_HELP": _row(
        "Uses the amount from the pad on the right.",
        "Nutzt die Menge aus dem Feld rechts.",
        "Utilise la quantité du pavé de droite.",
        "Использует количество из панели справа."
    ),
    "CCP_EQUIPMENT_STOCK_TOOLTIP": _row(
        "How many of this equipment your country holds right now.",
        "Wie viele dieser Ausrüstung Ihr Land derzeit besitzt.",
        "Combien de cet équipement votre pays possède actuellement.",
        "Сколько этого снаряжения у вашей страны сейчас."
    ),
    "CCP_STATUS_CATEGORY": _row(
        "Added [?ccp_amount|0] of every item in [CCP_GetEquipmentCategoryName].",
        "Von jedem Eintrag in [CCP_GetEquipmentCategoryName] wurden [?ccp_amount|0] hinzugefügt.",
        "[?ccp_amount|0] de chaque élément de [CCP_GetEquipmentCategoryName] ajoutés.",
        "Добавлено по [?ccp_amount|0] каждого предмета в разделе [CCP_GetEquipmentCategoryName]."
    ),
    "CCP_STATUS_SELECTION": _row(
        "Nothing was selected, so nothing was added. Pick a category first, then use a row.",
        "Es war nichts ausgewählt, also wurde nichts hinzugefügt. Erst eine Kategorie wählen, dann eine Zeile.",
        "Rien n était sélectionné, donc rien n a été ajouté. Choisissez d abord une catégorie, puis une ligne.",
        "Ничего не было выбрано, поэтому ничего не добавлено. Сначала выберите категорию, затем строку."
    ),
    "CCP_COUNTRY_TARGET": _row(
        "TARGET", "ZIEL", "CIBLE", "ЦЕЛЬ"
    ),
    "CCP_COUNTRY_TARGET_TOOLTIP": _row(
        "Make this the country that States hands a transferred state to.",
        "Macht dies zum Land, an das ein Staat in Staaten übergeben wird.",
        "Définit le pays auquel la section États transfère un État.",
        "Назначает страну, которой раздел Провинции передаёт провинцию."
    ),
    "CCP_STATE_GIVE": _row(
        "GIVE", "GEBEN", "DONNER", "ОТДАТЬ"
    ),
    "CCP_STATE_GIVE_TOOLTIP": _row(
        "Hand this state to the country picked as TARGET in the Countries section.",
        "Übergibt diesen Staat dem in Länder als ZIEL gewählten Land.",
        "Cède cet État au pays choisi comme CIBLE dans la section Pays.",
        "Передаёт провинцию стране, выбранной как ЦЕЛЬ в разделе Страны."
    ),
    "CCP_STATE_TARGET": _row(
        "Transfer target: [?ccp_target_country.GetNameDefCap]",
        "Übergabeziel: [?ccp_target_country.GetNameDefCap]",
        "Cible du transfert : [?ccp_target_country.GetNameDefCap]",
        "Цель передачи: [?ccp_target_country.GetNameDefCap]"
    ),
    "CCP_STATUS_TARGET": _row(
        "Transfer target set to [?ccp_target_country.GetNameDefCap].",
        "Übergabeziel auf [?ccp_target_country.GetNameDefCap] gesetzt.",
        "Cible du transfert : [?ccp_target_country.GetNameDefCap].",
        "Цель передачи: [?ccp_target_country.GetNameDefCap]."
    ),
    "CCP_RESEARCH_EVERYTHING": _row(
        "RESEARCH EVERYTHING",
        "ALLES ERFORSCHEN",
        "TOUT RECHERCHER",
        "ИЗУЧИТЬ ВСЁ"
    ),
    "CCP_RESEARCH_EVERYTHING_TOOLTIP": _row(
        "Complete every technology in every folder at once.",
        "Schliesst jede Technologie in jedem Ordner auf einmal ab.",
        "Termine toutes les technologies de tous les dossiers d un coup.",
        "Мгновенно завершает все технологии во всех папках."
    ),
    "CCP_STATUS_EVERYTHING": _row(
        "Every technology has been researched.",
        "Jede Technologie wurde erforscht.",
        "Toutes les technologies ont été recherchées.",
        "Все технологии изучены."
    ),
    "CCP_STATUS_GIVEN": _row(
        "State handed to [?ccp_target_country.GetNameDefCap].",
        "Staat an [?ccp_target_country.GetNameDefCap] übergeben.",
        "État cédé à [?ccp_target_country.GetNameDefCap].",
        "Провинция передана: [?ccp_target_country.GetNameDefCap]."
    ),
    "CCP_IRONMAN_LOCKED": _row(
        "This is an Ironman game, so the panel is locked.\n\nAn Ironman save cannot be rolled back and nothing here can be undone, so no section can be opened. This is intended, not a fault. Start a normal game to use the panel.\n\nClose it with CLOSE at the top right, Esc, or your panel hotkey.",
        "Dies ist eine Ironman-Partie, daher ist das Panel gesperrt.\n\nEin Ironman-Spielstand lässt sich nicht zurücksetzen und nichts hier ist umkehrbar, also lässt sich kein Bereich öffnen. Das ist beabsichtigt, kein Fehler. Starten Sie eine normale Partie, um das Panel zu nutzen.\n\nSchließen mit SCHLIESSEN oben rechts, Esc oder Ihrer Panel-Taste.",
        "Cette partie est en Ironman, le panneau est donc verrouillé.\n\nUne sauvegarde Ironman ne peut pas revenir en arrière et rien ici n est réversible, donc aucune section ne s ouvre. C est voulu, pas un défaut. Lancez une partie normale pour utiliser le panneau.\n\nFermez avec FERMER en haut à droite, Échap ou votre raccourci.",
        "Это игра в режиме Ironman, поэтому панель заблокирована.\n\nСохранение Ironman нельзя откатить, а действия панели необратимы, поэтому разделы не открываются. Так задумано, это не ошибка. Начните обычную игру, чтобы пользоваться панелью.\n\nЗакройте кнопкой ЗАКРЫТЬ справа вверху, Esc или горячей клавишей панели."
    ),
    "CCP_SETTINGS_DIPLO": _row(
        "DIPLOMACY", "DIPLOMATIE", "DIPLOMATIE", "ДИПЛОМАТИЯ"
    ),
    "CCP_SETTINGS_DIPLO_HELP": _row(
        "The console switches allowdiplo and yesman cannot be reached from a mod. These two do what they are used for, through the game's own rules: the first lifts every diplomatic restriction script can lift, the second makes every country strongly favourable towards you.",
        "Die Konsolenschalter allowdiplo und yesman sind aus einem Mod nicht erreichbar. Diese beiden erreichen ihren Zweck über die Spielregeln: der erste hebt jede per Skript aufhebbare diplomatische Beschränkung auf, der zweite macht jedes Land Ihnen gegenüber ausgesprochen wohlgesinnt.",
        "Les commandes console allowdiplo et yesman sont hors de portée d un mod. Ces deux boutons obtiennent le même résultat via les règles du jeu : le premier lève toutes les restrictions diplomatiques accessibles au script, le second rend tous les pays très favorables envers vous.",
        "Консольные переключатели allowdiplo и yesman недоступны моду. Эти две кнопки дают тот же результат через правила игры: первая снимает все дипломатические ограничения, доступные скрипту, вторая делает все страны крайне благосклонными к вам."
    ),
    "CCP_SETTINGS_DIPLO_TOOLTIP": _row(
        "Lift faction, guarantee, puppet, volunteer, market and same-ideology war restrictions.",
        "Hebt Beschränkungen für Fraktionen, Garantien, Marionetten, Freiwillige, Markt und Kriege gegen die eigene Ideologie auf.",
        "Lève les restrictions sur factions, garanties, vassaux, volontaires, marché et guerres entre mêmes idéologies.",
        "Снимает ограничения на фракции, гарантии, марионеток, добровольцев, рынок и войну против своей идеологии."
    ),
    "CCP_SETTINGS_GOODWILL_TOOLTIP": _row(
        "Give every country a large positive opinion of you and tell their AI to befriend you. It does not force acceptance, which no effect can do, but it moves the AI as far as script reaches.",
        "Gibt jedem Land eine stark positive Meinung von Ihnen und weist dessen KI an, sich mit Ihnen anzufreunden. Eine Zustimmung erzwingt es nicht, das kann kein Effekt, aber es bewegt die KI so weit wie Skript reicht.",
        "Donne à chaque pays une opinion très positive de vous et demande à leur IA de se lier d amitié. Cela ne force pas l acceptation, aucun effet ne le peut, mais cela pousse l IA aussi loin que le script permet.",
        "Даёт всем странам крайне положительное мнение о вас и велит их ИИ дружить с вами. Согласие это не гарантирует, ни один эффект этого не может, но двигает ИИ настолько, насколько позволяет скрипт."
    ),
    "CCP_DIPLO_ON": _row(
        "DIPLOMACY RULES: ON", "DIPLOMATIEREGELN: AN", "REGLES DIPLO : ON",
        "ДИПЛ. ПРАВИЛА: ВКЛ"
    ),
    "CCP_DIPLO_OFF": _row(
        "DIPLOMACY RULES: OFF", "DIPLOMATIEREGELN: AUS", "REGLES DIPLO : OFF",
        "ДИПЛ. ПРАВИЛА: ВЫКЛ"
    ),
    "CCP_GOODWILL_ON": _row(
        "AI GOODWILL: ON", "KI-WOHLWOLLEN: AN", "BIENVEILLANCE IA : ON",
        "ЛОЯЛЬНОСТЬ ИИ: ВКЛ"
    ),
    "CCP_GOODWILL_OFF": _row(
        "AI GOODWILL: OFF", "KI-WOHLWOLLEN: AUS", "BIENVEILLANCE IA : OFF",
        "ЛОЯЛЬНОСТЬ ИИ: ВЫКЛ"
    ),
    "CCP_STATUS_DIPLO_ON": _row(
        "Diplomatic restrictions lifted.",
        "Diplomatische Beschränkungen aufgehoben.",
        "Restrictions diplomatiques levées.",
        "Дипломатические ограничения сняты."
    ),
    "CCP_STATUS_DIPLO_OFF": _row(
        "Diplomatic restrictions restored.",
        "Diplomatische Beschränkungen wiederhergestellt.",
        "Restrictions diplomatiques rétablies.",
        "Дипломатические ограничения восстановлены."
    ),
    "CCP_STATUS_GOODWILL_ON": _row(
        "Every country now views you very favourably.",
        "Jedes Land sieht Sie nun ausgesprochen positiv.",
        "Tous les pays vous voient désormais très favorablement.",
        "Все страны теперь относятся к вам крайне положительно."
    ),
    "CCP_STATUS_CONFIRM_PENDING": _row(
        "Waiting for you to confirm. Press CONFIRM in the dialog, or turn confirmations off in Settings.",
        "Wartet auf Ihre Bestätigung. Drücken Sie BESTÄTIGEN im Dialog oder schalten Sie Bestätigungen in den Einstellungen ab.",
        "En attente de votre confirmation. Appuyez sur CONFIRMER, ou désactivez les confirmations dans Réglages.",
        "Ожидается подтверждение. Нажмите ПОДТВЕРДИТЬ в окне или отключите подтверждения в настройках."
    ),
    "CCP_STATUS_NO_STATE": _row(
        "Pick a state in the States section or on the map first; this action needs one.",
        "Wählen Sie zuerst einen Staat unter Staaten oder auf der Karte; diese Aktion braucht einen.",
        "Choisissez d abord un État dans la section États ou sur la carte ; cette action en exige un.",
        "Сначала выберите провинцию в разделе Провинции или на карте: этому действию она нужна."
    ),
    "CCP_STATUS_NO_TARGET": _row(
        "Pick a country in the Countries section first; this action needs a target.",
        "Wählen Sie zuerst ein Land im Bereich Länder; diese Aktion braucht ein Ziel.",
        "Choisissez d abord un pays dans la section Pays ; cette action exige une cible.",
        "Сначала выберите страну в разделе Страны: этому действию нужна цель."
    ),
    "CCP_STATUS_GOODWILL_OFF": _row(
        "Opinion boost removed.",
        "Meinungsbonus entfernt.",
        "Bonus d opinion retiré.",
        "Бонус к мнению снят."
    ),
    "CCP_POLITICS_HELP": _row(
        "Every button here changes the government. The red ones cannot be undone.",
        "Jede Schaltfläche hier ändert die Regierung. Die roten lassen sich nicht rückgängig machen.",
        "Chaque bouton ici change le gouvernement. Les rouges sont irréversibles.",
        "Каждая кнопка здесь меняет власть. Красные необратимы."
    ),
    "CCP_STOCKPILE_HELP": _row(
        "Resources are added to every state you own, so the totals show up in your trade view.",
        "Rohstoffe werden jedem Ihrer Staaten hinzugefügt und erscheinen in der Handelsansicht.",
        "Les ressources sont ajoutées à tous vos États et apparaissent dans la vue commerce.",
        "Ресурсы добавляются во все ваши провинции и видны в окне торговли."
    ),
    "CCP_MILITARY_HELP": _row(
        "Divisions come from templates this mod adds to your list: in your capital, or in the state last picked under States or on the map.",
        "Divisionen entstehen aus Vorlagen dieses Mods: in Ihrer Hauptstadt oder im zuletzt unter Staaten oder auf der Karte gewählten Staat.",
        "Les divisions viennent de modèles ajoutés par ce mod : dans votre capitale, ou dans l État choisi en dernier dans États ou sur la carte.",
        "Дивизии создаются по шаблонам мода: в столице или в провинции, выбранной последней в разделе Провинции или на карте."
    ),
    "CCP_THREAT_SOURCE": _row(
        "Cheat Control Panel", "Cheat-Kontrollpanel", "Panneau de triche",
        "Панель управления читами"
    ),
    "CCP_DIPLOMACY_HELP": _row(
        "Every button here acts on [?ccp_target_country.GetNameDefCap]. Pick a different country with TARGET in the Countries section.",
        "Jede Schaltfläche hier wirkt auf [?ccp_target_country.GetNameDefCap]. Ein anderes Land wählen Sie mit ZIEL unter Länder.",
        "Chaque bouton agit sur [?ccp_target_country.GetNameDefCap]. Choisissez un autre pays avec CIBLE dans la section Pays.",
        "Все кнопки действуют на [?ccp_target_country.GetNameDefCap]. Другую страну выберите кнопкой ЦЕЛЬ в разделе Страны."
    ),
    "CCP_FACTION_NAME": _row(
        "Cheat Control Pact", "Cheat-Kontroll-Pakt", "Pacte du panneau de triche",
        "Пакт панели читов"
    ),
    "CCP_STATE_UNCLAIM": _row("UNCLAIM", "ANSPR. WEG", "RETIRER", "СНЯТЬ"),
    "CCP_STATE_UNCLAIM_TOOLTIP": _row(
        "Remove your claim from this state.",
        "Entfernt Ihren Anspruch auf diesen Staat.",
        "Retire votre revendication sur cet État.",
        "Снимает ваше притязание на провинцию."
    ),
    "CCP_STATE_COMPLY": _row("COMPLY", "FÜGSAM", "SOUMIS", "ПОКОРН"),
    "CCP_STATE_COMPLY_TOOLTIP": _row(
        "Set this state's compliance to full, so occupation runs smoothly.",
        "Setzt die Fügsamkeit dieses Staates auf das Maximum, damit die Besatzung reibungslos läuft.",
        "Porte la soumission de cet État au maximum pour une occupation sans heurts.",
        "Доводит покорность провинции до максимума, чтобы оккупация шла гладко."
    ),
    "CCP_STATE_QUIET": _row("PACIFY", "BEFRIEDEN", "PACIFIER", "УСМИРИТЬ"),
    "CCP_STATE_QUIET_TOOLTIP": _row(
        "Wipe out resistance in this state.",
        "Löscht den Widerstand in diesem Staat aus.",
        "Élimine la résistance dans cet État.",
        "Полностью подавляет сопротивление в провинции."
    ),
    "CCP_PAD_LABEL": _row(
        "CUSTOM AMOUNT", "EIGENE MENGE", "MONTANT PERSONNALISÉ",
        "СВОЁ ЗНАЧЕНИЕ"
    ),
    "CCP_PAD_BACK": _row("DEL", "LÖSCH", "EFF", "СТЕР"),
    "CCP_PAD_CLEAR": _row("CLR", "RESET", "RAZ", "СБРОС"),
    "CCP_PAD_DIGIT_TOOLTIP": _row(
        "Append this digit to the custom amount.",
        "Hängt diese Ziffer an die eigene Menge an.",
        "Ajoute ce chiffre au montant personnalisé.",
        "Добавляет цифру к введённому значению."
    ),
    "CCP_PAD_BACK_TOOLTIP": _row(
        "Remove the last digit.",
        "Entfernt die letzte Ziffer.",
        "Supprime le dernier chiffre.",
        "Удаляет последнюю цифру."
    ),
    "CCP_PAD_CLEAR_TOOLTIP": _row(
        "Reset the custom amount to zero.",
        "Setzt die eigene Menge auf null zurück.",
        "Remet le montant personnalisé à zéro.",
        "Обнуляет введённое значение."
    ),
    "CCP_PAD_HELP": _row(
        "To give any amount: tap it in on these number keys, then press CUSTOM on the row you want. The game cannot read typed text back into a mod, which is why there is no input box. The amount is capped at what that resource can usefully take.",
        "Hearts of Iron IV kann einen eingetippten Wert nicht ans Skript zurückgeben, daher wird die Menge hier eingegeben. Jede EIGENER-Schaltfläche vergibt diese Menge, begrenzt auf das, was die Ressource sinnvoll aufnimmt.",
        "Hearts of Iron IV ne peut pas renvoyer une valeur saisie au script ; le montant se saisit donc ici. Chaque bouton PERSO accorde ce montant, plafonné à ce que la ressource peut réellement utiliser.",
        "Hearts of Iron IV не может вернуть набранное значение в скрипт, поэтому величина вводится здесь. Каждая кнопка СВОЁ выдаёт это количество с ограничением по ресурсу."
    ),
}

SECTION_NAMES: dict[str, Row] = {
    "dashboard": _row(
        "Dashboard", "Übersicht", "Tableau de bord", "Обзор"
    ),
    "resources": _row(
        "Resources", "Ressourcen", "Ressources", "Ресурсы"
    ),
    "equipment": _row(
        "Equipment", "Ausrüstung", "Équipement", "Снаряжение"
    ),
    "research": _row(
        "Research", "Forschung", "Recherche", "Исследования"
    ),
    "country": _row(
        "Countries", "Länder", "Pays", "Страны"
    ),
    "states": _row(
        "States", "Staaten", "États", "Провинции"
    ),
    "nation": _row(
        "Nation", "Nation", "Nation", "Держава"
    ),
    "construction": _row(
        "Construction", "Bau", "Construction", "Строительство"
    ),
    "politics": _row(
        "Politics", "Politik", "Politique", "Политика"
    ),
    "stockpile": _row(
        "Resources", "Ressourcen", "Ressources", "Сырьё"
    ),
    "military": _row(
        "Military", "Militär", "Militaire", "Армия"
    ),
    "commanders": _row(
        "Commanders", "Befehlshaber", "Commandants", "Командующие"
    ),
    "diplomacy": _row(
        "Diplomacy", "Diplomatie", "Diplomatie", "Дипломатия"
    ),
    "history": _row(
        "History", "Verlauf", "Historique", "История"
    ),
    "settings": _row(
        "Settings", "Einstellungen", "Paramètres", "Настройки"
    ),
}

SECTION_TOOLTIPS: dict[str, Row] = {
    "dashboard": _row(
        "A live summary of the country you are playing.",
        "Eine Live-Übersicht des Landes, das Sie spielen.",
        "Un résumé en direct du pays que vous jouez.",
        "Сводка по стране, за которую вы играете."
    ),
    "resources": _row(
        "Grant political power, command power, manpower and experience.",
        "Vergibt politische Macht, Kommandopunkte, Rekruten und Erfahrung.",
        "Accorde pouvoir politique, points de commandement, effectifs et expérience.",
        "Выдаёт политическую силу, очки командования, людские ресурсы и опыт."
    ),
    "equipment": _row(
        "Add any equipment in your installation to the stockpile.",
        "Fügt dem Lager jede in Ihrer Installation vorhandene Ausrüstung hinzu.",
        "Ajoute au stock n'importe quel équipement présent dans votre installation.",
        "Добавляет на склад любое снаряжение из вашей установки."
    ),
    "research": _row(
        "Grant technologies one at a time or a whole research folder at once.",
        "Vergibt Technologien einzeln oder einen ganzen Forschungsordner auf einmal.",
        "Accorde des technologies une par une ou un dossier de recherche entier.",
        "Выдаёт технологии по одной или целую папку исследований сразу."
    ),
    "country": _row(
        "Annex, puppet, declare war on or switch to any country in the game.",
        "Annektieren, zum Marionettenstaat machen, Krieg erklären oder zu einem Land wechseln.",
        "Annexer, vassaliser, déclarer la guerre ou incarner un pays.",
        "Аннексировать, сделать марионеткой, объявить войну или переключиться на любую страну."
    ),
    "states": _row(
        "Take states, add or remove cores, and add claims.",
        "Staaten übernehmen, Kerngebiete setzen oder entfernen und Ansprüche erheben.",
        "Prendre des États, ajouter ou retirer des territoires nationaux, revendiquer.",
        "Забирать провинции, добавлять и снимать коренные территории, выдвигать притязания."
    ),
    "nation": _row(
        "Stability, war support, research slots and fuel.",
        "Stabilität, Kriegsunterstützung, Forschungsplätze und Treibstoff.",
        "Stabilité, soutien à la guerre, emplacements de recherche et carburant.",
        "Стабильность, поддержка войны, слоты исследований и топливо."
    ),
    "construction": _row(
        "Build instantly across every state you own.",
        "Baut sofort in jedem Ihrer Staaten.",
        "Construit instantanément dans tous vos États.",
        "Мгновенно строит во всех ваших провинциях."
    ),
    "politics": _row(
        "Change who rules, shift popular support, or split the country.",
        "Ändert die Regierung, verschiebt die Unterstützung oder spaltet das Land.",
        "Change le gouvernement, déplace le soutien populaire ou divise le pays.",
        "Меняет власть, сдвигает поддержку или раскалывает страну."
    ),
    "stockpile": _row(
        "Add raw resources to every state you own.",
        "Fügt jedem Ihrer Staaten Rohstoffe hinzu.",
        "Ajoute des ressources brutes à chacun de vos États.",
        "Добавляет сырьё во все ваши провинции."
    ),
    "military": _row(
        "Nuclear bombs, divisions and experience.",
        "Atombomben, Divisionen und Erfahrung.",
        "Bombes nucléaires, divisions et expérience.",
        "Ядерные бомбы, дивизии и опыт."
    ),
    "commanders": _row(
        "Raise the skills of every general and admiral you have.",
        "Erhöht die Fähigkeiten aller Ihrer Generäle und Admirale.",
        "Améliore les compétences de tous vos généraux et amiraux.",
        "Повышает навыки всех ваших генералов и адмиралов."
    ),
    "diplomacy": _row(
        "Acts on the country you picked as TARGET in the Countries section.",
        "Wirkt auf das Land, das Sie unter Länder als ZIEL gewählt haben.",
        "Agit sur le pays choisi comme CIBLE dans la section Pays.",
        "Действует на страну, выбранную как ЦЕЛЬ в разделе Страны."
    ),
    "history": _row(
        "The last ten actions this panel applied, each repeatable.",
        "Die letzten zehn Aktionen dieses Panels, jede wiederholbar.",
        "Les dix dernières actions du panneau, toutes répétables.",
        "Последние десять действий панели, каждое можно повторить."
    ),
    "settings": _row(
        "Change the hotkey and the confirmation behaviour.",
        "Ändert Tastenkürzel und Bestätigungsverhalten.",
        "Modifie le raccourci et le comportement des confirmations.",
        "Меняет горячую клавишу и поведение подтверждений."
    ),
}

RESOURCE_NAMES: dict[str, Row] = {
    "political_power": _row(
        "Political Power", "Politische Macht", "Pouvoir politique",
        "Политическая сила"
    ),
    "command_power": _row(
        "Command Power", "Kommandopunkte", "Points de commandement",
        "Очки командования"
    ),
    "manpower": _row(
        "Manpower", "Rekruten", "Effectifs", "Людские ресурсы"
    ),
    "army_experience": _row(
        "Army Experience", "Heereserfahrung", "Expérience terrestre",
        "Опыт армии"
    ),
    "navy_experience": _row(
        "Navy Experience", "Marineerfahrung", "Expérience navale",
        "Опыт флота"
    ),
    "air_experience": _row(
        "Air Experience", "Luftwaffenerfahrung", "Expérience aérienne",
        "Опыт авиации"
    ),
}

RESOURCE_HELP: dict[str, Row] = {
    "political_power": _row(
        "Spent on advisors, laws and decisions.",
        "Wird für Berater, Gesetze und Entscheidungen ausgegeben.",
        "Dépensé pour les conseillers, les lois et les décisions.",
        "Тратится на советников, законы и решения."
    ),
    "command_power": _row(
        "Spent on army abilities. The game caps command power at 100, so larger grants are wasted.",
        "Für Armeefähigkeiten. Das Spiel begrenzt Kommandopunkte auf 100, mehr verfällt.",
        "Pour les capacités d'armée. Le jeu plafonne à 100, au-delà c'est perdu.",
        "Для армейских способностей. Игра ограничивает их сотней, излишек пропадает."
    ),
    "manpower": _row(
        "Used to deploy and reinforce divisions.",
        "Zum Aufstellen und Verstärken von Divisionen.",
        "Sert à déployer et renforcer les divisions.",
        "Используется для развёртывания и пополнения дивизий."
    ),
    "army_experience": _row(
        "Spent on division templates.",
        "Wird für Divisionsvorlagen ausgegeben.",
        "Dépensé sur les modèles de division.",
        "Тратится на шаблоны дивизий."
    ),
    "navy_experience": _row(
        "Spent on ship designs.",
        "Wird für Schiffsentwürfe ausgegeben.",
        "Dépensé sur les modèles de navire.",
        "Тратится на проекты кораблей."
    ),
    "air_experience": _row(
        "Spent on aircraft designs.",
        "Wird für Flugzeugentwürfe ausgegeben.",
        "Dépensé sur les modèles d'avion.",
        "Тратится на проекты самолётов."
    ),
}

ADD_TEMPLATE = _row(
    "Add {amount} {name}.",
    "{amount} {name} hinzufügen.",
    "Ajouter {amount} {name}.",
    "Добавить: {amount} {name}."
)

CUSTOM_TEMPLATE = _row(
    "Add the custom amount, capped at {cap}.",
    "Fügt die eigene Menge hinzu, begrenzt auf {cap}.",
    "Ajoute le montant personnalisé, plafonné à {cap}.",
    "Добавляет введённое значение, максимум {cap}."
)

HOTKEY_TEMPLATE = _row(
    "Use {key} to open and close the panel.",
    "Mit {key} das Panel öffnen und schließen.",
    "Utiliser {key} pour ouvrir et fermer le panneau.",
    "Клавиша {key} открывает и закрывает панель."
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

    for action in COUNTRY_ACTIONS:
        strings[action.key] = dict(zip(ALL, title_for(action.slug)))
        strings[f"{action.key}_HELP"] = dict(zip(ALL, help_for(action.slug)))
        strings[f"{action.key}_TOOLTIP"] = dict(zip(ALL, help_for(action.slug)))
        for level in action.levels:
            strings[f"{action.key}_{level_id(level)}"] = _same(action.caption(level))

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


SHARED_ACROSS_LANGUAGES = frozenset(
    {
        # Key names are what the keyboard is labelled, not words to translate.
        "CCP_HOTKEY_1",
        "CCP_HOTKEY_2",
        "CCP_HOTKEY_3",
        "CCP_HOTKEY_4",
        "CCP_HOTKEY_5",
        # Durations and element names that read the same in every language here.
        "CCP_ACTION_TRUCE_180",
        "CCP_ACTION_TRUCE_365",
        "CCP_ACTION_TRUCE_730",
        "CCP_ACTION_RESOURCE_ALUMINIUM",
        "CCP_ACTION_RESOURCE_RUBBER",
        "CCP_ACTION_RESOURCE_TUNGSTEN",
        "CCP_ACTION_INFRASTRUCTURE",
        "CCP_ACTION_COLLABORATION",
        "CCP_ACTION_PLANNING",
        "CCP_SECTION_NATION",
        "CCP_SECTION_CONSTRUCTION",
        "CCP_SIDEBAR_HEADING",
        "CCP_SETTINGS_CONFIRM",
    }
)


def untranslated() -> dict[str, list[str]]:
    """Keys whose translation is still the English text, per language.

    A missing translation passes the parity check, because the key exists in every
    file -- it just says the same thing. This is what actually catches it. Rows
    that are correctly identical are listed above rather than tolerated silently.
    """
    import re as _re

    rows = all_strings()
    from .languages import ALL as LANGUAGES

    languages = [name for name in LANGUAGES if name != "english"]
    found: dict[str, list[str]] = {name: [] for name in languages}
    for key, row in rows.items():
        english = row["english"].strip()
        if key in SHARED_ACROSS_LANGUAGES:
            continue
        if len(english) < 4 or english.startswith("[") or _re.fullmatch(r"[+\-x0-9%KM ]+", english):
            continue
        for name in languages:
            if row[name].strip() == english:
                found[name].append(key)
    return {name: keys for name, keys in found.items() if keys}
