"""P5 — player tools, action validation, and input handling.

Validation here is UI-level (can the click even make sense, and how good an
idea is it — the green/yellow/red preview from the design deck). P4's real
action code stays the authority on what actually changes in the world; the
UI just calls the functions in src/player/player_tools.py.
"""
import pygame

from src.core.constants import WATER, GRASSLAND, FOREST, DESERT
from src.player import player_tools

PLANT = "Plant Forest"
DEFOREST = "Deforest"
SETTLE = "Place Settlement"
TOOLS = [PLANT, DEFOREST, SETTLE]

TOOL_KEYS = {pygame.K_f: PLANT, pygame.K_d: DEFOREST, pygame.K_s: SETTLE}
SPEED_KEYS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 4}


def preview(world, tool, cell):
    """Return (quality, reason) for using `tool` on `cell`.

    quality is "good" / "risky" / "bad" (slide 22). "bad" actions are blocked.
    """
    if cell is None or tool is None:
        return None, ""

    if tool == PLANT:
        if cell.biome == WATER:
            return "bad", "Can't plant forest in water"
        if cell.biome == FOREST:
            return "bad", "Already forest"
        suit = world.forest_suitability(cell)
        if suit > 0.45:
            return "good", "Climate suits forest well"
        if suit > 0.15:
            return "risky", "Borderline climate — forest may struggle"
        return "risky", "Harsh climate — forest will likely die"

    if tool == DEFOREST:
        if cell.biome != FOREST:
            return "bad", "No forest here to clear"
        return "good", "Forest can be cleared"

    if tool == SETTLE:
        if cell.biome == WATER:
            return "bad", "Can't settle in water"
        if world.settlement_at(cell.x, cell.y):
            return "bad", "A settlement is already here"
        near = world.neighbors(cell)
        has_water = any(n.biome == WATER or n.moisture > 55 for n in near)
        has_food = any(n.biome in (GRASSLAND, FOREST) for n in near)
        if has_water and has_food:
            return "good", "Food and water nearby"
        if has_water or has_food:
            return "risky", "Some resources missing nearby"
        return "risky", "Very poor location — expect a struggle"

    return None, ""


def apply_tool(tool, cell):
    """Fire the P4 player action for the armed tool (bad ones are blocked
    by the caller before we get here)."""
    if tool == PLANT:
        player_tools.plant_forest(cell)
    elif tool == DEFOREST:
        player_tools.deforest(cell)
    elif tool == SETTLE:
        player_tools.place_settlement(cell)
