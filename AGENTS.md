# AGENT Instructions for `galaga`

This file describes the project, its goals, and a task checklist for contributors.

## Project Overview

This repository contains a simple clone of the **Galaga** arcade game written in
Python. The main script [`galaga.py`](galaga.py) uses the `pygame` library to
render sprites supplied in the `space_starter_kit` directory. The game opens a
window at 800x600 pixels, displays a player starship, lets the player move left
and right, shoot bullets, and provides a single row of enemies that move back
and forth. Collisions remove enemies when hit by bullets. The README explains
how to run the game using `python3 galaga.py`.

The intent of this project is to progressively build a more complete Galaga
experience while remaining lightweight and easy to run on most systems. The
code currently provides a minimal working prototype and can be extended with
additional features such as scoring, multiple waves, sound, and UI screens.

## Guiding Principles

* **No frameworks or additional libraries** should be introduced unless the
  user explicitly requests them. If another module or approach might be useful,
  feel free to mention it in discussion, but do not add it to the project on
your own.
* Keep the repository self-contained. Remember that this environment will not
  have network access once setup is complete, so any dependencies must already
  be present in the repo or be part of the Python standard library (except for
  the `pygame` dependency used by the existing code).
* Use this checklist to track progress. Check off items that have been
  implemented by editing this file in future pull requests.

## Development Checklist

### Stage 1 – Initial Setup

- [x] Establish Python project with `galaga.py` using `pygame`.
- [x] Include sprite assets in `space_starter_kit`.
- [ ] Document setup steps for installing dependencies.

### Stage 2 – Basic Gameplay (current state)

- [x] Display game window (800x600) titled "Galaga".
- [x] Player ship moves horizontally with arrow keys.
- [x] Fire bullets with space bar.
- [x] Row of enemy UFO sprites moves horizontally and descends when reaching
      screen edges.
- [x] Collision detection removes enemies when hit by bullets.

### Stage 3 – Core Game Features

- [ ] Implement score tracking and on‑screen display.
- [x] Track player lives and end the game when lives reach zero.
- [ ] Introduce multiple waves or levels of enemies.
- [ ] Add increasing difficulty and varied enemy behaviors.

### Stage 4 – Polish and Quality of Life

- [ ] Intro/menu screen and game over screen.
- [ ] Sound effects and/or background music (using `pygame` audio APIs only,
      unless the user specifies otherwise).
- [ ] Visual enhancements (animations, additional sprites, backgrounds).
- [ ] Packaging or distribution instructions.

## How to Run

```bash
python3 galaga.py
```

Running the command above should launch the game window if `pygame` is
installed. If you encounter import errors, ensure that `pygame` is available in
your Python environment.

