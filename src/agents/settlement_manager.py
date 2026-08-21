# owns the list of settlements, runs them each year, handles migration

from src.core.constants import WATER
from src.core.event_bus import event_bus
from src.agents.settlement import Settlement
from src.agents.agent_constants import (
	MIGRATION_SEARCH_RADIUS, MIGRATION_MIN_IMPROVEMENT,
	SETTLEMENT_RADIUS, WATER_ADJACENCY_BONUS,
	STATE_STABLE, STATE_COLLAPSED,
	SETTLEMENT_CREATED, SETTLEMENT_MIGRATED,
)


def _score_location(world, x, y):
	# score a candidate cell the same way a settlement scores its home
	cells = world.get_cells_in_radius(x, y, SETTLEMENT_RADIUS)
	land = [c for c in cells if c.biome != WATER]
	if not land:
		return 0.0
	food = sum(c.food for c in land) / len(land)
	water = sum(c.moisture for c in land) / len(land)
	if any(c.biome == WATER for c in cells):
		water = min(100.0, water + WATER_ADJACENCY_BONUS)
	return food * 0.6 + water * 0.4


class SettlementManager:
	def __init__(self):
		self.settlements = []

	def can_settle(self, world, x, y):
		# no water, no doubling up (same rules as the player tool)
		cell = world.get_cell(x, y)
		if cell is None:
			return False
		if cell.biome == WATER:
			return False
		if cell.settlement is not None:
			return False
		return True

	def create_settlement(self, world, x, y, name=None, cause="founded by the player"):
		if not self.can_settle(world, x, y):
			return None

		s = Settlement(x, y, name=name)
		world.get_cell(x, y).settlement = s
		self.settlements.append(s)

		data = s.event_data(world)
		data["cause"] = cause
		data["description"] = f"{s.name} was founded at ({x}, {y})."
		event_bus.emit(SETTLEMENT_CREATED, data)
		return s

	def update(self, world):
		# advance every settlement one year. call once per simulate_year
		for s in list(self.settlements):
			s.update(world)

			if s.state == STATE_COLLAPSED:
				self._remove(world, s)
				continue

			if s.wants_to_migrate():
				self._try_migrate(world, s)

	def _remove(self, world, settlement):
		cell = world.get_cell(settlement.x, settlement.y)
		if cell is not None and cell.settlement is settlement:
			cell.settlement = None
		if settlement in self.settlements:
			self.settlements.remove(settlement)

	def _try_migrate(self, world, settlement):
		# look for a spot thats actually better, not just slightly
		current_score = settlement.site_score()
		best_cell = None
		best_score = current_score + MIGRATION_MIN_IMPROVEMENT

		candidates = world.get_cells_in_radius(
			settlement.x, settlement.y, MIGRATION_SEARCH_RADIUS
		)
		for cell in candidates:
			if cell.biome == WATER or cell.settlement is not None:
				continue
			if cell.x == settlement.x and cell.y == settlement.y:
				continue
			score = _score_location(world, cell.x, cell.y)
			if score > best_score:
				best_score = score
				best_cell = cell

		if best_cell is None:
			return False  # nowhere better, stay and hope

		old_x, old_y = settlement.x, settlement.y
		old_cell = world.get_cell(old_x, old_y)
		if old_cell is not None and old_cell.settlement is settlement:
			old_cell.settlement = None

		settlement.x = best_cell.x
		settlement.y = best_cell.y
		best_cell.settlement = settlement
		settlement.critical_years = 0
		settlement.state = STATE_STABLE  # fresh start, no event for this

		data = settlement.event_data(world)
		data["from_x"] = old_x
		data["from_y"] = old_y
		data["cause"] = settlement._scarcity_cause()
		data["description"] = (
			f"{settlement.name} abandoned ({old_x}, {old_y}) and moved to "
			f"({settlement.x}, {settlement.y}) because {data['cause']}."
		)
		event_bus.emit(SETTLEMENT_MIGRATED, data)
		return True

	def connect_to_player_events(self):
		# divya's tool puts a placeholder dict on cell.settlement,
		# this swaps it for a real Settlement so the AI takes over
		event_bus.subscribe("PLAYER_PLACED_SETTLEMENT", self._on_player_placed)

	def _on_player_placed(self, data):
		cell = (data or {}).get("cell")
		if cell is None:
			return
		self.adopt_cell(cell)

	def adopt_cell(self, cell):
		if isinstance(cell.settlement, Settlement):
			if cell.settlement not in self.settlements:
				self.settlements.append(cell.settlement)
			return cell.settlement

		s = Settlement(cell.x, cell.y)
		cell.settlement = s
		self.settlements.append(s)
		# no CREATED event here, history already logged the player action
		return s

	def get_settlement_at(self, x, y):
		for s in self.settlements:
			if s.x == x and s.y == y:
				return s
		return None

	def total_population(self):
		return sum(s.population for s in self.settlements)

	def to_dict(self):
		return {
			"count": len(self.settlements),
			"total_population": self.total_population(),
			"settlements": [s.to_dict() for s in self.settlements],
		}


# shared instance like event_bus
settlement_manager = SettlementManager()