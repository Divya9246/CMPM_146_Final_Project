from src.core.event_bus import event_bus


def plant_forest(cell):
    event_bus.emit(
        "PLAYER_PLANTED_FOREST",
        {"cell": cell}
    )


def deforest(cell):
    event_bus.emit(
        "PLAYER_DEFORESTED",
        {"cell": cell}
    )


def place_settlement(cell):
    event_bus.emit(
        "PLAYER_PLACED_SETTLEMENT",
        {"cell": cell}
    )