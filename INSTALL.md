# Install

## Prerequisites

- **Python 3.10+** (we develop on 3.14, but 3.10–3.13 work too).
  Check with `python3 --version`.
- **git** for cloning.
- ~500 MB free disk space (the asset folders are heavy).

## 1. Clone the repo

```sh
git clone <repo-url>
cd Royal-Animation
```

## 2. Create a virtualenv

**macOS / Linux:**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your prompt.

## 3. Install dependencies

> **Don't** run `pip install -r requirements.txt` blindly. It pins
> `pywin32~=310` which is Windows-only and will fail on macOS/Linux,
> and it pins plain `pygame` which is broken on Python 3.14
> (no `pygame.mixer`).

Install only what we actually need:

```sh
pip install pygame-ce pyperclip screeninfo Pillow
```

`pygame-ce` (community edition) is a drop-in replacement for `pygame`
and ships a working mixer on Python 3.14. If you previously installed
plain `pygame`, uninstall it first:

```sh
pip uninstall pygame
pip install pygame-ce
```

## 4. Run the game

From the repo root, with the venv active:

```sh
python main.py
```

The game opens in a new window. Press `Esc` to quit.

## 5. Verify your install

The intro should drop you straight into **Mission 1** (forest scene
with Mariana and Ali Baba). If you see the JRPG dialog box at the
bottom with portraits, click-to-advance works, and you can reach
Mission 2 — your install is fine.

## Common problems

### `ModuleNotFoundError: No module named 'pygame.mixer'`

You're on Python 3.14 (or some other newer build) with vanilla pygame.
Switch to `pygame-ce`:

```sh
pip uninstall pygame
pip install pygame-ce
```

### `Could not find a version that satisfies the requirement pywin32~=310`

You're on macOS/Linux running `pip install -r requirements.txt`. Skip
that file — install dependencies manually as in step 3.

### `KeyError: 'p1_head'` or `KeyError: <some character name>`

Stale character config. Make sure you're on the latest commit and the
expected portraits are in `data/portrait/`. See `AGENT_BRIEFING.md`
for the full asset list.

### Black screen / no portraits

Portrait loader runs at battle init from `data/portrait/`. If you
moved or renamed portraits, the dialog box falls back to nothing.
Re-check filenames are lowercase + `.png` extension.

### The window opens but nothing happens

Click the window once to give it focus, then click again to advance
the dialog. If clicks don't register, check that `Space` or `Enter`
work — those are also bound to "advance dialog."

## Where to go next

- `STORY.md` — what the game is about, mission structure, cast.
- `AGENT_BRIEFING.md` — engine architecture, CSV format, copy-paste
  patterns for adding scenes, debugging cheatsheet.
- `data/map/preset/1/1/1/event.csv` — the simplest real example of how
  a mission is wired.
