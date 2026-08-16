"""
Terrain Generator - Procedural generation of Terrain Layers

"""

from src.world.noise_generator import noise_layer, island_mask
from src.core.constants import (
	NOISE_SCALE_HEIGHT, NOISE_SCALE_MOISTURE, NOISE_SCALE_PRECIPITATION,
	ISLAND_MASK_ENABLED, ISLAND_MASK_STRENGTH,
	WATER_HEIGHT, DESERT_MOISTURE_MAX, FOREST_MOISTURE_MIN,
	TEMP_BASE, TEMP_HEIGHT_PENALTY, TEMP_LATITUDE_FACTOR,
)


def generate_heightmap(width, height, seed):
	"""generate the elevation layer. returns numpy array 0.0 - 1.0."""
	grid = noise_layer(width, height, seed, NOISE_SCALE_HEIGHT)
	if ISLAND_MASK_ENABLED:
		mask = island_mask(width, height, ISLAND_MASK_STRENGTH)
		grid = grid * 0.6 + grid * mask * 0.4
		min_val = grid.min()
		max_val = grid.max()
		if max_val - min_val > 0:
			grid = (grid - min_val) / (max_val - min_val)
	return grid


def generate_moisture(width, height, seed):
	return noise_layer(width, height, seed + 1000, NOISE_SCALE_MOISTURE)


def generate_precipitation(width, height, seed):
	return noise_layer(width, height, seed + 2000, NOISE_SCALE_PRECIPITATION)


def compute_temperature(height_val, y_pos, grid_height):
	latitude_factor = 1.0 - (y_pos / grid_height) * TEMP_LATITUDE_FACTOR
	temp = (TEMP_BASE - height_val * TEMP_HEIGHT_PENALTY) * latitude_factor
	return max(0.0, min(1.0, temp))


def assign_biome(height_val, moisture_val):
	if height_val < WATER_HEIGHT:
		return "water"
	if moisture_val > FOREST_MOISTURE_MIN:
		return "forest"
	if moisture_val < DESERT_MOISTURE_MAX:
		return "desert"
	return "grassland"


def generate_world(world, seed):
	world.seed = seed
	world.year = 0

	w = world.width
	h = world.height

    # Three main layers
	heights = generate_heightmap(w, h, seed)
	moistures = generate_moisture(w, h, seed)
	precips = generate_precipitation(w, h, seed)

    # Module to assign biome and compute food for each cell
	for cell in world.get_all_cells():
		x, y = cell.x, cell.y
		cell.height = float(heights[y][x])
		cell.moisture = float(moistures[y][x])
		cell.precipitation = float(precips[y][x])
		cell.temperature = compute_temperature(cell.height, y, h)
		cell.biome = assign_biome(cell.height, cell.moisture)
		cell.compute_food()