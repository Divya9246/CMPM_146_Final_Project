"""P5 — the Echo Earth application: game loop and system integration.

INTEGRATION SWAP POINTS (for Sprint 2)
--------------------------------------
The UI talks to the world only through the object created in `make_world()`.
When teammates' real modules are merged, replace the MockWorld pieces:

  * P1 terrain  -> build the cell grid with src/world/ instead of
                   MockWorld._generate()
  * P2 climate  -> call the real per-tick biome/climate update instead of
                   MockWorld._tick_biomes()
  * P3 agents   -> real settlement objects/AI instead of MockSettlement and
                   MockWorld._tick_settlements()
  * P4 actions  -> already integrated: the UI calls src/player/player_tools
                   and displays src/history/ events; P4's handlers just need
                   to subscribe to the same event names MockWorld does.

As long as the replacement exposes: .cells / .cell(x,y) / .neighbors /
.settlement_at / .forest_suitability / .stats / .tick() / .year / .events,
nothing in the UI has to change.
"""
import pygame

from src.core.event_bus import event_bus
from src.ui import theme, controls
from src.ui.mock_world import MockWorld
from src.ui.sim_clock import SimClock
from src.ui.map_view import MapView
from src.ui.hud import Hud
from src.ui.cell_info_panel import CellInfoPanel
from src.ui.history_panel import HistoryPanel
from src.ui.widgets import Notifications


def make_world(seed=None):
    """Single place where the world implementation is chosen."""
    return MockWorld(seed=seed)


class EchoEarthApp:
    def __init__(self, seed=None):
        pygame.init()
        pygame.display.set_caption("Echo Earth")
        self.screen = pygame.display.set_mode((theme.WINDOW_W, theme.WINDOW_H))
        self.font = pygame.font.SysFont("dejavusans,arial", 15)
        self.font_small = pygame.font.SysFont("dejavusans,arial", 13)
        self.font_big = pygame.font.SysFont("dejavusans,arial", 20, bold=True)

        self.clock = SimClock()
        self.notifications = Notifications()
        self.selected = None
        self.armed_tool = None
        self.feedback = ""
        self.show_history = False
        self._pygame_clock = pygame.time.Clock()
        self.running = True

        self._build_world(seed)
        event_bus.subscribe("HISTORY_EVENT", self._on_history_event)

    # ---- world / notifications -------------------------------------------
    def _build_world(self, seed=None):
        self.world = make_world(seed)
        self.map_view = MapView(self.world)
        self.hud = Hud(self.clock, self)
        self.panel = CellInfoPanel(self)
        self.history_panel = HistoryPanel(self)

    def _on_history_event(self, ev):
        self.notifications.push(f"Year {ev.year}: {ev.description}")

    def reset_world(self):
        self.selected = None
        self.armed_tool = None
        self.feedback = "World reset."
        self.clock.paused = True
        self._build_world()          # new seed each reset

    # ---- player intent ----------------------------------------------------
    def arm_tool(self, tool):
        self.armed_tool = None if self.armed_tool == tool else tool
        self.feedback = f"Tool armed: {tool}" if self.armed_tool else ""

    def toggle_history(self):
        self.show_history = not self.show_history

    def _click_map(self, cell):
        self.selected = cell
        if not self.armed_tool:
            return
        quality, reason = controls.preview(self.world, self.armed_tool, cell)
        if quality == "bad":
            self.feedback = f"Blocked: {reason}"
            return
        controls.apply_tool(self.armed_tool, cell)
        self.feedback = f"{self.armed_tool} done. {reason}"

    # ---- event handling ---------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.clock.toggle_pause()
            elif event.key == pygame.K_h:
                self.toggle_history()
            elif event.key == pygame.K_r:
                self.reset_world()
            elif event.key == pygame.K_ESCAPE:
                self.armed_tool = None
                self.show_history = False
                self.feedback = ""
            elif event.key in controls.SPEED_KEYS:
                self.clock.set_speed(controls.SPEED_KEYS[event.key])
            elif event.key in controls.TOOL_KEYS:
                self.arm_tool(controls.TOOL_KEYS[event.key])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_history:
                self.show_history = False
                return
            if self.hud.handle_click(event.pos):
                return
            if self.panel.handle_click(event.pos):
                return
            cell = self.map_view.cell_at_pixel(event.pos)
            if cell:
                self._click_map(cell)

    # ---- per-frame update/draw (also used by headless tests) --------------
    def step_frame(self, dt):
        for _ in range(self.clock.update(dt)):
            self.world.tick()
        self.notifications.update(dt)

        hovered = self.map_view.cell_at_pixel(pygame.mouse.get_pos())
        quality = None
        if hovered and self.armed_tool:
            quality, _ = controls.preview(self.world, self.armed_tool, hovered)

        self.screen.fill(theme.BG)
        self.map_view.draw(self.screen, self.selected, hovered, quality)
        self.hud.draw(self.screen, self.font, self.font_big)
        self.panel.draw(self.screen, self.font, self.font_small)
        self.notifications.draw(self.screen, self.font_small,
                                theme.MAP_X + 8, theme.MAP_Y + 8, 380)
        if self.show_history:
            self.history_panel.draw(self.screen, self.font, self.font_small)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self._pygame_clock.tick(theme.FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.step_frame(dt)
        pygame.quit()


def run():
    EchoEarthApp().run()
