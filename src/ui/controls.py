"""P5 — player tools and input mapping, wired to P4's PlayerController.

P4's code is the authority on what actions are allowed and what they change.
This module just translates between UI labels/keys and P4's tool names, and
maps P4's green/yellow/red preview levels onto hover-outline colors.
"""
import pygame

PLANT = "Plant Forest"
DEFOREST = "Deforest"
SETTLE = "Place Settlement"
TOOLS = [PLANT, DEFOREST, SETTLE]

# UI label -> P4's internal tool name (src/player/player_controller.py)
P4_TOOL_NAMES = {
    PLANT: "plant_forest",
    DEFOREST: "deforest",
    SETTLE: "place_settlement",
}

# P4's preview levels -> outline quality used by map_view
LEVEL_TO_QUALITY = {"green": "good", "yellow": "risky", "red": "bad"}

TOOL_KEYS = {pygame.K_f: PLANT, pygame.K_d: DEFOREST, pygame.K_s: SETTLE}
SPEED_KEYS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 4}


def preview(game, tool, cell):
    """Return (quality, reason) for hover feedback, straight from P4."""
    if cell is None or tool is None:
        return None, ""
    game.player.set_tool(P4_TOOL_NAMES[tool])
    p = game.player.preview(cell)
    return LEVEL_TO_QUALITY.get(p["level"]), p["reason"]


def apply_tool(game, tool, cell):
    """Run the armed tool through P4's controller.

    Returns (ok, message). P4 blocks invalid actions itself.
    """
    game.player.set_tool(P4_TOOL_NAMES[tool])
    result = game.player.click_cell(cell)
    return result["ok"], result["message"]
