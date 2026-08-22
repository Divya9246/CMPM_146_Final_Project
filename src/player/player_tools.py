# Player tools. These actually change a cell, then tell history what happened.
from src.core.event_bus import event_bus
from src.core.constants import WATER, FOREST, GRASSLAND

# Same numbers Chloe/Saurav already use. Copied here so we do not edit shared constants.
WATER_HEIGHT_MAX = 25.0
FOREST_MOISTURE_MIN = 55.0
RISKY_MOISTURE_MIN = 40.0


def _location(cell):
    return (cell.x, cell.y)


def _touch_food(cell):
    # Saurav's cells can recount food after the biome changes.
    if hasattr(cell, "compute_food"):
        cell.compute_food()


def preview_plant_forest(cell):
    """
    green = good place
    yellow = allowed but risky
    red = blocked or very poor
    """
    if cell.biome == WATER or getattr(cell, "height", 100) < WATER_HEIGHT_MAX:
        return {"level": "red", "blocked": True, "reason": "Cannot plant forest on water."}
    if cell.biome == FOREST:
        return {"level": "red", "blocked": True, "reason": "This cell is already forest."}
    if cell.moisture >= FOREST_MOISTURE_MIN:
        return {"level": "green", "blocked": False, "reason": "Climate looks good for forest."}
    if cell.moisture >= RISKY_MOISTURE_MIN:
        return {"level": "yellow", "blocked": False, "reason": "Borderline climate. Forest may struggle later."}
    return {"level": "red", "blocked": False, "reason": "Very dry. You can still try, but it may not last."}


def preview_deforest(cell):
    if cell.biome != FOREST:
        return {"level": "red", "blocked": True, "reason": "There is no forest here to remove."}
    return {"level": "green", "blocked": False, "reason": "This forest can be cleared."}


def preview_place_settlement(cell):
    if cell.biome == WATER or getattr(cell, "height", 100) < WATER_HEIGHT_MAX:
        return {"level": "red", "blocked": True, "reason": "Cannot place a settlement on water."}
    if getattr(cell, "settlement", None) is not None:
        return {"level": "red", "blocked": True, "reason": "A settlement is already here."}
    if cell.biome == FOREST and cell.moisture >= FOREST_MOISTURE_MIN:
        return {"level": "green", "blocked": False, "reason": "This area looks livable."}
    if cell.biome == GRASSLAND:
        return {"level": "yellow", "blocked": False, "reason": "Okay, but resources may be weaker."}
    return {"level": "red", "blocked": False, "reason": "Harsh land. Allowed, but a settlement may struggle."}


def plant_forest(cell, year=0):
    preview = preview_plant_forest(cell)
    if preview["blocked"]:
        return {"ok": False, "message": preview["reason"]}

    cell.biome = FOREST
    # Tiny local boost only. This does not invent a new climate.
    cell.moisture = min(100.0, cell.moisture + 5)
    _touch_food(cell)

    event_bus.emit("PLAYER_PLANTED_FOREST", {
        "cell": cell,
        "year": year,
        "location": _location(cell),
        "cause": "player",
        "description": f"The player planted forest at ({cell.x}, {cell.y}).",
    })
    return {"ok": True, "message": "Forest planted."}


def deforest(cell, year=0):
    preview = preview_deforest(cell)
    if preview["blocked"]:
        return {"ok": False, "message": preview["reason"]}

    cell.biome = GRASSLAND
    # Trees were holding a little moisture. Clearing them dries the cell a bit.
    cell.moisture = max(0.0, cell.moisture - 8)
    _touch_food(cell)

    event_bus.emit("PLAYER_DEFORESTED", {
        "cell": cell,
        "year": year,
        "location": _location(cell),
        "cause": "player",
        "description": f"The player removed forest at ({cell.x}, {cell.y}).",
    })
    return {"ok": True, "message": "Forest cleared."}


def place_settlement(cell, year=0):
    preview = preview_place_settlement(cell)
    if preview["blocked"]:
        return {"ok": False, "message": preview["reason"]}

    # Placeholder until Aaron puts his Settlement object in this same field.
    cell.settlement = {"placed_by": "player"}
    _touch_food(cell)

    event_bus.emit("PLAYER_PLACED_SETTLEMENT", {
        "cell": cell,
        "year": year,
        "location": _location(cell),
        "cause": "player",
        "description": f"A settlement was founded at ({cell.x}, {cell.y}).",
    })
    return {"ok": True, "message": "Settlement placed."}