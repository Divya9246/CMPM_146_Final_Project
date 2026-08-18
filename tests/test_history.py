from src.core.event_bus import event_bus
from src.player.player_tools import plant_forest, deforest, place_settlement
from src.player.player_controller import PlayerController
from src.history.event_manager import EventManager
from src.history.history_generator import HistoryGenerator
from src.history.statistics import summarize_planet, format_summary
from src.history.world_event import WorldEvent


class FakeCell:
    def __init__(self, x, y, biome="grassland", height=40, moisture=70, temperature=50):
        self.x = x
        self.y = y
        self.biome = biome
        self.height = height
        self.moisture = moisture
        self.temperature = temperature
        self.settlement = None
        self.food = 40

    def compute_food(self):
        self.food = 55
        return self.food


def setup_manager():
    event_bus._listeners.clear()
    manager = EventManager()
    manager.connect()
    return manager


def test_cannot_plant_on_water():
    cell = FakeCell(1, 1, biome="water", height=10)
    result = plant_forest(cell, year=3)
    assert result["ok"] is False
    assert cell.biome == "water"


def test_plant_forest_changes_cell_and_history():
    manager = setup_manager()
    cell = FakeCell(4, 7, biome="grassland", moisture=80)
    result = plant_forest(cell, year=5)
    assert result["ok"] is True
    assert cell.biome == "forest"
    assert len(manager.events) == 1
    assert manager.events[0].year == 5
    assert manager.events[0].location == (4, 7)


def test_deforest_only_works_on_forest():
    grass = FakeCell(0, 0, biome="grassland")
    assert deforest(grass)["ok"] is False
    forest = FakeCell(2, 2, biome="forest")
    assert deforest(forest, year=8)["ok"] is True
    assert forest.biome == "grassland"


def test_place_settlement_once():
    manager = setup_manager()
    cell = FakeCell(3, 3, biome="forest")
    assert place_settlement(cell, year=1)["ok"] is True
    assert cell.settlement is not None
    assert place_settlement(cell, year=2)["ok"] is False
    assert len(manager.events) == 1


def test_controller_blocks_then_plants():
    setup_manager()
    controller = PlayerController()
    controller.set_tool("plant_forest")
    water = FakeCell(0, 0, biome="water", height=5)
    bad = controller.click_cell(water)
    assert bad["ok"] is False
    land = FakeCell(1, 1, biome="grassland", moisture=80)
    good = controller.click_cell(land)
    assert good["ok"] is True
    assert land.biome == "forest"


def test_history_reads_like_a_story():
    events = [
        WorldEvent(1, "PLAYER_PLACED_SETTLEMENT", "A settlement was founded at (2, 2)."),
        WorldEvent(4, "PLAYER_DEFORESTED", "The player removed forest at (3, 2)."),
        WorldEvent(10, "SETTLEMENT_MIGRATED", "The settlement left its home."),
    ]
    text = HistoryGenerator().generate(events)
    assert "The First Settlement" in text
    assert "The Great Clearing" in text
    assert "The Migration" in text
    assert "EVENT_" not in text


def test_summary_counts_player_actions():
    events = [
        WorldEvent(1, "PLAYER_PLANTED_FOREST", "planted"),
        WorldEvent(2, "PLAYER_DEFORESTED", "cut"),
    ]
    summary = summarize_planet(None, events)
    assert summary["player_interventions"] == 2
    assert "player actions 2" in format_summary(summary)