"""P5 — the History overlay: the story of the planet.

Displays P4's HistoryGenerator output (titled story lines like
"Year 17 — The Great Clearing: ...") plus the end-of-run planet summary
from P4's statistics module.
"""
import pygame

from src.ui import theme

MAX_LINES = 22


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

        lines = self.app.game.history_lines()
        if not lines:
            surf = font_small.render(
                "Nothing has happened yet. Let time run, or act on the world.",
                True, theme.TEXT_DIM)
            screen.blit(surf, (x, y))
        shown = lines[-MAX_LINES:]
        if len(lines) > MAX_LINES:
            surf = font_small.render(
                f"... {len(lines) - MAX_LINES} earlier events ...",
                True, theme.TEXT_DIM)
            screen.blit(surf, (x, y))
            y += surf.get_height() + 5
        for line in shown:
            surf = font_small.render(line[:110], True, theme.TEXT)
            screen.blit(surf, (x, y))
            y += surf.get_height() + 5

        # planet summary (P4's statistics) at the bottom
        s = self.app.game.summary()
        summary = (f"So far: {s['player_interventions']} player actions, "
                   f"{s['migrations']} migrations, {s['collapses']} collapses.")
        surf = font_small.render(summary, True, theme.ACCENT)
        screen.blit(surf, (x, self.rect.bottom - 48))

        hint = font_small.render("Press H or click History to close",
                                 True, theme.TEXT_DIM)
        screen.blit(hint, (x, self.rect.bottom - 26))
