"""P5 — mock world + mock simulation used until teammates' real modules land.

Per the Sprint 1 plan, Person 5 builds the UI and integration harness against
mock systems. This module fakes, in miniature, what P1-P4 will provide:

  * P1 (src/world/):      terrain generation  -> MockWorld._generate()
  * P2 (src/simulation/): climate/biome tick  -> MockWorld._tick_biomes()
  * P3 (src/agents/):     settlement AI       -> MockWorld._tick_settlements()
  * P4 (src/player/ + src/history/): actions + events -> apply_* / EventManager

It uses only the frozen shared contracts from src/core/ (Cell, biome names,
value ranges, event bus), so swapping in the real modules later should not
require UI changes — see src/ui/app.py for the swap points.
"""
import random

from src.core.constants import (
    WATER, GRASSLAND, FOREST, DESERT,
    WORLD_WIDTH, WORLD_HEIGHT,
)
from src.core.world_types import Cell
from src.core.event_bus import event_bus
from src.history.event_manager import EventManager
from src.history.world_event import WorldEvent


class MockSettlement:
    """Stand-in for P3's settlement object (population / food / water)."""

    _next_id = 1

    def __init__(self, x, y, year):
        self.id = MockSettlement._next_id
        MockSettlement._next_id += 1
        self.x, self.y = x, y
        self.founded_year = year
        self.population = 25
        self.food = 60.0
        self.water = 60.0
        self.status = "settling in"


class MockWorld:
    """Owns the cell grid, settlements, and the per-tick update rules."""

    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randrange(10_000)
        self.year = 0
        self.events = EventManager()
        self.settlements = []
        self.start_stats = None
        self._generate()
        self._wire_player_actions()

    # ---- generation (mock of P1) -----------------------------------------
    def _generate(self):
        rng = random.Random(self.seed)
        w, h = WORLD_WIDTH, WORLD_HEIGHT

        # smooth value-noise: coarse random lattice, bilinear-interpolated
        def noise_grid(step, lo=0.0, hi=1.0):
            gw, gh = w // step + 2, h // step + 2
            lattice = [[rng.random() for _ in range(gw)] for _ in range(gh)]
            grid = []
            for y in range(h):
                row = []
                gy, fy = divmod(y, step)
                ty = fy / step
                for x in range(w):
                    gx, fx = divmod(x, step)
                    tx = fx / step
                    a = lattice[gy][gx] * (1 - tx) + lattice[gy][gx + 1] * tx
                    b = lattice[gy + 1][gx] * (1 - tx) + lattice[gy + 1][gx + 1] * tx
                    row.append(lo + (a * (1 - ty) + b * ty) * (hi - lo))
                grid.append(row)
            return grid

        elev = noise_grid(10)
        moist = noise_grid(12, 15, 95)
        self.cells = []
        for y in range(h):
            row = []
            for x in range(w):
                e = elev[y][x]
                # temperature: warm at equator (middle rows), cooler at poles
                lat = abs(y - h / 2) / (h / 2)
                t = max(0.0, min(100.0, 85 - lat * 55 + rng.uniform(-4, 4)))
                m = moist[y][x]
                if e < 0.35:
                    biome = WATER
                elif m > 62 and 35 < t < 90:
                    biome = FOREST
                elif m < 30 and t > 55:
                    biome = DESERT
                else:
                    biome = GRASSLAND
                row.append(Cell(x=x, y=y, elevation=e, biome=biome,
                                temperature=t, moisture=m))
            self.cells.append(row)
        self.start_stats = self.stats()

    # ---- shared helpers ---------------------------------------------------
    def cell(self, x, y):
        if 0 <= x < WORLD_WIDTH and 0 <= y < WORLD_HEIGHT:
            return self.cells[y][x]
        return None

    def neighbors(self, cell):
        out = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = self.cell(cell.x + dx, cell.y + dy)
            if n:
                out.append(n)
        return out

    def settlement_at(self, x, y):
        for s in self.settlements:
            if s.x == x and s.y == y:
                return s
        return None

    def forest_suitability(self, cell):
        """0..1 score — mock of P2's climate->biome suitability rule."""
        if cell.biome == WATER:
            return 0.0
        t_ok = 1.0 - min(1.0, abs(cell.temperature - 62) / 45)
        m_ok = max(0.0, min(1.0, (cell.moisture - 25) / 50))
        return t_ok * m_ok

    def stats(self):
        flat = [c for row in self.cells for c in row]
        n = len(flat)
        return {
            "year": self.year,
            "forest %": round(100 * sum(c.biome == FOREST for c in flat) / n, 1),
            "desert %": round(100 * sum(c.biome == DESERT for c in flat) / n, 1),
            "grass %": round(100 * sum(c.biome == GRASSLAND for c in flat) / n, 1),
            "water %": round(100 * sum(c.biome == WATER for c in flat) / n, 1),
            "settlements": len(self.settlements),
            "population": sum(s.population for s in self.settlements),
        }

    def _record(self, etype, desc, loc=None, cause=None):
        ev = WorldEvent(year=self.year, event_type=etype, description=desc,
                        location=loc, cause=cause)
        self.events.record(ev)
        event_bus.emit("HISTORY_EVENT", ev)   # UI notifications listen to this

    # ---- player actions (mock of P4's action handling) --------------------
    def _wire_player_actions(self):
        event_bus.subscribe("PLAYER_PLANTED_FOREST", self._on_plant)
        event_bus.subscribe("PLAYER_DEFORESTED", self._on_deforest)
        event_bus.subscribe("PLAYER_PLACED_SETTLEMENT", self._on_place)

    def _owns(self, cell):
        """The shared EventBus has no unsubscribe, so old worlds (after a
        reset) still hear player events. Only react to cells from THIS world."""
        return self.cell(cell.x, cell.y) is cell

    def _on_plant(self, data):
        cell = data["cell"]
        if not self._owns(cell):
            return
        cell.biome = FOREST
        self._record("PLAYER_PLANTED_FOREST",
                     f"The player planted a forest at ({cell.x}, {cell.y}).",
                     (cell.x, cell.y), cause="player action")

    def _on_deforest(self, data):
        cell = data["cell"]
        if not self._owns(cell):
            return
        cell.biome = GRASSLAND
        cell.moisture = max(0.0, cell.moisture - 6)  # small local drying
        self._record("PLAYER_DEFORESTED",
                     f"The player cleared the forest at ({cell.x}, {cell.y}).",
                     (cell.x, cell.y), cause="player action")

    def _on_place(self, data):
        cell = data["cell"]
        if not self._owns(cell):
            return
        s = MockSettlement(cell.x, cell.y, self.year)
        self.settlements.append(s)
        self._record("PLAYER_PLACED_SETTLEMENT",
                     f"A settlement was founded at ({cell.x}, {cell.y}).",
                     (cell.x, cell.y), cause="player action")

    # ---- simulation tick ---------------------------------------------------
    def tick(self):
        """Advance the world by one year."""
        self.year += 1
        self._tick_biomes()
        self._tick_settlements()

    def _tick_biomes(self):
        rng = random.Random(self.seed * 100_003 + self.year)
        changes = []
        for row in self.cells:
            for c in row:
                if c.biome == WATER:
                    continue
                suit = self.forest_suitability(c)
                if c.biome == FOREST:
                    if suit < 0.15 and rng.random() < 0.25:
                        changes.append((c, GRASSLAND))       # forest dies off
                    elif suit > 0.45 and rng.random() < 0.06:
                        opts = [n for n in self.neighbors(c)
                                if n.biome == GRASSLAND
                                and self.forest_suitability(n) > 0.3]
                        if opts:
                            changes.append((rng.choice(opts), FOREST))
                elif c.biome == GRASSLAND:
                    if c.moisture < 22 and c.temperature > 60 and rng.random() < 0.04:
                        changes.append((c, DESERT))          # desertification
                elif c.biome == DESERT:
                    if c.moisture > 45 and rng.random() < 0.03:
                        changes.append((c, GRASSLAND))       # recovery
        for c, b in changes:
            c.biome = b
        # record only milestones, not every flip (slide 24: no debug-log spam)
        n_desert = sum(1 for _, b in changes if b == DESERT)
        if n_desert >= 3:
            self._record("DESERT_SPREAD",
                         f"Dry lands expanded — {n_desert} areas turned to desert.")

    def _tick_settlements(self):
        rng = random.Random(self.seed * 100_003 + self.year + 51_679)
        for s in list(self.settlements):
            cell = self.cell(s.x, s.y)
            near = self.neighbors(cell) + [cell]
            food_supply = sum(2.5 for n in near if n.biome in (GRASSLAND, FOREST))
            water_supply = sum(3.0 for n in near if n.biome == WATER
                               or n.moisture > 55)
            s.food = max(0.0, min(100.0, s.food + food_supply - s.population * 0.12))
            s.water = max(0.0, min(100.0, s.water + water_supply - s.population * 0.10))

            if s.food > 30 and s.water > 30:
                s.population += rng.randint(1, 3)
                s.status = "growing"
            elif s.food > 10 and s.water > 10:
                s.status = "struggling"
            else:
                s.population -= rng.randint(2, 5)
                s.status = "declining"

            if s.population <= 0:
                self.settlements.remove(s)
                self._record("SETTLEMENT_COLLAPSED",
                             f"The settlement at ({s.x}, {s.y}) collapsed.",
                             (s.x, s.y), cause="resources ran out")
            elif s.status == "declining" and rng.random() < 0.3:
                target = self._best_nearby_cell(s)
                if target:
                    old = (s.x, s.y)
                    s.x, s.y = target.x, target.y
                    s.status = "migrating"
                    self._record("SETTLEMENT_MIGRATED",
                                 f"The settlement at {old} migrated to "
                                 f"({s.x}, {s.y}) in search of resources.",
                                 (s.x, s.y), cause="declining resources")
            elif s.status == "growing" and s.population in range(98, 103):
                self._record("SETTLEMENT_GREW",
                             f"The settlement at ({s.x}, {s.y}) grew into a town "
                             f"of {s.population} people.", (s.x, s.y))

    def _best_nearby_cell(self, s):
        best, best_score = None, -1.0
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                c = self.cell(s.x + dx, s.y + dy)
                if not c or c.biome == WATER or self.settlement_at(c.x, c.y):
                    continue
                score = self.forest_suitability(c) + c.moisture / 200
                if score > best_score:
                    best, best_score = c, score
        return best
