<p align="center">
  <img src="logo.png" alt="HOI4 Cheat Control Panel" width="320">
</p>

<h1 align="center">Hearts of Iron IV — Cheat Control Panel</h1>

<p align="center">
  A categorised, searchable, tooltip-driven in-game control panel that replaces console typing.
  <br>
  <strong>Target game version 1.19.2 · MIT licensed · Singleplayer</strong>
</p>

---

## Overview

Hearts of Iron IV's console is powerful and unpleasant. It requires memorising internal
identifiers like `infantry_equipment_3`, offers no discovery, no validation, and no undo.

The Cheat Control Panel turns those commands into a real interface:

```
Console:  add_equipment 1000 infantry_equipment_3
Panel:    Equipment → Infantry Equipment III → Amount 1000 → ADD
```

It is an **additive** mod. It overrides no vanilla file, so it coexists with most other
mods, and every identifier it defines is prefixed `ccp_`.

## Status

**0.1.0 — in development.** This section is updated honestly as each module lands; see
`MEMORY.md` for per-phase status and `CHANGELOG.md` for the release history.

## Features

Planned modules, each shipping only what the engine genuinely supports:

- **Dashboard** — live country summary and one-click resource top-ups
- **Resources** — political power, army/navy/air XP, command power, manpower
- **Equipment Manager** — every equipment type in your install, by category, with an
  "add latest version" shortcut
- **Research** — grant technologies individually, by category, or in bulk
- **Country** — play as another country, annex, puppet, release, change ideology
- **States** — click a state on the map to inspect it, transfer ownership, manage cores and claims
- **Diplomacy & War** — declare war, white peace, relations, guarantees
- **Construction & Production** — set building levels directly, manage production lines
- **National Focus & Characters** — complete or unlock focuses, edit commander XP and traits
- **Command Builder** — compose an action from type, target and amount, see the exact
  equivalent command, then execute it
- **Settings** — remap the hotkey, toggle confirmation prompts

## Opening the panel

Default hotkey: **`Ctrl+F8`**.

Plain `F8` is deliberately not the default because vanilla already binds it to a map mode —
using it would switch the map mode every time you opened the panel. You can change the
hotkey to `F8`, `F11` or `F12` from the panel's **Settings** tab; the choice is stored in
your save.

## Languages

The panel ships in **English, German, French and Russian**. It follows whatever
language the game is set to — no configuration needed.

**Turkish and Dutch are translated but cannot ship as languages.** Hearts of Iron IV
loads exactly ten localisation folders, listed in the game's own
`localisation/languages.yml`, and neither Turkish nor Dutch is among them; a
`localisation/turkish/` folder is ignored by the engine. Both translations are
therefore kept in `extras/language_overlays/` under English keys and applied on
request:

```bash
python tools/install_local.py
python tools/set_panel_language.py turkish    # or: dutch
```

That changes this panel only; the game stays in whatever language you had.
Reinstalling resets the panel to English.

## Requirements

- Hearts of Iron IV **1.19.x** (developed and tested against 1.19.2)
- No DLC required. DLC-specific content appears only when you own the relevant DLC.

## Installation

**Steam Workshop** — subscribe, then enable the mod in the Paradox Launcher playset.

**Manual** — copy the `mod/` directory into
`Documents/Paradox Interactive/Hearts of Iron IV/mod/hoi4_cheat_control_panel/`
and place the accompanying `.mod` descriptor alongside it.

## Compatibility

- **Singleplayer.** Several actions (country switching, annexation, state transfer) carry a
  real desync risk and are hidden in multiplayer. No claim of multiplayer safety is made.
- **Ironman / achievements.** Enabling any mod disables achievements. This mod makes no
  Ironman-compatibility claim.
- **Other mods.** Nothing vanilla is overridden and every identifier is namespaced, so
  conflicts are unlikely. Total conversions that replace the GUI wholesale are untested.

## Known limitations

These are engine limits, verified against the shipped game files, not oversights:

| Limitation | Consequence |
|---|---|
| Scripted GUIs cannot read text input | Custom amounts use a digit pad; search uses category and A-Z filters instead of typing |
| Console-only commands are unreachable from script | Effects with no scripted equivalent (fog of war, AI acceptance) ship disabled with an explanatory tooltip |
| No state snapshot API | There is no undo. Destructive actions require confirmation instead |
| Equipment and technology cannot be iterated at runtime | Their lists are generated from your game files at build time rather than live |
| No keybind remapping API | The hotkey is chosen from a fixed set of options rather than freely bound |
| Only ten localisation folders exist | Turkish and Dutch ship as an overlay rather than as selectable languages |

## Development

```bash
python tools/build_assets.py       # draw the interface plates and sprite definitions
python tools/build_interface.py    # generate the .gui files, scripts, strings and descriptor
python tools/generate_data.py      # derive the equipment catalogue from the installed game
python tools/validate_mod.py       # release checklist
python tools/install_local.py      # install into the game for testing
python tools/enable_local_mod.py   # register it in the launcher playset
```

Nothing under `mod/` is edited by hand — it is all generated from `tools/ccp/`.

See `CLAUDE.md` for conventions, `CONTRIBUTING.md` for the contribution workflow, and
`docs/` for architecture, modding notes, testing and the release process.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Created by [X1NPAR1](https://github.com/X1NPAR1).

Hearts of Iron IV is a trademark of Paradox Interactive AB. This is an unofficial,
fan-made modification and is not affiliated with or endorsed by Paradox Interactive.
No assets from other mods are used.
