# Integration Notes (P5 — Winston)

The full game now runs: `python3 main.py` (after `pip3 install -r requirements.txt`).
P1's terrain, P2's climate/biomes, P3's settlement AI, and P4's player tools +
history are all connected through the UI in `src/ui/`. `src/ui/game_world.py`
is the single integration point — the UI only talks to that class.

## Controls

Space = play/pause · 1/2/3 = 1x/2x/4x speed · F/D/S = tools · click map to
select/act · H = history · R = new world · Esc = disarm tool.

## Changes I made INSIDE teammates' modules (please review, owners!)

1. **src/simulation/climate.py** (P2) — `proximity_to_water` scanned every
   cell for every cell (~1.2 s per simulated year; the game needs 4 ticks/sec
   at 4x). Replaced with a per-year multi-source BFS distance field. Same
   signature and 0..1 falloff; grid distance instead of exact euclidean.
   Original kept as `_original_proximity_to_water` for comparison.
2. **src/simulation/biome_simulation.py** (P2) — DESERT_SPREAD fired almost
   every year (any +1 desert cell), flooding history. Now fires when desert
   grows by ≥5 cells in a year. Also: heat_wave now emits `DROUGHT_STARTED`
   and heavy_rain emits `HEAVY_RAIN_STARTED` so those show in history/UI
   instead of only printing to the console.
3. **src/history/event_manager.py** (P4) — added `HEAVY_RAIN_STARTED` to
   LISTEN_TO (one line).

## Bugs spotted but NOT fixed (owner's call)

* **P2, climate.py `calculate_temperature`**: `normalized_height = height /
  WORLD_HEIGHT` divides terrain height (0–100) by the grid dimension (50),
  so any cell above height 50 gets base temperature 0 — high ground reads as
  0° in the UI. Probably want `height / 100.0`. Gameplay still works (cold
  mountains), so I left the behavior alone.
* **src/ui/mock_world.py** is my old Sprint-1 mock; nothing imports it now.
  It can be deleted whenever.

## Renderer decision

The UI is pygame (2D grid, height-shaded). P1's Ursina 3D renderer
(`src/world/biome_renderer.py`) is untouched and still available if we decide
to switch views — everything except `src/ui/map_view.py` and the panels is
renderer-agnostic. `ursina` stays in requirements.txt for that reason.

## Demo chain (verified working, seed 42)

Place settlement → it grows → heat wave hits (~year 21) → land dries →
settlement declines → migrates to better land → all of it readable in the
History panel. `tests/test_ui.py` runs the whole loop headless (39 tests).
