"""P5 — draws the world grid and handles hover / selection / action preview.

Works on P1's real cells: `height` is 0-100 and is used to shade each biome
color, which fakes a 3D relief look on the 2D grid. (P1's Ursina renderer in
src/world/biome_renderer.py stays available if the team switches to 3D.)
"""
import pygame

from src.core.constants import WORLD_WIDTH, WORLD_HEIGHT, WATER_HEIGHT_MAX
from src.ui import theme


def _shade(color, height):
    f = 0.6 + 0.55 * min(1.0, max(0.0, height / 100.0))
    return tuple(min(255, int(c * f)) for c in color)


class MapView:
    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(theme.MAP_X, theme.MAP_Y,
                                WORLD_WIDTH * theme.CELL_PX,
                                WORLD_HEIGHT * theme.CELL_PX)

    def cell_at_pixel(self, pos):
        if not self.rect.collidepoint(pos):
            return None
        cx = (pos[0] - self.rect.x) // theme.CELL_PX
        cy = (pos[1] - self.rect.y) // theme.CELL_PX
        return self.game.cell(cx, cy)

    def _cell_rect(self, cell):
        return pygame.Rect(self.rect.x + cell.x * theme.CELL_PX,
                           self.rect.y + cell.y * theme.CELL_PX,
                           theme.CELL_PX, theme.CELL_PX)

    def draw(self, screen, selected, hovered, preview_quality):
        for row in self.game.cells:
            for cell in row:
                shade_h = WATER_HEIGHT_MAX if cell.biome == "water" else cell.height
                color = _shade(theme.BIOME_COLORS[cell.biome], shade_h)
                pygame.draw.rect(screen, color, self._cell_rect(cell))

        # settlements on top of terrain (P3's real settlements)
        for s in self.game.settlements:
            cell = self.game.cell(s.x, s.y)
            if cell is None:
                continue
            r = self._cell_rect(cell).inflate(-3, -3)
            pygame.draw.rect(screen, theme.SETTLEMENT_COLOR, r)
            pygame.draw.rect(screen, (40, 40, 40), r, 1)

        # hover: action preview color if a tool is armed, else soft white
        if hovered:
            colors = {"good": theme.PREVIEW_GOOD,
                      "risky": theme.PREVIEW_RISKY,
                      "bad": theme.PREVIEW_BAD}
            color = colors.get(preview_quality, (255, 255, 255))
            pygame.draw.rect(screen, color, self._cell_rect(hovered), 2)

        if selected:
            pygame.draw.rect(screen, theme.SELECT_COLOR,
                             self._cell_rect(selected).inflate(2, 2), 2)

        pygame.draw.rect(screen, theme.PANEL_BORDER, self.rect.inflate(2, 2), 1)
