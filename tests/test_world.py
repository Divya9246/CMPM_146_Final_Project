# Tests for world generation and grid functionality

# Failure is inevitable due to the randomness of procedural generation

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.world.world_grid import World
from src.world.terrain_generator import generate_world
from src.core.world_types import Cell
from src.core.constants import WORLD_WIDTH, WORLD_HEIGHT, BIOME_TYPES


def test_grid_dimensions():
	w = World()
	assert w.width == WORLD_WIDTH and w.height == WORLD_HEIGHT
	assert sum(1 for _ in w.get_all_cells()) == WORLD_WIDTH * WORLD_HEIGHT

def test_get_cell_bounds():
	w = World()
	assert w.get_cell(0, 0) is not None
	assert w.get_cell(WORLD_WIDTH - 1, WORLD_HEIGHT - 1) is not None
	assert w.get_cell(-1, 0) is None
	assert w.get_cell(WORLD_WIDTH, WORLD_HEIGHT) is None

def test_neighbors_count():
	w = World()
	assert len(w.get_neighbors(0, 0)) == 3
	assert len(w.get_neighbors(5, 0)) == 5
	assert len(w.get_neighbors(5, 5)) == 8

def test_radius():
	w = World()
	mid = WORLD_WIDTH // 2
	assert len(w.get_cells_in_radius(mid, mid, 2)) == 25

def test_generation_fills_all_cells():
	w = World()
	generate_world(w, seed=42)
	for cell in w.get_all_cells():
		assert 0.0 <= cell.height <= 100.0
		assert 0.0 <= cell.temperature <= 100.0
		assert 0.0 <= cell.moisture <= 100.0
		assert cell.biome in BIOME_TYPES

def test_reproducibility():
	w1 = World()
	generate_world(w1, seed=42)
	w2 = World()
	generate_world(w2, seed=42)
	for c1, c2 in zip(w1.get_all_cells(), w2.get_all_cells()):
		assert c1.height == c2.height and c1.biome == c2.biome

def test_all_biomes_present():
	w = World()
	generate_world(w, seed=42)
	counts = w.count_biomes()
	for b in BIOME_TYPES:
		assert counts.get(b, 0) > 0, f"{b} missing"

def test_water_zero_food():
	w = World()
	generate_world(w, seed=42)
	for c in w.get_all_cells():
		if c.biome == "water":
			assert c.food == 0.0

def test_high_elevation_cold():
	w = World()
	generate_world(w, seed=42)
	high = [c for c in w.get_all_cells() if c.height > 70]
	low = [c for c in w.get_all_cells() if 30 < c.height < 50]
	if high and low:
		avg_high = sum(c.temperature for c in high) / len(high)
		avg_low = sum(c.temperature for c in low) / len(low)
		assert avg_high < avg_low

def test_cell_to_dict():
	c = Cell(5, 10)
	c.height = 50.0
	c.biome = "forest"
	d = c.to_dict()
	assert d["x"] == 5 and d["biome"] == "forest" and "food" in d

def test_world_to_dict():
	w = World()
	generate_world(w, seed=42)
	d = w.to_dict()
	assert d["seed"] == 42 and "biome_counts" in d


if __name__ == "__main__":
	tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
	passed = 0
	for t in tests:
		try:
			t()
			print(f"  [PASS] {t.__name__}")
			passed += 1
		except Exception as e:
			print(f"  [FAIL] {t.__name__}: {e}")
	print(f"\n{passed}/{len(tests)} passed")