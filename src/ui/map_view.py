"""P5 — draws the world grid and handles hover / selection / action preview.

Rendering note: real 3D terrain is P1's job. Until then we fake depth by
shading each biome color with the cell's elevation, which reads surprisingly
well on a 2D grid.
"""
import pygame

from src.core.constants import WORLD_WIDTH, WORLD_HEIGHT
from src.ui import theme


def _shade(color, elevation):
    f = 0.6 + 0.55 * elevation           # low = darker, high = lighter
    return tuple(min(255, int(c * f)) for c in color)


class MapView:
    def __init__(self, world):
        self.world = world
        self.rect = pygame.Rect(theme.MAP_X, theme.MAP_Y,
                                WORLD_WIDTH * theme.CELL_PX,
                                WORLD_HEIGHT * theme.CELL_PX)

    def cell_at_pixel(self, pos):
        if not self.rect.collidepoint(pos):
            return None
        cx = (pos[0] - self.rect.x) // theme.CELL_PX
        cy = (pos[1] - self.rect.y) // theme.CELL_PX
        return self.world.cell(cx, cy)

    def _cell_rect(self, cell):
        return pygame.Rect(self.rect.x + cell.x * theme.CELL_PX,
                           self.rect.y + cell.y * theme.CELL_PX,
                           theme.CELL_PX, theme.CELL_PX)

    def draw(self, screen, selected, hovered, preview_quality):
        for row in self.world.cells:
            for cell in row:
                color = _shade(theme.BIOME_COLORS[cell.biome], cell.elevation)
                pygame.draw.rect(screen, color, self._cell_rect(cell))

        # settlements on top of terrain
        for s in self.world.settlements:
            r = self._cell_rect(self.world.cell(s.x, s.y)).inflate(-3, -3)
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
