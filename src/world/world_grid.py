# world_grid.py
# containers and Accessors for the world grid

from src.core.world_types import Cell
from src.core.constants import WORLD_WIDTH, WORLD_HEIGHT


class World:
	def __init__(self, seed=None):
		self.width = WORLD_WIDTH
		self.height = WORLD_HEIGHT
		self.seed = seed
		self.year = 0

		self.grid = []
		self._init_empty_grid()

	def _init_empty_grid(self):
		self.grid = []
		for y in range(self.height):
			row = []
			for x in range(self.width):
				row.append(Cell(x, y))
			self.grid.append(row)

	def get_cell(self, x, y):
		if 0 <= x < self.width and 0 <= y < self.height:
			return self.grid[y][x]
		return None

	def get_neighbors(self, x, y):
		neighbors = []
		for dx in (-1, 0, 1):
			for dy in (-1, 0, 1):
				if dx == 0 and dy == 0:
					continue
				nx, ny = x + dx, y + dy
				cell = self.get_cell(nx, ny)
				if cell is not None:
					neighbors.append(cell)
		return neighbors

	def get_cells_in_radius(self, x, y, radius):
		cells = []
		for dy in range(-radius, radius + 1):
			for dx in range(-radius, radius + 1):
				cell = self.get_cell(x + dx, y + dy)
				if cell is not None:
					cells.append(cell)
		return cells

	def get_all_cells(self):
		for row in self.grid:
			for cell in row:
				yield cell

    # Count the number of cells for each biome type
	def count_biomes(self):
		counts = {}
		for cell in self.get_all_cells():
			counts[cell.biome] = counts.get(cell.biome, 0) + 1
		return counts
 
	def to_dict(self):
		return {
			"seed": self.seed,
			"year": self.year,
			"width": self.width,
			"height": self.height,
			"biome_counts": self.count_biomes(),
		}
 
	def __repr__(self):
		counts = self.count_biomes()
		return f"World(seed={self.seed}, year={self.year}, biomes={counts})"