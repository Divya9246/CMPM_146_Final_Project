import math
import numpy as np
from opensimplex import OpenSimplex

from src.core.constants import NOISE_OCTAVES, NOISE_PERSISTENCE

# Generate a 2D noise layer using Opensimplex
def noise_layer(width, height, seed, scale):
	gen = OpenSimplex(seed=seed)
	grid = np.zeros((height, width))

	for y in range(height):
		for x in range(width):
			val = 0.0
			amplitude = 1.0
			freq = scale
			max_amp = 0.0
			for _ in range(NOISE_OCTAVES):
				val += gen.noise2(x * freq, y * freq) * amplitude
				max_amp += amplitude
				amplitude *= NOISE_PERSISTENCE
				freq *= 2.0
			grid[y][x] = val / max_amp

	min_val = grid.min()
	max_val = grid.max()
	if max_val - min_val > 0:
		grid = (grid - min_val) / (max_val - min_val)
	return grid


def island_mask(width, height, strength):
	mask = np.zeros((height, width))
	cx, cy = width / 2.0, height / 2.0
	for y in range(height):
		for x in range(width):
			dx = (x - cx) / cx
			dy = (y - cy) / cy
			dist = math.sqrt(dx * dx + dy * dy)
			mask[y][x] = max(0.0, 1.0 - dist ** strength)
	return mask