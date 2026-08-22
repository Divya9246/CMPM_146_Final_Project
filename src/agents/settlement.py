# settlement state + AI behavior
#
# every year the behavior tree decides what happens:
#   sense environment -> track crisis -> pick ONE of grow / decline / hold steady
# migration and collapse cleanup happen in settlement_manager since they
# need to search the world / rewire cell.settlement
#
# events only fire on state CHANGES so history doesnt get spammed

from src.core.constants import WATER
from src.core.event_bus import event_bus
from src.agents.behavior_tree import Sequence, Selector, Condition, Action
from src.agents import agent_actions as act
from src.agents.agent_constants import (
	SETTLEMENT_RADIUS, WATER_ADJACENCY_BONUS,
	STARTING_POPULATION, MIN_POPULATION,
	GOOD_FOOD, GOOD_WATER, BAD_FOOD, BAD_WATER,
	CRITICAL_FOOD, CRITICAL_WATER,
	MIGRATION_PATIENCE,
	STATE_GROWING, STATE_STABLE, STATE_DECLINING, STATE_COLLAPSED,
	SETTLEMENT_GREW, SETTLEMENT_DECLINED, SETTLEMENT_COLLAPSED,
)

_next_id = 1


def _make_name():
	global _next_id
	name = f"Settlement {_next_id}"
	_next_id += 1
	return name


def build_settlement_tree():
	return Sequence(
		Action(act.sense_environment),
		Action(act.track_crisis),
		Selector(
			Sequence(Condition(act.is_thriving), Action(act.grow)),
			Sequence(Condition(act.is_struggling), Action(act.decline)),
			Action(act.hold_steady),
		),
	)


class Settlement:
	def __init__(self, x, y, name=None, population=STARTING_POPULATION):
		self.x = x
		self.y = y
		self.name = name if name is not None else _make_name()
		self.population = population

		self.food_supply = 0.0
		self.water_supply = 0.0

		self.state = STATE_STABLE
		self.critical_years = 0
		self.alive = True

		self.tree = build_settlement_tree()

	def assess_environment(self, world):
		# read food/water from nearby cells
		cells = world.get_cells_in_radius(self.x, self.y, SETTLEMENT_RADIUS)

		# simulate_year doesnt recompute food yet, so refresh it ourselves,
		# otherwise we'd be reading generation-time food forever
		for c in cells:
			c.compute_food()

		land = [c for c in cells if c.biome != WATER]
		has_water_tile = any(c.biome == WATER for c in cells)

		if land:
			self.food_supply = sum(c.food for c in land) / len(land)
			avg_moisture = sum(c.moisture for c in land) / len(land)
		else:
			self.food_supply = 0.0
			avg_moisture = 0.0

		self.water_supply = avg_moisture
		if has_water_tile:
			self.water_supply = min(100.0, self.water_supply + WATER_ADJACENCY_BONUS)

		return self.food_supply, self.water_supply

	def site_score(self):
		# one number for "how good is it here", used to compare migration targets
		return self.food_supply * 0.6 + self.water_supply * 0.4

	def conditions_good(self):
		return self.food_supply >= GOOD_FOOD and self.water_supply >= GOOD_WATER

	def conditions_bad(self):
		return self.food_supply < BAD_FOOD or self.water_supply < BAD_WATER

	def conditions_critical(self):
		return self.food_supply < CRITICAL_FOOD or self.water_supply < CRITICAL_WATER

	def wants_to_migrate(self):
		return self.critical_years >= MIGRATION_PATIENCE

	def update(self, world):
		# one year of settlement life
		if not self.alive:
			return self.state

		self.tree.tick({"settlement": self, "world": world})

		# collapse overrides whatever the tree decided
		if self.population < MIN_POPULATION:
			self._transition(world, STATE_COLLAPSED)

		return self.state

	def _transition(self, world, new_state):
		# only emit when the state actually changes
		if new_state == self.state:
			return

		old_state = self.state
		self.state = new_state

		data = self.event_data(world)
		data["previous_state"] = old_state

		if new_state == STATE_GROWING:
			data["cause"] = "abundant food and water"
			data["description"] = (
				f"{self.name} flourished and grew to {self.population} people "
				f"at ({self.x}, {self.y})."
			)
			event_bus.emit(SETTLEMENT_GREW, data)
		elif new_state == STATE_DECLINING:
			data["cause"] = self._scarcity_cause()
			data["description"] = f"{self.name} began to decline because {data['cause']}."
			event_bus.emit(SETTLEMENT_DECLINED, data)
		elif new_state == STATE_COLLAPSED:
			self.alive = False
			data["cause"] = self._scarcity_cause()
			data["description"] = (
				f"{self.name} collapsed at ({self.x}, {self.y}) because {data['cause']}."
			)
			event_bus.emit(SETTLEMENT_COLLAPSED, data)
		# going back to stable emits nothing

	def _scarcity_cause(self):
		food_bad = self.food_supply < BAD_FOOD
		water_bad = self.water_supply < BAD_WATER
		if food_bad and water_bad:
			return "of food and water shortages"
		if water_bad:
			return "the land dried out"
		return "of food shortages"

	def event_data(self, world):
		# includes location + description because thats what divya's EventManager reads
		return {
			"year": world.year,
			"x": self.x,
			"y": self.y,
			"location": (self.x, self.y),
			"settlement": self.name,
			"population": self.population,
			"state": self.state,
		}

	def to_dict(self):
		return {
			"name": self.name,
			"x": self.x,
			"y": self.y,
			"population": self.population,
			"state": self.state,
			"food_supply": round(self.food_supply, 1),
			"water_supply": round(self.water_supply, 1),
		}

	def __repr__(self):
		return f"Settlement({self.name} @({self.x},{self.y}) pop={self.population} {self.state})"