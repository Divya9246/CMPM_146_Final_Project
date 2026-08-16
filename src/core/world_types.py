# world_types.py - data model for a single grid cell

# every cell in the world grid is one of these

from src.core.constants import WATER

class Cell:
	def __init__(self, x, y):
		# Initial grid position
		self.x = x
		self.y = y

		# terrain properties: derived from noise functions
		self.height = 0.0         
		self.temperature = 0.0   
		self.moisture = 0.0        
		self.precipitation = 0.0   

		self.biome = "grassland"

		self.food = 0.0

		self.settlement = None

		self.entity = None

	def compute_food(self):
		"""
		Recalculation of food is required from current bioclimatic values.
		food is high when all conditions are met:mid elevation, decent rainfall, warm, moist.
		
		Initial Assumption: water and desert cells produce very little food."""
		
		from src.core.constants import (FOOD_PRECIP_WEIGHT, FOOD_MOISTURE_WEIGHT,
			FOOD_TEMP_WEIGHT, FOOD_HEIGHT_WEIGHT, FOOD_OPTIMAL_HEIGHT)

		if self.biome == WATER:
			self.food = 0.0
			return self.food

		# TEST REQUIRED -- FLAGGED not sure if this is correct
		height_score = 100.0 - abs(self.height - FOOD_OPTIMAL_HEIGHT) * 2.0
		height_score = max(0.0, min(100.0, height_score))

		self.food = (
			self.precipitation * FOOD_PRECIP_WEIGHT +
			self.moisture * FOOD_MOISTURE_WEIGHT +
			self.temperature * FOOD_TEMP_WEIGHT +
			height_score * FOOD_HEIGHT_WEIGHT
		)
		self.food = max(0.0, min(100.0, self.food))
		return self.food

	def to_dict(self):
		# return a dictionary representation of the cell for serialization - Assigned to Divya
		return {
			"x": self.x,
			"y": self.y,
			"height": round(self.height, 1),
			"temperature": round(self.temperature, 1),
			"moisture": round(self.moisture, 1),
			"precipitation": round(self.precipitation, 1),
			"biome": self.biome,
			"food": round(self.food, 1),
			"has_settlement": self.settlement is not None,
		}

	def __repr__(self):
		return f"Cell({self.x},{self.y} h={self.height:.1f} b={self.biome})"