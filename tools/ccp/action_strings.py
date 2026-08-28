"""Names and explanations for every action, in all six languages.

Kept apart from `strings.py` because the action registry is where most of the
panel's text now lives. Repetitive families — the seven resources, the four
ideologies — get their noun translated once and share a sentence template, so a
new member of a family needs one line rather than eighteen.
"""

from __future__ import annotations

Row = tuple[str, str, str, str]

# ---------------------------------------------------------------- shared sentences

HELP_BUILDING: Row = (
    "Built instantly in every state you own.",
    "Wird sofort in jedem Ihrer Staaten gebaut.",
    "Construit instantanément dans chacun de vos États.",
    "Мгновенно строится во всех ваших провинциях."
)

HELP_COASTAL: Row = (
    "Built instantly in every coastal state you own.",
    "Wird sofort in jedem Ihrer Küstenstaaten gebaut.",
    "Construit instantanément dans chacun de vos États côtiers.",
    "Мгновенно строится во всех ваших прибрежных провинциях."
)

HELP_RESOURCE: Row = (
    "Adds this resource to every state you own.",
    "Fügt jedem Ihrer Staaten diese Ressource hinzu.",
    "Ajoute cette ressource à chacun de vos États.",
    "Добавляет этот ресурс во все ваши провинции."
)

HELP_POPULARITY: Row = (
    "Raises this ideology's share of the popular vote.",
    "Erhöht den Stimmenanteil dieser Ideologie.",
    "Augmente la part de cette idéologie dans l'opinion.",
    "Повышает долю этой идеологии в общественном мнении."
)

HELP_RULING: Row = (
    "Puts this ideology in power immediately. Elections stay allowed.",
    "Bringt diese Ideologie sofort an die Macht. Wahlen bleiben erlaubt.",
    "Porte cette idéologie au pouvoir immédiatement. Les élections restent autorisées.",
    "Немедленно приводит эту идеологию к власти. Выборы остаются разрешёнными."
)

HELP_LEADER: Row = (
    "Applies to every commander you have right now, not to future ones.",
    "Gilt für alle derzeitigen Befehlshaber, nicht für künftige.",
    "S'applique à tous vos commandants actuels, pas aux futurs.",
    "Действует на нынешних командующих, но не на будущих."
)

HELP_DIVISIONS: Row = (
    "Spawns divisions in your capital from a template this mod adds. The template stays in your list.",
    "Stellt Divisionen in Ihrer Hauptstadt aus einer Vorlage dieses Mods auf. Die Vorlage bleibt in Ihrer Liste.",
    "Fait apparaître des divisions dans votre capitale à partir d'un modèle ajouté par ce mod. Le modèle reste dans votre liste.",
    "Создаёт дивизии в столице по шаблону, который добавляет этот мод. Шаблон остаётся в вашем списке."
)

# ---------------------------------------------------------------- per-action titles

TITLES: dict[str, Row] = {
    "research_bonus": (
        "Research bonus",
        "Forschungsbonus",
        "Bonus de recherche",
        "Бонус исследований"
    ),
    "doctrines_free": (
        "Free doctrines",
        "Kostenlose Doktrinen",
        "Doctrines gratuites",
        "Бесплатные доктрины"
    ),
    "occupation_harsh": (
        "Military governor",
        "Militärgouverneur",
        "Gouverneur militaire",
        "Военный губернатор"
    ),
    "occupation_soft": (
        "Local police",
        "Örtliche Polizei",
        "Police locale",
        "Местная полиция"
    ),
    "collaboration": (
        "Collaboration",
        "Kollaboration",
        "Collaboration",
        "Коллаборация"
    ),
    "guarantee": (
        "Guarantee",
        "Garantie",
        "Garantie",
        "Гарантия"
    ),
    # nation
    "stability": ("Stability", "Stabilität", "Stabilité", "Стабильность"),
    "stability_full": ("Stability to full", "Stabilität auf Maximum", "Stabilité au maximum", "Стабильность на максимум"),
    "stability_zero": ("Stability to zero", "Stabilität auf null", "Stabilité à zéro", "Стабильность в ноль"),
    "war_support": ("War support", "Kriegsunterstützung", "Soutien à la guerre", "Поддержка войны"),
    "war_support_full": ("War support to full", "Kriegsunterstützung auf Maximum", "Soutien au maximum", "Поддержка на максимум"),
    "war_support_zero": ("War support to zero", "Kriegsunterstützung auf null", "Soutien à zéro", "Поддержка в ноль"),
    "research_slots": ("Research slots", "Forschungsplätze", "Emplacements de recherche", "Слоты исследований"),
    "fuel": ("Fuel", "Treibstoff", "Carburant", "Топливо"),
    "cic": ("Market funds", "Marktmittel", "Fonds de marché", "Рыночные средства"),
    "threat": ("World tension", "Weltspannung", "Tension mondiale", "Мировая напряжённость"),
    "legitimacy": ("Legitimacy", "Legitimität", "Légitimité", "Легитимность"),
    # construction
    "infrastructure": ("Infrastructure", "Infrastruktur", "Infrastructure", "Инфраструктура"),
    "civilian": ("Civilian factories", "Zivilfabriken", "Usines civiles", "Гражданские заводы"),
    "military": ("Military factories", "Militärfabriken", "Usines militaires", "Военные заводы"),
    "dockyard": ("Dockyards", "Werften", "Chantiers navals", "Верфи"),
    "airbase": ("Air bases", "Flugplätze", "Bases aériennes", "Аэродромы"),
    "radar": ("Radar stations", "Radarstationen", "Stations radar", "Радары"),
    "antiair": ("Anti-air", "Flugabwehr", "Antiaérien", "ПВО"),
    "fort": ("Land forts", "Landbefestigungen", "Fortifications terrestres", "Сухопутные форты"),
    "coastal_fort": ("Coastal forts", "Küstenbefestigungen", "Fortifications côtières", "Береговые форты"),
    "supply_hub": ("Supply hub", "Nachschubzentrum", "Centre de ravitaillement", "Узел снабжения"),
    "slots": ("Building slots", "Bauplätze", "Emplacements de construction", "Слоты построек"),
    "offsite_civilian": ("Off-map civilian factories", "Zivilfabriken ausserhalb der Karte", "Usines civiles hors carte", "Гражданские заводы вне карты"),
    "offsite_military": ("Off-map military factories", "Militärfabriken ausserhalb der Karte", "Usines militaires hors carte", "Военные заводы вне карты"),
    "mines": ("Naval mines", "Seeminen", "Mines navales", "Морские мины"),
    # politics
    "civil_war": ("Start a civil war", "Bürgerkrieg auslösen", "Déclencher une guerre civile", "Начать гражданскую войну"),
    "autonomy": ("Raise autonomy", "Autonomie erhöhen", "Augmenter l'autonomie", "Повысить автономию"),
    "autonomy_down": ("Lower autonomy", "Autonomie senken", "Réduire l'autonomie", "Понизить автономию"),
    # military
    "nukes": ("Nuclear bombs", "Atombomben", "Bombes nucléaires", "Ядерные бомбы"),
    "divisions_infantry": ("Infantry divisions", "Infanteriedivisionen", "Divisions d'infanterie", "Пехотные дивизии"),
    "divisions_armor": ("Armoured divisions", "Panzerdivisionen", "Divisions blindées", "Танковые дивизии"),
    "divisions_motorized": ("Motorized divisions", "Motorisierte Divisionen", "Divisions motorisées", "Моторизованные дивизии"),
    "delete_units": ("Disband every division", "Alle Divisionen auflösen", "Dissoudre toutes les divisions", "Расформировать все дивизии"),
    "army_xp": ("Army experience", "Heereserfahrung", "Expérience terrestre", "Опыт армии"),
    "navy_xp": ("Navy experience", "Marineerfahrung", "Expérience navale", "Опыт флота"),
    "air_xp": ("Air experience", "Luftwaffenerfahrung", "Expérience aérienne", "Опыт авиации"),
    # diplomacy
    "opinion_up": ("Win them over", "Wohlwollen wecken", "Gagner leur faveur", "Расположить к себе"),
    "opinion_down": ("Sour relations", "Verhältnis trüben", "Détériorer les relations", "Испортить отношения"),
    "intel": ("Intelligence", "Aufklärung", "Renseignement", "Разведка"),
    "wargoal": ("War goal", "Kriegsziel", "Objectif de guerre", "Цель войны"),
    "truce": ("Truce", "Waffenstillstand", "Trêve", "Перемирие"),
    "faction_create": ("Found a faction", "Fraktion gründen", "Fonder une faction", "Создать фракцию"),
    "faction_invite": ("Invite to faction", "Zur Fraktion einladen", "Inviter dans la faction", "Пригласить во фракцию"),
    "release_target": ("Release as a puppet", "Als Marionette freilassen", "Libérer comme vassal", "Освободить как марионетку"),
    "free_target": ("Grant independence", "Unabhängigkeit gewähren", "Accorder l'indépendance", "Дать независимость"),
    # commanders
    "skill": ("General skill", "Generalsstufe", "Compétence des généraux", "Навык генералов"),
    "attack": ("Attack", "Angriff", "Attaque", "Атака"),
    "defense": ("Defence", "Verteidigung", "Défense", "Защита"),
    "planning": ("Planning", "Planung", "Planification", "Планирование"),
    "logistics": ("Logistics", "Logistik", "Logistique", "Логистика"),
    "admiral_skill": ("Admiral skill", "Admiralsstufe", "Compétence des amiraux", "Навык адмиралов"),
}

RESOURCE_NOUNS: dict[str, Row] = {
    "oil": ("Oil", "Öl", "Pétrole", "Нефть"),
    "aluminium": ("Aluminium", "Aluminium", "Aluminium", "Алюминий"),
    "rubber": ("Rubber", "Gummi", "Caoutchouc", "Резина"),
    "tungsten": ("Tungsten", "Wolfram", "Tungstène", "Вольфрам"),
    "steel": ("Steel", "Stahl", "Acier", "Сталь"),
    "chromium": ("Chromium", "Chrom", "Chrome", "Хром"),
    "coal": ("Coal", "Kohle", "Charbon", "Уголь"),
}

IDEOLOGY_NOUNS: dict[str, Row] = {
    "democratic": ("Democratic", "Demokratisch", "Démocratique", "Демократия"),
    "communism": ("Communist", "Kommunistisch", "Communiste", "Коммунизм"),
    "fascism": ("Fascist", "Faschistisch", "Fasciste", "Фашизм"),
    "neutrality": ("Non-aligned", "Blockfrei", "Non-aligné", "Нейтралитет"),
}

HELPS: dict[str, Row] = {
    "research_bonus": (
        "Grants a free instant research for the next few technologies you start.",
        "Gewährt für die nächsten Technologien jeweils eine kostenlose Sofortforschung.",
        "Accorde une recherche instantanée gratuite pour les prochaines technologies lancées.",
        "Даёт мгновенное бесплатное исследование для следующих начатых технологий."
    ),
    "doctrines_free": (
        "Makes the next doctrines free in all three trees. set_technology cannot reach doctrines; a full cost reduction can.",
        "Macht die nächsten Doktrinen in allen drei Bäumen kostenlos. set_technology erreicht Doktrinen nicht, eine volle Kostensenkung schon.",
        "Rend gratuites les prochaines doctrines des trois arbres. set_technology n atteint pas les doctrines, une réduction totale du coût si.",
        "Делает следующие доктрины бесплатными во всех трёх ветках. set_technology до доктрин не достаёт, полное снижение стоимости достаёт."
    ),
    "occupation_harsh": (
        "Sets your default occupation law to military governor. Needs La Resistance.",
        "Setzt Ihr Standard-Besatzungsgesetz auf Militärgouverneur. Erfordert La Resistance.",
        "Définit votre loi d occupation par défaut sur gouverneur militaire. Nécessite La Resistance.",
        "Устанавливает закон оккупации по умолчанию: военный губернатор. Требуется La Resistance."
    ),
    "occupation_soft": (
        "Sets your default occupation law to local police force. Needs La Resistance.",
        "Setzt Ihr Standard-Besatzungsgesetz auf örtliche Polizei. Erfordert La Resistance.",
        "Définit votre loi d occupation par défaut sur police locale. Nécessite La Resistance.",
        "Устанавливает закон оккупации по умолчанию: местная полиция. Требуется La Resistance."
    ),
    "collaboration": (
        "Raises collaboration in the country picked in the Countries section.",
        "Erhöht die Kollaboration im Land, das im Bereich Länder gewählt ist.",
        "Augmente la collaboration dans le pays choisi dans la section Pays.",
        "Повышает коллаборацию в стране, выбранной в разделе Страны."
    ),
    "guarantee": (
        "Guarantees the independence of the country picked in the Countries section.",
        "Garantiert die Unabhängigkeit des im Bereich Länder gewählten Landes.",
        "Garantit l indépendance du pays choisi dans la section Pays.",
        "Гарантирует независимость страны, выбранной в разделе Страны."
    ),
    "stability": (
        "Raises national stability by the chosen amount.",
        "Erhöht die nationale Stabilität um den gewählten Wert.",
        "Augmente la stabilité nationale du montant choisi.",
        "Повышает стабильность на выбранную величину."
    ),
    "war_support": (
        "Raises war support by the chosen amount.",
        "Erhöht die Kriegsunterstützung um den gewählten Wert.",
        "Augmente le soutien à la guerre du montant choisi.",
        "Повышает поддержку войны на выбранную величину."
    ),
    "stability_full": (
        "Sets stability to its maximum.",
        "Setzt die Stabilität auf das Maximum.",
        "Porte la stabilité au maximum.",
        "Устанавливает максимальную стабильность."
    ),
    "war_support_full": (
        "Sets war support to its maximum.",
        "Setzt die Kriegsunterstützung auf das Maximum.",
        "Porte le soutien à la guerre au maximum.",
        "Устанавливает максимальную поддержку войны."
    ),
    "stability_zero": (
        "Drops stability to nothing. Useful for triggering a civil war, and hard to walk back.",
        "Senkt die Stabilität auf null. Nützlich für einen Bürgerkrieg und schwer rückgängig zu machen.",
        "Réduit la stabilité à zéro. Utile pour déclencher une guerre civile, difficile à corriger.",
        "Обнуляет стабильность. Полезно для гражданской войны и трудно исправимо."
    ),
    "war_support_zero": (
        "Drops war support to nothing.",
        "Senkt die Kriegsunterstützung auf null.",
        "Réduit le soutien à la guerre à zéro.",
        "Обнуляет поддержку войны."
    ),
    "research_slots": (
        "Sets how many technologies you can research at once. Five is the game's maximum.",
        "Legt fest, wie viele Technologien Sie gleichzeitig erforschen. Fünf ist das Maximum des Spiels.",
        "Définit le nombre de recherches simultanées. Cinq est le maximum du jeu.",
        "Задаёт число одновременных исследований. Пять — максимум игры."
    ),
    "fuel": (
        "Adds fuel to your reserves.",
        "Fügt Ihren Reserven Treibstoff hinzu.",
        "Ajoute du carburant à vos réserves.",
        "Добавляет топливо в резервы."
    ),
    "cic": (
        "Adds funds to the international market account.",
        "Fügt dem Konto des internationalen Marktes Mittel hinzu.",
        "Ajoute des fonds au compte du marché international.",
        "Добавляет средства на счёт международного рынка."
    ),
    "threat": (
        "Raises world tension, which unlocks wars and interventions.",
        "Erhöht die Weltspannung, was Kriege und Interventionen freischaltet.",
        "Augmente la tension mondiale, ce qui débloque guerres et interventions.",
        "Повышает мировую напряжённость, открывая войны и вмешательства."
    ),
    "legitimacy": (
        "Raises the legitimacy of a government in exile.",
        "Erhöht die Legitimität einer Exilregierung.",
        "Augmente la légitimité d'un gouvernement en exil.",
        "Повышает легитимность правительства в изгнании."
    ),
    "civil_war": (
        "Splits the country and hands the chosen share to communist rebels. There is no way back from this.",
        "Spaltet das Land und übergibt kommunistischen Rebellen den gewählten Anteil. Davon gibt es kein Zurück.",
        "Divise le pays et donne la part choisie aux rebelles communistes. Aucun retour possible.",
        "Раскалывает страну и отдаёт выбранную долю коммунистическим повстанцам. Пути назад нет."
    ),
    "autonomy": (
        "Moves a subject closer to independence.",
        "Bringt einen Vasallen der Unabhängigkeit näher.",
        "Rapproche un vassal de l'indépendance.",
        "Приближает вассала к независимости."
    ),
    "autonomy_down": (
        "Pulls a subject further under your control.",
        "Zieht einen Vasallen stärker unter Ihre Kontrolle.",
        "Resserre votre contrôle sur un vassal.",
        "Усиливает ваш контроль над вассалом."
    ),
    "nukes": (
        "Adds ready nuclear bombs to your stockpile.",
        "Fügt Ihrem Lager einsatzbereite Atombomben hinzu.",
        "Ajoute des bombes nucléaires prêtes à l'emploi.",
        "Добавляет готовые ядерные бомбы на склад."
    ),
    "delete_units": (
        "Disbands every division you have. There is no undo.",
        "Löst jede Ihrer Divisionen auf. Es gibt kein Rückgängig.",
        "Dissout toutes vos divisions. Aucune annulation.",
        "Расформировывает все ваши дивизии. Отмены нет."
    ),
    "army_xp": (
        "Army experience, spent on division templates.",
        "Heereserfahrung, für Divisionsvorlagen.",
        "Expérience terrestre, dépensée sur les modèles de division.",
        "Опыт армии, тратится на шаблоны дивизий."
    ),
    "navy_xp": (
        "Navy experience, spent on ship designs.",
        "Marineerfahrung, für Schiffsentwürfe.",
        "Expérience navale, dépensée sur les modèles de navire.",
        "Опыт флота, тратится на проекты кораблей."
    ),
    "air_xp": (
        "Air experience, spent on aircraft designs.",
        "Luftwaffenerfahrung, für Flugzeugentwürfe.",
        "Expérience aérienne, dépensée sur les modèles d'avion.",
        "Опыт авиации, тратится на проекты самолётов."
    ),

    "opinion_up": (
        "Gives the target country a strong positive opinion of you.",
        "Verschafft dem Zielland eine stark positive Meinung von Ihnen.",
        "Donne au pays ciblé une opinion très positive de vous.",
        "Даёт целевой стране крайне положительное мнение о вас."
    ),
    "opinion_down": (
        "Gives the target country a strong negative opinion of you.",
        "Verschafft dem Zielland eine stark negative Meinung von Ihnen.",
        "Donne au pays ciblé une opinion très négative de vous.",
        "Даёт целевой стране крайне отрицательное мнение о вас."
    ),
    "intel": (
        "Raises what you know about the target country across all four branches.",
        "Erhöht Ihr Wissen über das Zielland in allen vier Bereichen.",
        "Augmente ce que vous savez du pays ciblé dans les quatre domaines.",
        "Повышает ваши сведения о целевой стране во всех четырёх областях."
    ),
    "wargoal": (
        "Gives you an annexation war goal on the target, so war needs no justification.",
        "Verschafft Ihnen ein Annexions-Kriegsziel gegen das Ziel, ohne Rechtfertigung.",
        "Vous donne un objectif d'annexion sur la cible, sans justification à préparer.",
        "Даёт вам повод к войне на аннексию цели без обоснования."
    ),
    "truce": (
        "Locks a truce with the target country for the chosen number of days.",
        "Setzt einen Waffenstillstand mit dem Zielland für die gewählte Anzahl Tage.",
        "Impose une trêve avec la cible pour le nombre de jours choisi.",
        "Устанавливает перемирие с целью на выбранное число дней."
    ),
    "faction_create": (
        "Founds a faction with you at its head.",
        "Gründet eine Fraktion unter Ihrer Führung.",
        "Fonde une faction sous votre direction.",
        "Создаёт фракцию под вашим руководством."
    ),
    "faction_invite": (
        "Brings the target country into your faction.",
        "Nimmt das Zielland in Ihre Fraktion auf.",
        "Fait entrer le pays ciblé dans votre faction.",
        "Вводит целевую страну в вашу фракцию."
    ),
    "release_target": (
        "Releases the target as your puppet using land you own. This cannot be undone.",
        "Entlässt das Ziel als Ihre Marionette aus eigenem Gebiet. Nicht rückgängig zu machen.",
        "Libère la cible comme vassal à partir de vos territoires. Irréversible.",
        "Освобождает цель как вашу марионетку из ваших земель. Необратимо."
    ),
    "free_target": (
        "Ends your control over the target country entirely. This cannot be undone.",
        "Beendet Ihre Kontrolle über das Zielland vollständig. Nicht rückgängig zu machen.",
        "Met fin à votre contrôle sur le pays ciblé. Irréversible.",
        "Полностью прекращает ваш контроль над целевой страной. Необратимо."
    ),
}

FAMILY_HELP: dict[str, Row] = {
    "resource_": HELP_RESOURCE,
    "popularity_": HELP_POPULARITY,
    "ruling_": HELP_RULING,
    "divisions_": HELP_DIVISIONS,
}

BUILDING_HELP = {
    "infrastructure": HELP_BUILDING,
    "civilian": HELP_BUILDING,
    "military": HELP_BUILDING,
    "airbase": HELP_BUILDING,
    "radar": HELP_BUILDING,
    "antiair": HELP_BUILDING,
    "fort": HELP_BUILDING,
    "supply_hub": HELP_BUILDING,
    "slots": HELP_BUILDING,
    "dockyard": HELP_COASTAL,
    "coastal_fort": HELP_COASTAL,
    "mines": HELP_COASTAL,
    "offsite_civilian": HELP_BUILDING,
    "offsite_military": HELP_BUILDING,
}

LEADER_SLUGS = {"skill", "attack", "defense", "planning", "logistics", "admiral_skill"}


def title_for(slug: str) -> Row:
    if slug.startswith("resource_"):
        return RESOURCE_NOUNS[slug[len("resource_") :]]
    if slug.startswith("popularity_"):
        return IDEOLOGY_NOUNS[slug[len("popularity_") :]]
    if slug.startswith("ruling_"):
        return IDEOLOGY_NOUNS[slug[len("ruling_") :]]
    return TITLES[slug]


def help_for(slug: str) -> Row:
    for prefix, row in FAMILY_HELP.items():
        if slug.startswith(prefix):
            return row
    if slug in BUILDING_HELP:
        return BUILDING_HELP[slug]
    if slug in LEADER_SLUGS:
        return HELP_LEADER
    return HELPS[slug]
