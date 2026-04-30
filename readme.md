# 1001 Nights — Ali Baba (Marjana POV)

A visual-novel adaptation of *Ali Baba and the Forty Thieves* from
*One Thousand and One Nights*, retold from **Marjana's** point of view.

She's the slave-girl who normally gets two paragraphs in the original
tale before saving the entire household. Here she's the narrator, the
investigator, and the one making the hard calls. Ali Baba is her
well-meaning but anxious master whose decisions she keeps having to
clean up.

Built on top of the
[Royal-Animation](https://github.com/remance/Royal-Animation) Pygame
engine (originally an Elden Ring fan-animation tool by **remance**),
heavily modified into a JRPG-style dialogue system with portraits,
click-to-advance, branching choices, and watercolor backgrounds.

## Quick start

```sh
git clone https://github.com/PhucNguyen-rsc/1001_nights_final_project.git
cd 1001_nights_final_project
python3 -m venv .venv && source .venv/bin/activate
pip install pygame-ce pyperclip screeninfo Pillow
python main.py
```

Full setup notes (Windows instructions, common errors): see
[INSTALL.md](INSTALL.md).

> Don't `pip install -r requirements.txt` — it's the upstream file and
> pins Windows-only / Python-3.13-only packages that break on most
> systems. The four packages above are all you need.

## Story

8 missions, ~30 minutes of playthrough. Linear at the mission level,
branches A/B at three points (M6, M7, M8) — the choices change *how*
Marjana acts, not what happens next.

Full plot, mission breakdown, cast, and tone notes:
[STORY.md](STORY.md).

## Status

| Mission | Done? | Notes |
|---|---|---|
| M1 — Forest, the rock | ✓ playable | thieves arrive with empty donkeys, leave with loaded ones, M+A go in |
| M2 — Inside cave, exit | ✓ playable | take the gold, "Shut Sesame," walk home with loaded donkeys |
| M3 — Confession | partial | opens mid-conversation; the home-discovery scene is **missing** (see STORY.md "Known gaps") |
| M4 — Qasim is dead | dialogue done | events.csv needs a content pass |
| M5 — Funeral, the cobbler | dialogue done | events.csv needs a content pass |
| M6 — Forty thieves in oil jars | dialogue done, branching A/B/C | wiring in progress |
| M7 — Khawaja Husain dinner | dialogue done, branching A/B/C | wiring in progress |
| M8 — Ending | dialogue done, branching A/B/C | wiring in progress |

## For developers

If you're picking up the project (human or AI agent), start with
[AGENT_BRIEFING.md](AGENT_BRIEFING.md) — it covers the engine
architecture, CSV event format, world-coordinate system, asset layout,
copy-paste patterns for adding scenes, and a debugging cheatsheet.

The simplest real example of how a mission is wired is
[`data/map/preset/1/1/1/event.csv`](data/map/preset/1/1/1/event.csv) — read that file
top to bottom and you'll understand 80% of how everything works.

## Project layout

```
data/
  map/preset/1/<mission>/1/    mission scripts (event.csv, character_pos.csv)
  map/scene/1/                 background images
  portrait/                    JRPG dialog portraits
  animation/sprite/object/     stage objects (donkeys, gold sacks)
  animation/sprite/character/  character body sprites
  localisation/en/event.csv    all dialogue text
  character/character.csv      character roster
engine/
  battle/                      mission runtime + cutscene event interpreter
  character/                   character sprite + speech routing
  uibattle/                    JRPG dialog box, choice popup
  scene/                       background panels with cross-fade
  stageobject/                 non-character world objects
main.py                        entry point
```

## Credits

- **Engine:** [Royal-Animation](https://github.com/remance/Royal-Animation) by **remance** (MIT-style; see [LICENSE](LICENSE))
- **Adaptation, story, asset wiring:** PhucNguyen-rsc and collaborators
- **Backgrounds + portraits:** generated via Gemini, retouched and assembled by us

### Sound (inherited from upstream Royal-Animation)

- Weapon sound "Wooshes" by lebaston100 (https://freesound.org/people/lebaston100/)
- Various weapon sounds from Videvo (https://www.videvo.net/) and Audionautics (https://freesound.org/people/Audionautics/)
- "Battle horn 1" by kirmm (https://pixabay.com/sound-effects/battle-horn-1-6931/)
- "Mechanism" by Globofonia (https://freesound.org/people/Globofonia/)
- Various effect sounds by Pixabay (https://pixabay.com/users/pixabay-1/), UNIVERSFIELD (https://pixabay.com/users/universfield-28281460/), Alex_Jauk (https://pixabay.com/users/alex_jauk-16800354/), LordSonny (https://pixabay.com/users/lordsonny-38439655/)
- Ice sounds by danielsoundsgood (https://linktr.ee/danielsoundsgood)
- Grass walk by joentnt (https://pixabay.com/users/joentnt-47713256/)
- Music: *Blue Dream* and *White Dream* by BorealMix (https://www.mikseri.net/borealmix/)
- Forest/wind ambient by Pixabay; rain by lebaston100

(Music is muted by default in this build — set in the engine; see
`AGENT_BRIEFING.md` to re-enable.)

## License

The original Royal-Animation engine is under the upstream
[LICENSE](LICENSE) — keep that intact. Story content (dialogue,
narrative structure) and our adaptation work are released under the
same terms unless noted otherwise.
