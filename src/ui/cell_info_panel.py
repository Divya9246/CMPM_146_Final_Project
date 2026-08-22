"""P5 — right-hand panel: tools, selected-cell info, settlement info, stats.

Follows slide 21: show useful information in simple language, hide debug
values, keep the main screen clean.
"""
import pygame

from src.ui import theme
from src.ui import controls
from src.ui.widgets import Button


def _condition_word(suitability):
    if suitability > 0.45:
        return "Healthy"
    if suitability > 0.15:
        return "Fragile"
    return "Harsh"


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

        # armed-tool hint / last action feedback
        if self.app.feedback:
            y = self._text(screen, font_small, self.app.feedback, x, y,
                           theme.ACCENT) + 6

        y = self._section(screen, font, "SELECTED AREA", x, y)
        cell = self.app.selected
        if cell is None:
            y = self._text(screen, font_small, "Click a cell on the map.", x, y,
                           theme.TEXT_DIM)
        else:
            suit = self.app.world.forest_suitability(cell)
            rows = [
                f"Location: ({cell.x}, {cell.y})",
                f"Biome: {cell.biome.capitalize()}",
                f"Temperature: {cell.temperature:.0f}",
                f"Moisture: {cell.moisture:.0f}",
                f"Condition: {_condition_word(suit)}",
            ]
            for r in rows:
                y = self._text(screen, font_small, r, x, y)

            s = self.app.world.settlement_at(cell.x, cell.y)
            if s:
                y = self._section(screen, font, "SETTLEMENT", x, y + 6)
                for r in (f"Population: {s.population}",
                          f"Food: {s.food:.0f}   Water: {s.water:.0f}",
                          f"Status: {s.status}",
                          f"Founded: year {s.founded_year}"):
                    y = self._text(screen, font_small, r, x, y)

        # world stats at the bottom of the panel
        stats = self.app.world.stats()
        y = self.rect.bottom - 118
        y = self._section(screen, font, "WORLD", x, y)
        for k in ("forest %", "desert %", "grass %", "settlements", "population"):
            y = self._text(screen, font_small, f"{k}: {stats[k]}", x, y)

    def _text(self, screen, font, text, x, y, color=theme.TEXT):
        surf = font.render(text, True, color)
        screen.blit(surf, (x, y))
        return y + surf.get_height() + 3

    def _section(self, screen, font, title, x, y):
        y = self._text(screen, font, title, x, y + 4, theme.TEXT_DIM)
        pygame.draw.line(screen, theme.PANEL_BORDER,
                         (x, y - 2), (self.rect.right - 10, y - 2))
        return y + 2
