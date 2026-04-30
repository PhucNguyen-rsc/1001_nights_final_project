# Story — Ali Baba and the Forty Thieves (Mariana POV)

A visual-novel adaptation of "Ali Baba and the Forty Thieves," retold from
**Marjana's** perspective (spelled `Mariana` in some asset names — same
character). Mariana is the clever, observant one; Ali Baba is the
well-meaning but anxious partner whose decisions she has to repeatedly
clean up after.

The narrative is linear at the mission level but branches at three
points (M6, M7, M8) via A/B choices that change *how* Mariana acts, not
which mission plays.

## Cast

- **Mariana (Marjana)** — POV character. Cool-headed, decisive. Speaks from the **left** in dialogues.
- **Ali Baba** — Mariana's master; later treats her as family. Speaks from the right.
- **Qasim** — Ali Baba's wealthier, greedier brother. Dies in the cave (off-screen, M3→M4 transition).
- **Qasim's wife** — Discovers the gold via the borrowed scale. (Currently MISSING from playable scenes — see "Known gaps" below.)
- **Captain of the Forty Thieves** — main antagonist. Returns disguised as "Khawaja Husain" in M7.
- **Standard Thief** — generic thief, used for "second voice" in the band.
- **Ali Baba's wife / son** — appear in later missions (M7, M8).
- **Tailor / Baba Mustafa** — old man Mariana pays to stitch Qasim's body in M5.
- **Narrator** — disembodied voice for scene-setting prose, drawn as a hooded silhouette portrait.

Portrait files in `data/portrait/` (one PNG per emotion variant). Naming: `<character>_<emotion>.png`.

## Mission breakdown

Dialogue text lives in `data/localisation/en/event.csv` keyed by `mX/n`. Each mission's events live in `data/map/preset/1/<mission>/1/event.csv`.

### M1 — Forest, the rock (DONE, playable)
- Mariana + Ali Baba gathering wood, hide as forty thieves arrive.
- Phase B: thieves arrive with **2 empty donkeys** (left side of road), Captain says "Open, Sesame," cave door opens, they go in.
- Phase C blackout: thieves emerge with **2 loaded donkeys** (gold), "Shut, Sesame," they ride off.
- Phase D: M+A return, debate, Mariana insists on going in too. "Open, Sesame" → blackout → M2.
- Backgrounds: `forest_outside_cave.png` → `forest_outside_cave_half_open.png` → `forest_outside_cave_open.png` (cross-fade, no black flash).

### M2 — Inside cave, exit (DONE, playable)
- Brief dialogue inside cave (bg = `cave.png`).
- Door opens (cross-fade) → outside. **2 loaded donkeys** appear with M+A.
- "Shut, Sesame" → cave closes. They start walking home.
- Setup line: "your wife will notice. We should have a story ready."

### M3 — Confession, Qasim knows (PARTIAL — starts mid-conversation)
- Currently OPENS with: "He knows, Marjana. He found the coin."
- Ali Baba reveals he told Qasim everything, including the password. Mariana realizes Qasim will go alone.
- **Missing**: the actual scene where Qasim discovers the gold (borrowed scale, stuck coin) and confronts Ali Baba. See "Known gaps."

### M4 — Qasim is dead (DONE, dialogue only)
- Ali Baba grieves; Mariana takes charge of covering it up so the thieves don't know they have a leak.

### M5 — Funeral, the cobbler/tailor (DONE, dialogue only)
- Mariana pays an old man (blindfolded) to stitch Qasim's body so it looks like he died of fever.
- 3 days of mourning; neighbours believe the cover story.
- Mariana: "We're not done yet. The thieves will come back."

### M6 — Forty thieves in oil jars (DONE, branching A/B/C)
- Captain returns disguised as oil merchant with 38 jars. 37 jars hide men, 1 holds real oil.
- Mariana investigates the courtyard, realizes the trap.
- **Choice A**: Burn them — soak hay in real oil, set the jars on fire. Captain escapes through window.
- **Choice B**: Betray Ali Baba — go to the captain, demand a cut. Captain kills them all.
- **Choice C**: Confront her master directly with the truth. They handle it together.
- (Each branch's dialogue is `m6/A1..A7`, `m6/B1..B7`, `m6/C1..C6`.)

### M7 — Khawaja Husain (the dinner) (DONE, branching A/B/C)
- Captain returns disguised as a wealthy cloth merchant who befriends Ali Baba's son.
- Invited to dinner; refuses salt (won't share bread with someone he'll kill).
- Mariana dances, then strikes during the dance. Ali Baba: "WHAT HAVE YOU DONE?!"
- **Choice A**: Show him the dagger under the robe.
- **Choice B**: "I didn't kill your guest. I killed the man who murdered your brother."
- **Choice C**: Identify him — "It's him. The oil merchant. The captain."

### M8 — Ending (DONE, branching A/B/C)
- Ali Baba offers Mariana to marry his son and inherit the cave's secret.
- **Choice A**: Accept, "because this is home."
- **Choice B**: "I was already family. I have been since the forest. But yes."
- **Choice C**: Smiling close — Ali Baba looks like the man Mariana met on the forest road. The door is shut. The house is safe.

## Known gaps

- **Home-and-discovery scene is missing** between M2 and M3.
  Needed beats: Ali Baba returns home → distributes/measures gold →
  Qasim's wife borrows the scale → coin sticks to scale →
  Qasim confronts Ali Baba.
  Currently M3 jumps straight to Ali Baba telling Mariana that Qasim
  *already* knows. Either insert as new mission (renumber M3..M8 → M4..M9)
  or prepend to M3.
- **Qasim's wife** has no portrait yet. Need `qasim_wife_*.png`.
- **Ali Baba's house interior** has no background yet. Need
  `alibaba_house_interior.png` (existing `alibaba_house.png` is the exterior).

## Tone & style

- Mariana's voice: spare, observational, slightly clipped. She narrates as the Narrator portrait when monologuing.
- Ali Baba's voice: warmer, more apologetic, rambles when worried.
- Captain: blunt, threatening; menacing portrait used for orders, neutral for "merchant disguise" lines.
- Narrator portrait: a black-hood silhouette — used for any third-person prose ("An hour passes. The forest holds its breath.").

## Branching mechanics

Choice missions (M6, M7, M8) use the engine's `select:choice` event property
with `choice_a` / `choice_b` labels. Branch lines are gated by `Trigger="yes"`
or `Trigger="no"` — when the player picks A, all `no`-trigger events are
removed from the queue (and vice versa). See `engine/battle/cutscene_player_input.py`.

Each mission can offer **2** branches (A vs. B). The third "C" texts in
the localisation are *narrator post-summaries* that play regardless of
choice — they tie the branches back into a single thread for the next mission.
