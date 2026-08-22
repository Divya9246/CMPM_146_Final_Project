"""P5 — simulation clock: play/pause and 1x/2x/4x speed.

The clock converts real time into simulation ticks. The UI asks it every
frame how many ticks to run; at 1x speed one year passes per second.
"""

SPEEDS = [1, 2, 4]
BASE_SECONDS_PER_YEAR = 1.0


class SimClock:
    def __init__(self):
        self.paused = True          # start paused so the player can look around
        self.speed = 1
        self._accum = 0.0

    def toggle_pause(self):
        self.paused = not self.paused

    def set_speed(self, speed):
        if speed in SPEEDS:
            self.speed = speed

    def update(self, dt_seconds):
        """Return how many simulation ticks should run this frame."""
        if self.paused:
            return 0
        self._accum += dt_seconds * self.speed
        ticks = int(self._accum / BASE_SECONDS_PER_YEAR)
        self._accum -= ticks * BASE_SECONDS_PER_YEAR
        return ticks

    @property
    def label(self):
        return "PAUSED" if self.paused else f"{self.speed}x"
