<p align="center">
  <img src="logo.png" alt="HOI4 Cheat Control Panel" width="320">
</p>

<h1 align="center">Hearts of Iron IV — Cheat Control Panel</h1>

<p align="center">
  A categorised, tooltip-driven in-game control panel that replaces console typing.
  <br>
  <strong>Hearts of Iron IV 1.19 · MIT licensed · singleplayer</strong>
</p>

---

## Overview

Hearts of Iron IV's console is powerful and unpleasant. It expects you to memorise
identifiers like `infantry_equipment_3`, offers no discovery, no validation and no undo.

The Cheat Control Panel turns those actions into a real interface:

```
Console:  add_equipment 1000 infantry_equipment_3
Panel:    Equipment → Infantry → Infantry Equipment III → ADD
```

It is an **additive** mod. It overrides no vanilla file — a release check enforces
that — and every identifier it defines is prefixed `ccp_`, so it sits alongside
other mods rather than fighting them.

## Opening the panel

Default hotkey: **`Insert`**. There is also a logo button below the top bar.

Plain `F8` is not the default because vanilla already binds it to a map mode, so
it would switch the map mode every time you opened the panel. You can change the
hotkey to `F8`, `F11`, `F12` or `Ctrl+F8` in the panel's **Settings**; the choice
is stored in your save.

## Sections

| Section | What it does |
|---|---|
| **Dashboard** | Live country summary: political power, command power, manpower, army/navy/air experience, stability, factories |
| **Resources** | Grant any of those six resources, with scaled presets and a custom amount |
| **Equipment** | Every addable equipment variant in your installation, grouped by category, sixteen to a page, with ADD and LATEST |
| **Research** | Every technology, grouped by the research folder the game assigns it, granted one at a time or a folder at once |
| **Countries** | Every country in the running game: annex, puppet, declare war, white peace, play as |
| **States** | Every state: take, add core, remove core, add claim — from the list or by clicking the map |
| **Nation** | Stability, war support, research slots, fuel |
| **Construction** | Infrastructure, factories, dockyards, air bases, radar and anti-air, built instantly across every owned state, plus off-map factories |
| **Commanders** | Skill, attack, defence, planning and logistics for every general and admiral |
| **History** | The last ten actions the panel applied, each repeatable |
| **Settings** | Hotkey, confirmation prompts, compatibility and language notes |

Sections appear only when they do something. Nothing in the panel is a placeholder.

## Languages

The panel ships in **English, German, French and Russian** and follows the game's
own language setting.

**Turkish and Dutch are translated but cannot ship as languages.** Hearts of Iron IV
loads exactly ten localisation folders, listed in the game's own
`localisation/languages.yml`, and neither Turkish nor Dutch is among them — a
`localisation/turkish/` folder is ignored by the engine. Both translations live in
`extras/language_overlays/` under English keys and are applied on request:

```bash
python tools/install_local.py
python tools/set_panel_language.py turkish    # or: dutch
```

That changes the panel only; the game stays in whatever language you had.
Reinstalling resets the panel to English.

## Requirements

- Hearts of Iron IV **1.19.x** (developed against 1.19.2)
- No DLC required. DLC-specific content appears only if you own the relevant DLC.
- Python 3.10+ and Pillow, for the build tooling only — not to play the mod.

## Installation

**Steam Workshop** — [subscribe here](https://steamcommunity.com/sharedfiles/filedetails/?id=3790658065), then enable the mod in your Paradox Launcher playset.

**From source**

```bash
python tools/build_assets.py       # draw the interface plates and sprite definitions
python tools/build_interface.py    # generate the .gui files, scripts, strings and descriptor
python tools/generate_data.py      # derive equipment and technology from your installation
python tools/validate_mod.py       # release checklist
python tools/install_local.py      # copy into the game's mod directory
python tools/enable_local_mod.py   # register it in the launcher playset (launcher closed)
```

If the launcher shows the mod but the game starts without it, check that a playset
is actually active — an inactive playset makes the launcher start the game with no
mods at all. `enable_local_mod.py` fixes that and backs the launcher database up first.

## Compatibility

- **Singleplayer.** Country switching, annexation and state transfers can desync a
  multiplayer game. The engine gives script no way to detect a multiplayer session
  (`is_ironman` exists, `is_multiplayer` does not), so the panel cannot hide those
  actions automatically and says so instead of gating on a check that never fires.
- **Ironman and achievements.** Running any mod disables achievements. No Ironman
  compatibility is claimed.
- **Other mods.** No vanilla file is overridden and every identifier is namespaced.
  Total conversions that replace the interface wholesale are untested.

## Known limitations

These are engine limits, verified against the shipped game files, not oversights.

| Limitation | Consequence |
|---|---|
| Scripted GUIs cannot read text input | Custom amounts use a digit pad; browsing uses categories and pages rather than typing a search |
| Console commands cannot be invoked from script | Anything with no native equivalent — fog of war, AI acceptance — is absent rather than present and broken |
| No state snapshot API | There is no undo. Destructive actions require confirmation instead |
| Equipment and technology cannot be enumerated at runtime | Their lists are derived from your game files when the mod is built |
| No keybind remapping API | The hotkey is chosen from a fixed set rather than freely bound |
| `complete_national_focus` needs a specific focus token, and focus trees cannot be walked at runtime | There is no national focus section |
| Doctrines are a separate system since 1.19 | `set_technology` does not reach them, so Research does not list them |
| Only ten localisation folders exist | Turkish and Dutch ship as an overlay rather than as selectable languages |

## How it is built

Nothing under `mod/` is written by hand. `tools/ccp/` holds the registries — the
design grid, the sections, the actions, the strings — and the build scripts emit
the `.gui` files, the scripted GUI, the effects, the scripted localisation, the
localisation files and the descriptor from them. Positions are computed from one
grid rather than typed twice, and a button cannot exist without an effect behind
it, a name in every language and a destination in the navigation.

Equipment and technology are parsed from your own installation, so the lists are
real game data rather than a hand-maintained copy that drifts out of date.

`tools/validate_mod.py` runs the release checklist: descriptor validity, brace
balance, sprite and texture references, GUI element references, effect references,
vanilla overrides, placeholder text, localisation encoding, parity and coverage,
and Workshop payload cleanliness.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Created by [X1NPAR1](https://github.com/X1NPAR1).

Hearts of Iron IV is a trademark of Paradox Interactive AB. This is an unofficial,
fan-made modification, not affiliated with or endorsed by Paradox Interactive. No
assets from other mods are used.
