"""P5 — integration tests: UI layer driving the real P1-P4 systems."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src.core.constants import WATER, FOREST, GRASSLAND
from src.ui.sim_clock import SimClock
from src.ui.game_world import GameWorld
from src.ui import controls


def test_clock_paused_produces_no_ticks():
    clock = SimClock()
    assert clock.update(5.0) == 0


def test_clock_speed_scales_ticks():
    clock = SimClock()
    clock.toggle_pause()
    clock.set_speed(4)
    assert clock.update(1.0) == 4


def test_world_generates_all_biomes():
    game = GameWorld(seed=42)
    stats = game.stats()
    assert stats["water %"] > 0
    assert stats["forest %"] > 0


def test_simulation_ticks_advance_year():
    game = GameWorld(seed=42)
    for _ in range(5):
        game.tick()
    assert game.year == 5


def test_preview_blocks_invalid_actions():
    game = GameWorld(seed=42)
    water = next(c for row in game.cells for c in row if c.biome == WATER)
    grass = next(c for row in game.cells for c in row if c.biome == GRASSLAND)
    assert controls.preview(game, controls.PLANT, water)[0] == "bad"
    assert controls.preview(game, controls.DEFOREST, grass)[0] == "bad"
    assert controls.preview(game, controls.SETTLE, water)[0] == "bad"


def test_plant_forest_changes_cell_and_records_history():
    game = GameWorld(seed=42)
    spot = next(c for row in game.cells for c in row
                if controls.preview(game, controls.PLANT, c)[0] in ("good", "risky"))
    ok, msg = controls.apply_tool(game, controls.PLANT, spot)
    assert ok
    assert spot.biome == FOREST
    events = game.events.get_all_events()
    assert any(e.event_type == "PLAYER_PLANTED_FOREST" for e in events)


def test_place_settlement_creates_real_settlement_ai():
    game = GameWorld(seed=42)
    spot = next(c for row in game.cells for c in row
                if controls.preview(game, controls.SETTLE, c)[0] in ("good", "risky"))
    ok, _ = controls.apply_tool(game, controls.SETTLE, spot)
    assert ok
    s = game.settlement_at(spot.x, spot.y)
    assert s is not None and s.population > 0    # P3's real Settlement
    game.tick()                                  # AI runs without crashing
    assert game.settlements


def test_tick_is_fast_enough_for_4x_speed():
    import time
    game = GameWorld(seed=42)
    t0 = time.time()
    for _ in range(4):
        game.tick()
    assert (time.time() - t0) < 1.0, "4 ticks must fit in one second (4x speed)"
