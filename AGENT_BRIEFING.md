# Agent Briefing — Royal-Animation → "Ali Baba" VN

This repo started as a Pygame Elden Ring fan animation engine
(`Royal-Animation`) and is being converted into a visual-novel adaptation
of *Ali Baba and the Forty Thieves*, told from Marjana's POV.

If you are an AI agent landing here for the first time: read this file
and `STORY.md`, then read `data/map/preset/1/1/1/event.csv` to see how a
real mission looks. That's enough to be productive.

## Run it

```sh
# from repo root, in the venv
python main.py
```

If pygame fails on Python 3.14 with "no module named pygame.mixer" — the
fix is `pygame-ce` (community edition) instead of vanilla pygame:

```sh
pip uninstall pygame
pip install pygame-ce pyperclip screeninfo Pillow
```

Don't use `pip install -r requirements.txt` blindly — it pins
`pywin32~=310` which is invalid on macOS/Linux.

## High-level architecture

- **`main.py`** — entry point. Boots `engine.game.Game`.
- **`engine/game/`** — game shell, menu, save/load, state machine.
- **`engine/battle/`** — the per-mission runtime ("battle" is legacy
  naming from the Elden Ring origin; here it just means "mission scene").
  - `prepare_new_stage` loads `character_pos.csv` + `event.csv` and
    spawns characters/cameras.
  - `event_process.py` is the cutscene event interpreter — every event
    in `event.csv` flows through here.
  - `cutscene_player_input.py` handles player clicks during dialog and
    branches on yes/no/choice events.
- **`engine/character/`** — character sprite, animation, body parts.
  Speech routing lives in `character_event_process.py` → `start_speech`.
- **`engine/uibattle/uibattle.py`** — UI widgets. The two relevant ones:
  - `JRPGDialogueBox` (lines ~1091–1248): JRPG-style dialog with
    portrait, speaker name bracket, click-to-advance, fade-in/out.
    Used whenever an event has a `portrait` property.
  - `ChoicePopup`: A/B button popup for branching choices.
- **`engine/scene/scene.py`** — background panels. Holds cross-fade
  state for `bgchange` with `fade` (snapshot of old image, blit over
  new with decreasing alpha).
- **`engine/stageobject/stageobject.py`** — non-character world objects
  (donkeys, gold sacks). Loaded from `data/animation/sprite/object/<id>/<chapter>/0.png`.

## Coordinate system

World is `3840 × 2160`. Everything in CSVs (POS, character_pos, etc.)
is in world coordinates. `screen_scale = (actual_w/3840, actual_h/2160)`
applies on render.

- `Y = 1750` is "feet on ground level" for characters.
- For stage objects, the rendered `pos` is the **center** of the sprite,
  so adjust Y up by half the sprite height to get feet on the ground.

## CSV formats (the only ones that matter)

### `data/map/preset/1/<mission>/1/event.csv`

Columns: `ID, Text ID, Object, Animation, Type, Trigger, Property`.

- **`ID`** is non-empty only on the *parent* row (typically `event` for
  the music-start event). Every subsequent row is a child of that parent.
- **`Type`** drives behaviour: `cutscene`, `bgchange`, `music`, `place`,
  `delete`, `hide`, `show`, `create`, `weather`, `sound`, `ambient`, etc.
- **`Property`** is a comma-list of `key:value` pairs. Tuple values use
  semicolons inside parens, e.g. `POS:(900;1600)` (NOT commas inside the
  tuple — the dict parser splits on `,` first).
  - `wait` — block until the user clicks (or until the inner timer ends)
  - `hold` — keep the speech box visible after the line plays out
  - `interact` — wait for user click before firing the event
  - `instant fade` — set blackout alpha to 255 immediately
  - `no auto fade out` — blackout stays after `wait` (use a follow-up
    blackout to fade back in)
  - `portrait:<name>` — route through JRPG dialog box, looks up
    `data/portrait/<name>.png`
  - `side:left|right` — which side of the screen the portrait sits on
  - `speaker:Some Name` — speaker label shown in the bracket
  - `voice:(soundname;distance;shake)` — sample played per character of
    text. We use `Parchment_write` for typewriter sound.
  - `select:choice` with `choice_a:Label`, `choice_b:Label` — open the
    `ChoicePopup`. Subsequent events with `Trigger="yes"`/`Trigger="no"`
    are filtered to whichever the player picked.
- For `bgchange` rows: `Object` is the bg image name (without `.png`),
  `Property` is `scene:1,POS:1,fade` — the `fade` flag triggers cross-fade.

### `data/map/preset/1/<mission>/1/character_pos.csv`

Columns: `Object ID, ID, Camera, Scene, POS, Ground Y POS, Direction, Stage Property`.

- `Object ID` = in-game name used in events (e.g. `Mariana`, `Alibaba`).
- `ID` = lookup key into `data/character/character.csv`. Legacy ER
  names — e.g. `Trina` is Mariana's sprite key, `Miquella` is Ali Baba's.
- `POS` is `"x,y"` (comma-separated, no parens — different from event.csv).

## Assets — what exists today

### Backgrounds (`data/map/scene/1/`)

- `forest_outside_cave.png`, `forest_outside_cave_half_open.png`, `forest_outside_cave_open.png` (3-frame door animation)
- `cave.png` — cave interior
- `alibaba_house.png` — exterior
- `alibaba_house_exterior_night.png`
- `alibaba_garden.png`
- `qasim_house.png`
- `dining_hall.png`
- `courtyard_night.png`
- `city_street.png`
- `baba_mustafa_cobbler_shop.png`
- `teaparty_1.png`, `teaparty_2.png` (legacy ER, unused)

**Missing**: `alibaba_house_interior.png` for the home-discovery scene (see `STORY.md` "Known gaps").

### Portraits (`data/portrait/`)

Installed: `alibaba_neutral`, `alibaba_worried`, `alibaba_grateful`, `alibaba_son_neutral`, `alibaba_wife_neutral`, `marianna_neutral`, `marianna_decisive`, `marianna_wary`, `marianna_talking`, `chief_thief_neutral`, `chief_thief_menacing`, `standard_thief_neutral`, `standard_thief_angry`, `qasim_neutral`, `qasim_angry`, `tailor_neutral`, `abdallah_neutral`, `narrator`.

**Missing**: `qasim_wife_*` portraits.

### Stage objects (`data/animation/sprite/object/`)

`donkey/`, `donkey_loaded/`, `gold_pile/`, `gold_heap/`, `gold_sack/` — each
has `<chapter>/0.png` (chapter `1` for now). Donkeys are scaled 1.5×
already (donkey: 984×675, donkey_loaded: 1094×750).

Also legacy: `bigtea`, `chair`, `dream-swirl1`, `moon-ring`, `sun-ring`.

## What's done vs. what's left

### Done
- M1, M2 fully wired: dialogue, character hide/show, bg cross-fade door
  animation, donkey place/delete, narrator narration during blackouts.
- M6, M7, M8 dialogue exists in `localisation/en/event.csv` and engine
  supports the A/B branching they need.
- JRPG dialogue box, choice popup, click-to-advance, narrator silhouette.

### Left
- **Home-and-discovery scene** (M2 → M3 gap, see `STORY.md`).
- M3, M4, M5, M6, M7, M8 events.csv files exist but are minimal — they
  reference dialogue that's already localised but the
  `character_pos.csv` / bg setup may still be Elden Ring legacy. Each
  one needs a pass to:
  - Set `character_pos.csv` to whichever characters speak in that mission.
  - Set the right opening bg in `event.csv` (or via `object_pos.csv`).
  - Add hide/show/blackout transitions between sub-scenes.
  - For M6/M7/M8, wire the `select:choice` popup with the right A/B labels.
- Music is **muted** for now per user request — the `"music"` event
  type still works but `current_music` is unset. To re-enable, drop a
  music file into `data/sound/music/<name>.ogg` and reference it via
  the `music` event with `Object` = the filename without extension.

## House conventions

- **No emojis** in dialogue, code, or commit messages.
- **No comments** in CSVs or code unless documenting a non-obvious
  invariant.
- **Don't rename** existing portraits or stage object folder names —
  events.csv refers to them by exact name (case-sensitive after the
  `filename_convert_readable` capitalisation: `donkey` → `Donkey`,
  `donkey_loaded` → `Donkey_loaded`).
- When you add a new portrait, drop it into `data/portrait/` and
  reference it in events without `.png`. The portrait loader picks up
  every `*.png` in that folder at battle init.

## Useful patterns (copy-paste)

### A normal dialogue line

```csv
"","m1/5","Thief","Default","","","voice:(Parchment_write;3000;0),portrait:standard_thief_neutral,side:right,speaker:Thief,wait,hold"
```

### A narrator line (any character can deliver — they just don't show)

```csv
"","m1/8","Thief","Default","","","voice:(Parchment_write;3000;0),portrait:narrator,side:left,speaker:Narrator,wait,hold"
```

### A bg cross-fade

```csv
"","","Forest_outside_cave_open","","bgchange","","scene:1,POS:1,fade"
"","","camera","wait","cutscene","","timer:0.6,wait"
```

### A blackout that holds (e.g., scene transition where you swap characters)

```csv
"","","camera","blackout","cutscene","","timer:1,wait,no auto fade out"
"","","CharacterA","","hide","",""
"","","CharacterB","","show","",""
"","","camera","blackout","cutscene","","timer:0.5,wait,instant fade,fade"
```

### A choice point (M6 example)

```csv
"","m6/4","Mariana","Default","","","voice:(...),portrait:marianna_decisive,side:left,speaker:Marjana,wait,hold,select:choice,choice_a:Burn the jars,choice_b:Bargain with the captain"
"","m6/A1","Mariana","Default","","yes","voice:(...),portrait:..."
"","m6/B1","Mariana","Default","","no","voice:(...),portrait:..."
```

### Place / delete a stage object

```csv
"","","Donkey_loaded","","place","","POS:(900;1600),Camera:1"
"","","Donkey_loaded","","delete","",""
```

## Where to look when something breaks

- "Donkey doesn't appear" — check the `Object` name capitalisation
  matches `data/animation/sprite/object/<lowercase>/`. Check POS isn't
  off-screen (world `0..3840`, screen-cropped to first panel).
- "Portrait is missing / black" — file must be in `data/portrait/`,
  spelled exactly as referenced. Lookup is case-insensitive at load
  but the matching key is the lowercased filename without extension.
- "Click doesn't advance" — the line probably doesn't have `wait` in
  its property. Without `wait`, the engine fires the next event
  immediately.
- "Character doesn't speak" — events with `Object="SomeChar"` need
  that character to exist in `character_pos.csv` and be `show`n at the
  time of the event. Hidden characters can still deliver narrator lines
  (we kept them `event_process`-active when hidden).

## When in doubt

The user iterates fast and prefers screenshots over long write-ups.
Make a small change, ask them to reload, adjust based on what they see.
Don't refactor surrounding code while fixing a content bug.
