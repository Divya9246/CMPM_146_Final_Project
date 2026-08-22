# Saves important world changes. Ignore tiny yearly noise.
from src.core.event_bus import event_bus
from src.history.world_event import WorldEvent

LISTEN_TO = (
    "PLAYER_PLANTED_FOREST",
    "PLAYER_DEFORESTED",
    "PLAYER_PLACED_SETTLEMENT",
    "DROUGHT_STARTED",
    "HEAVY_RAIN_STARTED",  # P5 integration: P2's heavy-rain climate event
    "DESERT_SPREAD",
    "FOREST_DIED",
    "SETTLEMENT_GREW",
    "SETTLEMENT_DECLINED",
    "SETTLEMENT_MIGRATED",
    "SETTLEMENT_COLLAPSED",
)


class EventManager:
    def __init__(self):
        self.events = []
        self._connected = False

    def connect(self):
        if self._connected:
            return
        for name in LISTEN_TO:
            event_bus.subscribe(name, self._make_handler(name))
        self._connected = True

    def _make_handler(self, event_type):
        def handler(data):
            self._save(event_type, data or {})
        return handler

    def _save(self, event_type, data):
        cell = data.get("cell")
        location = data.get("location")
        if location is None and cell is not None:
            location = (cell.x, cell.y)

        description = data.get("description")
        if not description:
            description = f"{event_type} at {location}."

        self.record(WorldEvent(
            year=int(data.get("year", 0)),
            event_type=event_type,
            description=description,
            location=location,
            cause=data.get("cause"),
            data=data,
        ))

    def record(self, event: WorldEvent):
        self.events.append(event)

    def get_all_events(self):
        return list(self.events)

    def clear(self):
        self.events.clear()