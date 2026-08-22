import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.world.world_grid import World
from src.world.terrain_generator import generate_world
from src.core.constants import WATER, GRASSLAND, DESERT
from src.core.event_bus import event_bus
from src.agents.settlement import Settlement
from src.agents.settlement_manager import SettlementManager
from src.agents.agent_constants import (
	STARTING_POPULATION, MIN_POPULATION, MIGRATION_PATIENCE,
	STATE_GROWING, STATE_DECLINING, STATE_COLLAPSED, STATE_STABLE,
	SETTLEMENT_CREATED, SETTLEMENT_GREW, SETTLEMENT_DECLINED,
	SETTLEMENT_MIGRATED, SETTLEMENT_COLLAPSED,
)


def make_flat_world(biome=GRASSLAND, food=60.0, moisture=60.0):
	# hand built flat world, no noise so tests are deterministic
	w = World()
	for c in w.get_all_cells():
		c.biome = biome
		c.height = 40.0
		c.moisture = moisture
		c.precipitation = moisture
		c.temperature = 60.0
		c.food = food
	return w


def capture(event_type):
	# collect events of one type into a list
	events = []
	event_bus.subscribe(event_type, events.append)
	return events


from src.agents.behavior_tree import (
	Sequence, Selector, Condition, Action, Inverter, SUCCESS, FAILURE,
)


def test_behavior_tree_sequence_and_selector():
	log = []
	yes = Condition(lambda ctx: True, name="yes")
	no = Condition(lambda ctx: False, name="no")
	say = lambda tag: Action(lambda ctx: log.append(tag), name=tag)

	# sequence stops at the first failure
	assert Sequence(yes, say("a"), no, say("never")).tick({}) == FAILURE
	assert log == ["a"]

	# selector picks the first branch that passes
	log.clear()
	tree = Selector(
		Sequence(no, say("skipped")),
		Sequence(yes, say("chosen")),
		say("fallback"),
	)
	assert tree.tick({}) == SUCCESS
	assert log == ["chosen"]

	# inverter flips
	assert Inverter(no).tick({}) == SUCCESS
	assert Inverter(yes).tick({}) == FAILURE


def test_settlement_tree_priority_order():
	# thriving settlement should take the grow branch
	w = make_flat_world(food=80.0, moisture=80.0)
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	s.update(w)
	assert s.state == STATE_GROWING
	# starve it, same tree should now pick decline
	for c in w.get_all_cells():
		c.food = 5.0
		c.moisture = 5.0
		c.precipitation = 5.0
	s.update(w)
	assert s.state == STATE_DECLINING


def test_create_settlement_sets_cell_field():
	w = make_flat_world()
	m = SettlementManager()
	s = m.create_settlement(w, 10, 10)
	assert s is not None
	assert w.get_cell(10, 10).settlement is s
	assert s in m.settlements


def test_create_emits_created_event():
	w = make_flat_world()
	m = SettlementManager()
	events = capture(SETTLEMENT_CREATED)
	m.create_settlement(w, 5, 5)
	assert len(events) == 1
	assert events[0]["x"] == 5 and events[0]["y"] == 5
	assert "year" in events[0]


def test_cannot_settle_on_water():
	w = make_flat_world(biome=WATER)
	m = SettlementManager()
	assert m.create_settlement(w, 10, 10) is None


def test_cannot_settle_twice_on_same_cell():
	w = make_flat_world()
	m = SettlementManager()
	assert m.create_settlement(w, 10, 10) is not None
	assert m.create_settlement(w, 10, 10) is None


def test_population_grows_in_good_conditions():
	w = make_flat_world(food=80.0, moisture=80.0)
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	m.update(w)
	assert s.population > STARTING_POPULATION
	assert s.state == STATE_GROWING


def test_grew_event_emitted_once_not_every_tick():
	w = make_flat_world(food=80.0, moisture=80.0)
	m = SettlementManager()
	m.create_settlement(w, 25, 25)
	events = capture(SETTLEMENT_GREW)
	for _ in range(5):
		m.update(w)
	# stable->growing happens once, then it stays growing, so only 1 event
	assert len(events) == 1


def test_population_declines_in_bad_conditions():
	w = make_flat_world(biome=DESERT, food=10.0, moisture=10.0)
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	events = capture(SETTLEMENT_DECLINED)
	m.update(w)
	assert s.population < STARTING_POPULATION
	assert s.state == STATE_DECLINING
	assert len(events) == 1
	assert "cause" in events[0]


def test_settlement_collapses_and_is_removed():
	w = make_flat_world(biome=DESERT, food=0.0, moisture=0.0)
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	s.population = MIN_POPULATION  # one bad year from collapse
	events = capture(SETTLEMENT_COLLAPSED)
	for _ in range(3):
		m.update(w)
	assert len(events) == 1
	assert s not in m.settlements
	assert w.get_cell(25, 25).settlement is None


def test_migration_to_better_land():
	# wasteland everywhere except one lush patch
	w = make_flat_world(biome=DESERT, food=5.0, moisture=5.0)
	# patch is outside its read radius but inside search radius
	for c in w.get_cells_in_radius(31, 25, 2):
		c.biome = GRASSLAND
		c.food = 90.0
		c.moisture = 90.0
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	s.population = 200  # buffer so it survives long enough to migrate
	events = capture(SETTLEMENT_MIGRATED)
	for _ in range(MIGRATION_PATIENCE + 1):
		m.update(w)
	assert len(events) == 1
	assert (s.x, s.y) != (25, 25)
	assert w.get_cell(25, 25).settlement is None
	assert w.get_cell(s.x, s.y).settlement is s
	assert events[0]["from_x"] == 25 and events[0]["from_y"] == 25


def test_no_migration_when_nowhere_better():
	w = make_flat_world(biome=DESERT, food=5.0, moisture=5.0)
	m = SettlementManager()
	s = m.create_settlement(w, 25, 25)
	s.population = 300
	events = capture(SETTLEMENT_MIGRATED)
	for _ in range(MIGRATION_PATIENCE + 2):
		m.update(w)
	assert len(events) == 0
	assert (s.x, s.y) == (25, 25)


def test_works_on_generated_world():
	# smoke test on the real generated terrain
	w = World()
	generate_world(w, seed=42)
	m = SettlementManager()
	# settle the best land cell
	target = max(
		(c for c in w.get_all_cells() if c.biome != WATER),
		key=lambda c: c.food,
	)
	s = m.create_settlement(w, target.x, target.y)
	assert s is not None
	for _ in range(10):
		m.update(w)
		w.year += 1
	# should still be alive on good land
	assert s in m.settlements
	assert s.population > 0


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