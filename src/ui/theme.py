"""P5 — shared colors, fonts, and layout constants for the UI.

Keeping every magic number here makes it easy to restyle the game later
without hunting through drawing code.
"""

# ---- window layout -------------------------------------------------------
WINDOW_W = 940
WINDOW_H = 700

HUD_H = 48                      # top bar height
MAP_X, MAP_Y = 10, HUD_H + 10   # map top-left corner
CELL_PX = 12                    # pixel size of one world cell (50 * 12 = 600)
PANEL_X = MAP_X + 50 * CELL_PX + 14   # right-hand info panel
PANEL_W = WINDOW_W - PANEL_X - 10

FPS = 60

# ---- palette -------------------------------------------------------------
BG = (24, 26, 30)
PANEL_BG = (36, 39, 45)
PANEL_BORDER = (70, 75, 84)
TEXT = (230, 232, 235)
TEXT_DIM = (150, 155, 165)
ACCENT = (255, 200, 90)

BIOME_COLORS = {
    "water": (52, 105, 180),
    "grassland": (110, 165, 70),
    "forest": (40, 110, 55),
    "desert": (205, 178, 105),
}

SETTLEMENT_COLOR = (235, 235, 235)
SELECT_COLOR = (255, 255, 255)

# action-preview outline colors (slide 22: green / yellow / red)
PREVIEW_GOOD = (90, 220, 90)
PREVIEW_RISKY = (240, 210, 70)
PREVIEW_BAD = (235, 80, 80)

BTN_BG = (52, 56, 64)
BTN_BG_ACTIVE = (90, 96, 110)
BTN_BORDER = (95, 100, 112)
