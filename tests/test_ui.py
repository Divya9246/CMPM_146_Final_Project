"""P5 — tests for the UI-side logic that doesn't need a window."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src.core.constants import FOREST, GRASSLAND, WATER
from src.ui.sim_clock import SimClock
from src.ui.mock_world import MockWorld
from src.ui import controls


def test_clock_paused_produces_no_ticks():
    clock = SimClock()
    assert clock.update(5.0) == 0


def test_clock_speed_scales_ticks():
    clock = SimClock()
    clock.toggle_pause()
    clock.set_speed(4)
    assert clock.update(1.0) == 4


def test_world_generates_and_ticks():
    world = MockWorld(seed=42)
    stats = world.stats()
    assert 0 < stats["water %"] < 100
    for _ in range(10):
        world.tick()
    assert world.year == 10


def test_same_seed_same_world():
    a, b = MockWorld(seed=7), MockWorld(seed=7)
    assert [c.biome for row in a.cells for c in row] == \
           [c.biome for row in b.cells for c in row]


def test_preview_blocks_invalid_actions():
    world = MockWorld(seed=42)
    water = next(c for row in world.cells for c in row if c.biome == WATER)
    grass = next(c for row in world.cells for c in row if c.biome == GRASSLAND)
    assert controls.preview(world, controls.PLANT, water)[0] == "bad"
    assert controls.preview(world, controls.DEFOREST, grass)[0] == "bad"
    assert controls.preview(world, controls.SETTLE, water)[0] == "bad"


def test_plant_forest_records_history():
    world = MockWorld(seed=42)
    grass = next(c for row in world.cells for c in row if c.biome == GRASSLAND)
    controls.apply_tool(controls.PLANT, grass)
    assert grass.biome == FOREST
    events = world.events.get_all_events()
    assert any(e.event_type == "PLAYER_PLANTED_FOREST" for e in events)
