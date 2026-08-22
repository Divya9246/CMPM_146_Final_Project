"""P5 — the History overlay: the story of the planet (slide 24).

Reads events from P4's EventManager through the world object and shows the
most recent ones as readable lines. P4 owns what gets recorded and how it is
worded; this panel only displays it.
"""
import pygame

from src.ui import theme

MAX_LINES = 24


class HistoryPanel:
    def __init__(self, app):
        self.app = app
        w, h = theme.WINDOW_W - 160, theme.WINDOW_H - 160
        self.rect = pygame.Rect(80, 80, w, h)

    def draw(self, screen, font, font_small):
        overlay = pygame.Surface((theme.WINDOW_W, theme.WINDOW_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, theme.PANEL_BG, self.rect, border_radius=8)
        pygame.draw.rect(screen, theme.PANEL_BORDER, self.rect, 1, border_radius=8)

        x, y = self.rect.x + 16, self.rect.y + 12
        title = font.render("HISTORY OF THE PLANET", True, theme.ACCENT)
        screen.blit(title, (x, y))
        y += title.get_height() + 10

        events = self.app.world.events.get_all_events()[-MAX_LINES:]
        if not events:
            surf = font_small.render(
                "Nothing has happened yet. Let time run, or act on the world.",
                True, theme.TEXT_DIM)
            screen.blit(surf, (x, y))
        for ev in events:
            line = f"Year {ev.year} — {ev.description}"
            surf = font_small.render(line, True, theme.TEXT)
            screen.blit(surf, (x, y))
            y += surf.get_height() + 5

        hint = font_small.render("Press H or click History to close",
                                 True, theme.TEXT_DIM)
        screen.blit(hint, (x, self.rect.bottom - 26))
