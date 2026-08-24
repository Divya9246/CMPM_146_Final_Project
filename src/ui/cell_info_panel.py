"""P5 — right-hand panel: tools, selected-cell info, settlement info, stats.

Shows P1's terrain values, P2's biome condition, and P3's real settlement
state (name, population, food/water supply, behavior state) in the plain
language the design deck asks for.
"""
import pygame

from src.ui import theme
from src.ui import controls
from src.ui.widgets import Button


class CellInfoPanel:
    def __init__(self, app):
        self.app = app
        self.rect = pygame.Rect(theme.PANEL_X, theme.MAP_Y,
                                theme.PANEL_W, 600)
        self.tool_buttons = []
        y = self.rect.y + 34
        for tool in controls.TOOLS:
            self.tool_buttons.append(
                Button((self.rect.x + 10, y, self.rect.w - 20, 30), tool,
                        lambda t=tool: app.arm_tool(t),
                        lambda t=tool: app.armed_tool == t))
            y += 36

    def handle_click(self, pos):
        return any(b.handle_click(pos) for b in self.tool_buttons)

    # ---- drawing ----------------------------------------------------------
    def draw(self, screen, font, font_small):
        pygame.draw.rect(screen, theme.PANEL_BG, self.rect, border_radius=6)
        pygame.draw.rect(screen, theme.PANEL_BORDER, self.rect, 1, border_radius=6)

        x = self.rect.x + 10
        y = self.rect.y + 10
        y = self._text(screen, font, "TOOLS  (F / D / S)", x, y, theme.TEXT_DIM)
        for b in self.tool_buttons:
            b.draw(screen, font_small)
        y = self.tool_buttons[-1].rect.bottom + 12

        # last action feedback / armed-tool hint
        if self.app.feedback:
            y = self._wrapped(screen, font_small, self.app.feedback, x, y,
                                theme.ACCENT) + 6

        y = self._section(screen, font, "SELECTED AREA", x, y)
        cell = self.app.selected
        if cell is None:
            y = self._text(screen, font_small, "Click a cell on the map.", x, y,
                            theme.TEXT_DIM)
            if not self.app.armed_tool:
                y = self._wrapped(
                    screen, font_small,
                    "Pick a tool, then click the map. Green = good, yellow = risky, red = blocked.",
                    x, y, theme.TEXT_DIM,
                )
        else:
            rows = [
                f"Location: ({cell.x}, {cell.y})",
                f"Biome: {cell.biome.capitalize()}",
                f"Elevation: {cell.height:.0f}",
                f"Temperature: {cell.temperature:.0f}",
                f"Moisture: {cell.moisture:.0f}",
                f"Food value: {cell.food:.0f}",
                f"Condition: {self.app.game.condition_word(cell)}",
            ]
            for r in rows:
                y = self._text(screen, font_small, r, x, y)

            s = self.app.game.settlement_at(cell.x, cell.y)
            if s:
                y = self._section(screen, font, s.name.upper(), x, y + 6)
                for r in (f"Population: {s.population}",
                          f"Food supply: {s.food_supply:.0f}",
                          f"Water supply: {s.water_supply:.0f}",
                          f"Status: {s.state}"):
                    y = self._text(screen, font_small, r, x, y)

        # world stats at the bottom of the panel
        stats = self.app.game.stats()
        y = self.rect.bottom - 118
        y = self._section(screen, font, "WORLD", x, y)
        for k in ("forest %", "desert %", "grass %", "settlements", "population"):
            y = self._text(screen, font_small, f"{k}: {stats[k]}", x, y)

    def _text(self, screen, font, text, x, y, color=theme.TEXT):
        surf = font.render(text, True, color)
        screen.blit(surf, (x, y))
        return y + surf.get_height() + 3

    def _wrapped(self, screen, font, text, x, y, color=theme.TEXT):
        """Simple word-wrap so long messages from P4 fit the panel."""
        words, line = text.split(), ""
        max_w = self.rect.w - 24
        for w in words:
            trial = (line + " " + w).strip()
            if font.size(trial)[0] <= max_w:
                line = trial
            else:
                y = self._text(screen, font, line, x, y, color)
                line = w
        if line:
            y = self._text(screen, font, line, x, y, color)
        return y

    def _section(self, screen, font, title, x, y):
        y = self._text(screen, font, title, x, y + 4, theme.TEXT_DIM)
        pygame.draw.line(screen, theme.PANEL_BORDER,
                         (x, y - 2), (self.rect.right - 10, y - 2))
        return y + 2
