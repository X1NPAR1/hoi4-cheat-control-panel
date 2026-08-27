"""Names and explanations for every action, in all six languages.

Kept apart from `strings.py` because the action registry is where most of the
panel's text now lives. Repetitive families — the seven resources, the four
ideologies — get their noun translated once and share a sentence template, so a
new member of a family needs one line rather than eighteen.
"""

from __future__ import annotations

Row = tuple[str, str, str, str, str, str]

# ---------------------------------------------------------------- shared sentences

HELP_BUILDING: Row = (
    "Built instantly in every state you own.",
    "Wird sofort in jedem Ihrer Staaten gebaut.",
    "Construit instantanément dans chacun de vos États.",
    "Мгновенно строится во всех ваших провинциях.",
    "Sahip olduğunuz her eyalette anında inşa edilir.",
    "Wordt direct gebouwd in elke staat die je bezit.",
)

HELP_COASTAL: Row = (
    "Built instantly in every coastal state you own.",
    "Wird sofort in jedem Ihrer Küstenstaaten gebaut.",
    "Construit instantanément dans chacun de vos États côtiers.",
    "Мгновенно строится во всех ваших прибрежных провинциях.",
    "Sahip olduğunuz her kıyı eyaletinde anında inşa edilir.",
    "Wordt direct gebouwd in elke kuststaat die je bezit.",
)

HELP_RESOURCE: Row = (
    "Adds this resource to every state you own.",
    "Fügt jedem Ihrer Staaten diese Ressource hinzu.",
    "Ajoute cette ressource à chacun de vos États.",
    "Добавляет этот ресурс во все ваши провинции.",
    "Sahip olduğunuz her eyalete bu kaynağı ekler.",
    "Voegt deze grondstof toe aan elke staat die je bezit.",
)

HELP_POPULARITY: Row = (
    "Raises this ideology's share of the popular vote.",
    "Erhöht den Stimmenanteil dieser Ideologie.",
    "Augmente la part de cette idéologie dans l'opinion.",
    "Повышает долю этой идеологии в общественном мнении.",
    "Bu ideolojinin halk desteğindeki payını artırır.",
    "Verhoogt het aandeel van deze ideologie in de publieke opinie.",
)

HELP_RULING: Row = (
    "Puts this ideology in power immediately. Elections stay allowed.",
    "Bringt diese Ideologie sofort an die Macht. Wahlen bleiben erlaubt.",
    "Porte cette idéologie au pouvoir immédiatement. Les élections restent autorisées.",
    "Немедленно приводит эту идеологию к власти. Выборы остаются разрешёнными.",
    "Bu ideolojiyi anında iktidara getirir. Seçimler açık kalır.",
    "Brengt deze ideologie meteen aan de macht. Verkiezingen blijven toegestaan.",
)

HELP_LEADER: Row = (
    "Applies to every commander you have right now, not to future ones.",
    "Gilt für alle derzeitigen Befehlshaber, nicht für künftige.",
    "S'applique à tous vos commandants actuels, pas aux futurs.",
    "Действует на нынешних командующих, но не на будущих.",
    "Şu anki tüm komutanlarınıza uygulanır, gelecektekilere değil.",
    "Geldt voor al je huidige bevelhebbers, niet voor toekomstige.",
)

HELP_DIVISIONS: Row = (
    "Spawns divisions in your capital from a template this mod adds. The template stays in your list.",
    "Stellt Divisionen in Ihrer Hauptstadt aus einer Vorlage dieses Mods auf. Die Vorlage bleibt in Ihrer Liste.",
    "Fait apparaître des divisions dans votre capitale à partir d'un modèle ajouté par ce mod. Le modèle reste dans votre liste.",
    "Создаёт дивизии в столице по шаблону, который добавляет этот мод. Шаблон остаётся в вашем списке.",
    "Bu modun eklediği bir şablondan başkentinizde tümen üretir. Şablon listenizde kalır.",
    "Plaatst divisies in je hoofdstad vanuit een sjabloon dat deze mod toevoegt. Het sjabloon blijft in je lijst.",
)

# ---------------------------------------------------------------- per-action titles

TITLES: dict[str, Row] = {
    # nation
    "stability": ("Stability", "Stabilität", "Stabilité", "Стабильность", "İstikrar", "Stabiliteit"),
    "stability_full": ("Stability to full", "Stabilität auf Maximum", "Stabilité au maximum", "Стабильность на максимум", "İstikrarı tam yap", "Stabiliteit naar maximum"),
    "stability_zero": ("Stability to zero", "Stabilität auf null", "Stabilité à zéro", "Стабильность в ноль", "İstikrarı sıfırla", "Stabiliteit naar nul"),
    "war_support": ("War support", "Kriegsunterstützung", "Soutien à la guerre", "Поддержка войны", "Savaş desteği", "Oorlogssteun"),
    "war_support_full": ("War support to full", "Kriegsunterstützung auf Maximum", "Soutien au maximum", "Поддержка на максимум", "Savaş desteğini tam yap", "Oorlogssteun naar maximum"),
    "war_support_zero": ("War support to zero", "Kriegsunterstützung auf null", "Soutien à zéro", "Поддержка в ноль", "Savaş desteğini sıfırla", "Oorlogssteun naar nul"),
    "research_slots": ("Research slots", "Forschungsplätze", "Emplacements de recherche", "Слоты исследований", "Araştırma yuvaları", "Onderzoeksplekken"),
    "fuel": ("Fuel", "Treibstoff", "Carburant", "Топливо", "Yakıt", "Brandstof"),
    "cic": ("Market funds", "Marktmittel", "Fonds de marché", "Рыночные средства", "Pazar fonu", "Marktfondsen"),
    "threat": ("World tension", "Weltspannung", "Tension mondiale", "Мировая напряжённость", "Dünya gerginliği", "Wereldspanning"),
    "legitimacy": ("Legitimacy", "Legitimität", "Légitimité", "Легитимность", "Meşruiyet", "Legitimiteit"),
    # construction
    "infrastructure": ("Infrastructure", "Infrastruktur", "Infrastructure", "Инфраструктура", "Altyapı", "Infrastructuur"),
    "civilian": ("Civilian factories", "Zivilfabriken", "Usines civiles", "Гражданские заводы", "Sivil fabrikalar", "Civiele fabrieken"),
    "military": ("Military factories", "Militärfabriken", "Usines militaires", "Военные заводы", "Askeri fabrikalar", "Militaire fabrieken"),
    "dockyard": ("Dockyards", "Werften", "Chantiers navals", "Верфи", "Tersaneler", "Scheepswerven"),
    "airbase": ("Air bases", "Flugplätze", "Bases aériennes", "Аэродромы", "Hava üsleri", "Vliegbases"),
    "radar": ("Radar stations", "Radarstationen", "Stations radar", "Радары", "Radar istasyonları", "Radarstations"),
    "antiair": ("Anti-air", "Flugabwehr", "Antiaérien", "ПВО", "Uçaksavar", "Luchtafweer"),
    "fort": ("Land forts", "Landbefestigungen", "Fortifications terrestres", "Сухопутные форты", "Kara istihkâmları", "Landforten"),
    "coastal_fort": ("Coastal forts", "Küstenbefestigungen", "Fortifications côtières", "Береговые форты", "Kıyı istihkâmları", "Kustforten"),
    "supply_hub": ("Supply hub", "Nachschubzentrum", "Centre de ravitaillement", "Узел снабжения", "İkmal merkezi", "Bevoorradingshub"),
    "slots": ("Building slots", "Bauplätze", "Emplacements de construction", "Слоты построек", "Yapı yuvaları", "Bouwplekken"),
    "offsite_civilian": ("Off-map civilian factories", "Zivilfabriken ausserhalb der Karte", "Usines civiles hors carte", "Гражданские заводы вне карты", "Harita dışı sivil fabrikalar", "Civiele fabrieken buiten de kaart"),
    "offsite_military": ("Off-map military factories", "Militärfabriken ausserhalb der Karte", "Usines militaires hors carte", "Военные заводы вне карты", "Harita dışı askeri fabrikalar", "Militaire fabrieken buiten de kaart"),
    "mines": ("Naval mines", "Seeminen", "Mines navales", "Морские мины", "Deniz mayınları", "Zeemijnen"),
    # politics
    "civil_war": ("Start a civil war", "Bürgerkrieg auslösen", "Déclencher une guerre civile", "Начать гражданскую войну", "İç savaş başlat", "Burgeroorlog beginnen"),
    "autonomy": ("Raise autonomy", "Autonomie erhöhen", "Augmenter l'autonomie", "Повысить автономию", "Özerkliği artır", "Autonomie verhogen"),
    "autonomy_down": ("Lower autonomy", "Autonomie senken", "Réduire l'autonomie", "Понизить автономию", "Özerkliği azalt", "Autonomie verlagen"),
    # military
    "nukes": ("Nuclear bombs", "Atombomben", "Bombes nucléaires", "Ядерные бомбы", "Nükleer bombalar", "Kernbommen"),
    "divisions_infantry": ("Infantry divisions", "Infanteriedivisionen", "Divisions d'infanterie", "Пехотные дивизии", "Piyade tümenleri", "Infanteriedivisies"),
    "divisions_armor": ("Armoured divisions", "Panzerdivisionen", "Divisions blindées", "Танковые дивизии", "Zırhlı tümenler", "Pantserdivisies"),
    "divisions_motorized": ("Motorized divisions", "Motorisierte Divisionen", "Divisions motorisées", "Моторизованные дивизии", "Motorize tümenler", "Gemotoriseerde divisies"),
    "delete_units": ("Disband every division", "Alle Divisionen auflösen", "Dissoudre toutes les divisions", "Расформировать все дивизии", "Tüm tümenleri dağıt", "Alle divisies ontbinden"),
    "army_xp": ("Army experience", "Heereserfahrung", "Expérience terrestre", "Опыт армии", "Ordu tecrübesi", "Legerervaring"),
    "navy_xp": ("Navy experience", "Marineerfahrung", "Expérience navale", "Опыт флота", "Donanma tecrübesi", "Marine-ervaring"),
    "air_xp": ("Air experience", "Luftwaffenerfahrung", "Expérience aérienne", "Опыт авиации", "Hava tecrübesi", "Luchtmachtervaring"),
    # commanders
    "skill": ("General skill", "Generalsstufe", "Compétence des généraux", "Навык генералов", "General becerisi", "Generaalvaardigheid"),
    "attack": ("Attack", "Angriff", "Attaque", "Атака", "Saldırı", "Aanval"),
    "defense": ("Defence", "Verteidigung", "Défense", "Защита", "Savunma", "Verdediging"),
    "planning": ("Planning", "Planung", "Planification", "Планирование", "Planlama", "Planning"),
    "logistics": ("Logistics", "Logistik", "Logistique", "Логистика", "Lojistik", "Logistiek"),
    "admiral_skill": ("Admiral skill", "Admiralsstufe", "Compétence des amiraux", "Навык адмиралов", "Amiral becerisi", "Admiraalvaardigheid"),
}

RESOURCE_NOUNS: dict[str, Row] = {
    "oil": ("Oil", "Öl", "Pétrole", "Нефть", "Petrol", "Olie"),
    "aluminium": ("Aluminium", "Aluminium", "Aluminium", "Алюминий", "Alüminyum", "Aluminium"),
    "rubber": ("Rubber", "Gummi", "Caoutchouc", "Резина", "Kauçuk", "Rubber"),
    "tungsten": ("Tungsten", "Wolfram", "Tungstène", "Вольфрам", "Tungsten", "Wolfraam"),
    "steel": ("Steel", "Stahl", "Acier", "Сталь", "Çelik", "Staal"),
    "chromium": ("Chromium", "Chrom", "Chrome", "Хром", "Krom", "Chroom"),
    "coal": ("Coal", "Kohle", "Charbon", "Уголь", "Kömür", "Kolen"),
}

IDEOLOGY_NOUNS: dict[str, Row] = {
    "democratic": ("Democratic", "Demokratisch", "Démocratique", "Демократия", "Demokratik", "Democratisch"),
    "communism": ("Communist", "Kommunistisch", "Communiste", "Коммунизм", "Komünist", "Communistisch"),
    "fascism": ("Fascist", "Faschistisch", "Fasciste", "Фашизм", "Faşist", "Fascistisch"),
    "neutrality": ("Non-aligned", "Blockfrei", "Non-aligné", "Нейтралитет", "Bağlantısız", "Niet-gebonden"),
}

HELPS: dict[str, Row] = {
    "stability": (
        "Raises national stability by the chosen amount.",
        "Erhöht die nationale Stabilität um den gewählten Wert.",
        "Augmente la stabilité nationale du montant choisi.",
        "Повышает стабильность на выбранную величину.",
        "Ulusal istikrarı seçilen kadar artırır.",
        "Verhoogt de nationale stabiliteit met het gekozen bedrag.",
    ),
    "war_support": (
        "Raises war support by the chosen amount.",
        "Erhöht die Kriegsunterstützung um den gewählten Wert.",
        "Augmente le soutien à la guerre du montant choisi.",
        "Повышает поддержку войны на выбранную величину.",
        "Savaş desteğini seçilen kadar artırır.",
        "Verhoogt de oorlogssteun met het gekozen bedrag.",
    ),
    "stability_full": (
        "Sets stability to its maximum.",
        "Setzt die Stabilität auf das Maximum.",
        "Porte la stabilité au maximum.",
        "Устанавливает максимальную стабильность.",
        "İstikrarı en yükseğe çeker.",
        "Zet de stabiliteit op het maximum.",
    ),
    "war_support_full": (
        "Sets war support to its maximum.",
        "Setzt die Kriegsunterstützung auf das Maximum.",
        "Porte le soutien à la guerre au maximum.",
        "Устанавливает максимальную поддержку войны.",
        "Savaş desteğini en yükseğe çeker.",
        "Zet de oorlogssteun op het maximum.",
    ),
    "stability_zero": (
        "Drops stability to nothing. Useful for triggering a civil war, and hard to walk back.",
        "Senkt die Stabilität auf null. Nützlich für einen Bürgerkrieg und schwer rückgängig zu machen.",
        "Réduit la stabilité à zéro. Utile pour déclencher une guerre civile, difficile à corriger.",
        "Обнуляет стабильность. Полезно для гражданской войны и трудно исправимо.",
        "İstikrarı sıfıra düşürür. İç savaş için kullanışlı, geri dönmesi zor.",
        "Zet de stabiliteit op nul. Handig voor een burgeroorlog en lastig terug te draaien.",
    ),
    "war_support_zero": (
        "Drops war support to nothing.",
        "Senkt die Kriegsunterstützung auf null.",
        "Réduit le soutien à la guerre à zéro.",
        "Обнуляет поддержку войны.",
        "Savaş desteğini sıfıra düşürür.",
        "Zet de oorlogssteun op nul.",
    ),
    "research_slots": (
        "Sets how many technologies you can research at once. Five is the game's maximum.",
        "Legt fest, wie viele Technologien Sie gleichzeitig erforschen. Fünf ist das Maximum des Spiels.",
        "Définit le nombre de recherches simultanées. Cinq est le maximum du jeu.",
        "Задаёт число одновременных исследований. Пять — максимум игры.",
        "Aynı anda kaç teknoloji araştırabileceğinizi belirler. Oyunun üst sınırı beştir.",
        "Bepaalt hoeveel technologieën je tegelijk onderzoekt. Vijf is het maximum.",
    ),
    "fuel": (
        "Adds fuel to your reserves.",
        "Fügt Ihren Reserven Treibstoff hinzu.",
        "Ajoute du carburant à vos réserves.",
        "Добавляет топливо в резервы.",
        "Rezervlerinize yakıt ekler.",
        "Voegt brandstof toe aan je reserves.",
    ),
    "cic": (
        "Adds funds to the international market account.",
        "Fügt dem Konto des internationalen Marktes Mittel hinzu.",
        "Ajoute des fonds au compte du marché international.",
        "Добавляет средства на счёт международного рынка.",
        "Uluslararası pazar hesabınıza fon ekler.",
        "Voegt geld toe aan de rekening van de internationale markt.",
    ),
    "threat": (
        "Raises world tension, which unlocks wars and interventions.",
        "Erhöht die Weltspannung, was Kriege und Interventionen freischaltet.",
        "Augmente la tension mondiale, ce qui débloque guerres et interventions.",
        "Повышает мировую напряжённость, открывая войны и вмешательства.",
        "Dünya gerginliğini artırır; savaşların ve müdahalelerin önünü açar.",
        "Verhoogt de wereldspanning, wat oorlogen en interventies ontgrendelt.",
    ),
    "legitimacy": (
        "Raises the legitimacy of a government in exile.",
        "Erhöht die Legitimität einer Exilregierung.",
        "Augmente la légitimité d'un gouvernement en exil.",
        "Повышает легитимность правительства в изгнании.",
        "Sürgündeki bir hükûmetin meşruiyetini artırır.",
        "Verhoogt de legitimiteit van een regering in ballingschap.",
    ),
    "civil_war": (
        "Splits the country and hands the chosen share to communist rebels. There is no way back from this.",
        "Spaltet das Land und übergibt kommunistischen Rebellen den gewählten Anteil. Davon gibt es kein Zurück.",
        "Divise le pays et donne la part choisie aux rebelles communistes. Aucun retour possible.",
        "Раскалывает страну и отдаёт выбранную долю коммунистическим повстанцам. Пути назад нет.",
        "Ülkeyi böler ve seçilen payı komünist isyancılara verir. Bunun geri dönüşü yok.",
        "Splitst het land en geeft het gekozen deel aan communistische rebellen. Hier is geen weg terug.",
    ),
    "autonomy": (
        "Moves a subject closer to independence.",
        "Bringt einen Vasallen der Unabhängigkeit näher.",
        "Rapproche un vassal de l'indépendance.",
        "Приближает вассала к независимости.",
        "Bir tabiyi bağımsızlığa yaklaştırır.",
        "Brengt een vazal dichter bij onafhankelijkheid.",
    ),
    "autonomy_down": (
        "Pulls a subject further under your control.",
        "Zieht einen Vasallen stärker unter Ihre Kontrolle.",
        "Resserre votre contrôle sur un vassal.",
        "Усиливает ваш контроль над вассалом.",
        "Bir tabiyi kontrolünüz altına daha çok çeker.",
        "Trekt een vazal verder onder jouw controle.",
    ),
    "nukes": (
        "Adds ready nuclear bombs to your stockpile.",
        "Fügt Ihrem Lager einsatzbereite Atombomben hinzu.",
        "Ajoute des bombes nucléaires prêtes à l'emploi.",
        "Добавляет готовые ядерные бомбы на склад.",
        "Stoğunuza kullanıma hazır nükleer bomba ekler.",
        "Voegt inzetbare kernbommen toe aan je voorraad.",
    ),
    "delete_units": (
        "Disbands every division you have. There is no undo.",
        "Löst jede Ihrer Divisionen auf. Es gibt kein Rückgängig.",
        "Dissout toutes vos divisions. Aucune annulation.",
        "Расформировывает все ваши дивизии. Отмены нет.",
        "Sahip olduğunuz her tümeni dağıtır. Geri alınamaz.",
        "Ontbindt al je divisies. Er is geen ongedaan maken.",
    ),
    "army_xp": (
        "Army experience, spent on division templates.",
        "Heereserfahrung, für Divisionsvorlagen.",
        "Expérience terrestre, dépensée sur les modèles de division.",
        "Опыт армии, тратится на шаблоны дивизий.",
        "Tümen şablonlarında harcanan ordu tecrübesi.",
        "Legerervaring, besteed aan divisiesjablonen.",
    ),
    "navy_xp": (
        "Navy experience, spent on ship designs.",
        "Marineerfahrung, für Schiffsentwürfe.",
        "Expérience navale, dépensée sur les modèles de navire.",
        "Опыт флота, тратится на проекты кораблей.",
        "Gemi tasarımlarında harcanan donanma tecrübesi.",
        "Marine-ervaring, besteed aan scheepsontwerpen.",
    ),
    "air_xp": (
        "Air experience, spent on aircraft designs.",
        "Luftwaffenerfahrung, für Flugzeugentwürfe.",
        "Expérience aérienne, dépensée sur les modèles d'avion.",
        "Опыт авиации, тратится на проекты самолётов.",
        "Uçak tasarımlarında harcanan hava tecrübesi.",
        "Luchtmachtervaring, besteed aan vliegtuigontwerpen.",
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
