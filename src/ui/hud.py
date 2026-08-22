"""P5 — top HUD bar: year, time controls, armed tool, and key hints."""
import pygame

from src.ui import theme
from src.ui.widgets import Button


class Hud:
    def __init__(self, clock, app):
        self.clock = clock
        self.app = app
        x = 10
        self.buttons = [
            Button((x, 9, 84, 30), "Play/Pause",
                   clock.toggle_pause, lambda: not clock.paused),
        ]
        x += 92
        for spd in (1, 2, 4):
            self.buttons.append(
                Button((x, 9, 44, 30), f"{spd}x",
                       lambda s=spd: clock.set_speed(s),
                       lambda s=spd: clock.speed == s and not clock.paused))
            x += 50
        self.buttons.append(
            Button((x + 8, 9, 84, 30), "History",
                   app.toggle_history, lambda: app.show_history))
        self.buttons.append(
            Button((x + 100, 9, 70, 30), "Reset", app.reset_world))

    def handle_click(self, pos):
        return any(b.handle_click(pos) for b in self.buttons)

    def draw(self, screen, font, font_big):
        pygame.draw.rect(screen, theme.PANEL_BG,
                         (0, 0, theme.WINDOW_W, theme.HUD_H))
        pygame.draw.line(screen, theme.PANEL_BORDER,
                         (0, theme.HUD_H), (theme.WINDOW_W, theme.HUD_H))
        for b in self.buttons:
            b.draw(screen, font)

        year = font_big.render(f"Year {self.app.game.year}", True, theme.ACCENT)
        screen.blit(year, (theme.WINDOW_W - year.get_width() - 14, 12))

        state = font.render(self.clock.label, True, theme.TEXT_DIM)
        screen.blit(state, (theme.WINDOW_W - year.get_width() - 90, 17))
