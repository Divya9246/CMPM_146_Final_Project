"""P5 — GameWorld: the integration layer connecting all five systems.

This replaces the old src/ui/mock_world.py. The UI talks ONLY to this class,
which wires together the real modules:

  * P1  src/world/       — World grid + generate_world (terrain, climate values)
  * P2  src/simulation/  — simulate_year (climate drift, biome spread, events)
  * P3  src/agents/      — settlement_manager (behavior-tree settlement AI)
  * P4  src/player/ + src/history/ — PlayerController (tools + validation),
        EventManager (event memory), HistoryGenerator (story of the planet)

Nothing in here re-implements a teammate's system; it only calls them.
"""
import random

from src.core.constants import WATER, GRASSLAND, FOREST, DESERT
from src.world.world_grid import World
from src.world.terrain_generator import generate_world
from src.simulation.biome_simulation import simulate_year
from src.simulation.environmental_rules import calculate_biomeType
from src.agents.settlement_manager import settlement_manager
from src.player.player_controller import PlayerController
from src.history.event_manager import EventManager
from src.history.history_generator import HistoryGenerator
from src.history import statistics


class GameWorld:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randrange(1_000_000)

        # P1: build and generate the world grid
        self.world = World(seed=self.seed)
        generate_world(self.world, self.seed)

        # P4: event memory + story generator + player tools
        self.events = EventManager()
        self.events.connect()
        self.history_gen = HistoryGenerator()
        self.player = PlayerController(self.world)

        # P3: settlement AI. The manager is a shared singleton, so on a new
        # world (reset) we clear out settlements belonging to the old one.
        self._reset_settlement_manager()
        settlement_manager.connect_to_player_events()

        self.start_summary = statistics.summarize_planet(
            self.world, self.events.get_all_events())

    @staticmethod
    def _reset_settlement_manager():
        for s in list(settlement_manager.settlements):
            settlement_manager.settlements.remove(s)

    # ---- what the UI reads each frame -------------------------------------
    @property
    def cells(self):
        return self.world.grid

    @property
    def year(self):
        return self.world.year

    @property
    def settlements(self):
        return settlement_manager.settlements

    def cell(self, x, y):
        return self.world.get_cell(x, y)

    def settlement_at(self, x, y):
        return settlement_manager.get_settlement_at(x, y)

    def condition_word(self, cell):
        """Plain-language 'Biome condition' for the info panel: does the
        current climate (P2's rules) still support this cell's biome?"""
        if cell.biome == WATER:
            return "Open water"
        fits = calculate_biomeType(cell) == cell.biome
        return "Healthy" if fits else "Under pressure"

    def stats(self):
        counts = self.world.count_biomes()
        total = self.world.width * self.world.height
        pct = lambda b: round(100 * counts.get(b, 0) / total, 1)
        return {
            "year": self.world.year,
            "forest %": pct(FOREST),
            "desert %": pct(DESERT),
            "grass %": pct(GRASSLAND),
            "water %": pct(WATER),
            "settlements": len(settlement_manager.settlements),
            "population": settlement_manager.total_population(),
        }

    def summary(self):
        """End-of-demo numbers (P4's statistics module)."""
        return statistics.summarize_planet(self.world, self.events.get_all_events())

    def history_lines(self):
        """Story lines from P4's HistoryGenerator, with runs of repeated
        desert-spread years collapsed so the panel reads like a story."""
        events, filtered, last_type = self.events.get_all_events(), [], None
        for ev in events:
            if ev.event_type == "DESERT_SPREAD" and last_type == "DESERT_SPREAD":
                continue
            filtered.append(ev)
            last_type = ev.event_type
        text = self.history_gen.generate(filtered)
        return text.split("\n") if text else []

    # ---- simulation + reset ------------------------------------------------
    def tick(self):
        """One year: P2's climate/biomes, then P3's settlements."""
        simulate_year(self.world)
        settlement_manager.update(self.world)
