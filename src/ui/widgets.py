"""P5 — small reusable UI pieces: buttons and toast notifications."""
import pygame

from src.ui import theme


class Button:
    def __init__(self, rect, label, on_click, is_active=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.is_active = is_active   # optional callable -> bool (highlight)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.on_click()
            return True
        return False

    def draw(self, screen, font):
        active = bool(self.is_active and self.is_active())
        bg = theme.BTN_BG_ACTIVE if active else theme.BTN_BG
        pygame.draw.rect(screen, bg, self.rect, border_radius=4)
        pygame.draw.rect(screen, theme.BTN_BORDER, self.rect, 1, border_radius=4)
        text = font.render(self.label, True, theme.TEXT)
        screen.blit(text, text.get_rect(center=self.rect.center))


class Notifications:
    """Short-lived toast messages (slide 23: immediate feedback,
    slide 21: small event notification area)."""

    LIFETIME = 4.0   # seconds
    MAX_SHOWN = 4

    def __init__(self):
        self._items = []   # list of [text, time_left]

    def push(self, text):
        self._items.append([text, self.LIFETIME])
        self._items = self._items[-self.MAX_SHOWN:]

    def update(self, dt):
        for item in self._items:
            item[1] -= dt
        self._items = [i for i in self._items if i[1] > 0]

    def draw(self, screen, font, x, y, width):
        for text, time_left in self._items:
            alpha = min(1.0, time_left / 1.0)
            surf = font.render(text, True, theme.TEXT)
            box = pygame.Surface((width, surf.get_height() + 10), pygame.SRCALPHA)
            box.fill((20, 22, 26, int(215 * alpha)))
            box.blit(surf, (8, 5))
            screen.blit(box, (x, y))
            y += box.get_height() + 4
