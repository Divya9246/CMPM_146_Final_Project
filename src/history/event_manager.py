from src.history.world_event import WorldEvent


class EventManager:
    def __init__(self):
        self.events = []

    def record(self, event: WorldEvent):
        self.events.append(event)

    def get_all_events(self):
        return list(self.events)

    def clear(self):
        self.events.clear()