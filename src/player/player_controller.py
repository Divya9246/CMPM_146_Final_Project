# Remembers which tool is selected and what the player last clicked.
from src.player.player_tools import (
    plant_forest,
    deforest,
    place_settlement,
    preview_plant_forest,
    preview_deforest,
    preview_place_settlement,
)


class PlayerController:
    def __init__(self, world=None):
        self.world = world
        self.selected_tool = "plant_forest"
        self.selected_cell = None
        self.last_message = ""
        self.last_preview = None

    def set_tool(self, name):
        allowed = ("plant_forest", "deforest", "place_settlement")
        if name not in allowed:
            self.last_message = "Unknown tool."
            return
        self.selected_tool = name
        self.last_message = f"Selected tool: {name}"

    def _year(self):
        if self.world is not None:
            return getattr(self.world, "year", 0)
        return 0

    def preview(self, cell):
        if self.selected_tool == "plant_forest":
            return preview_plant_forest(cell)
        if self.selected_tool == "deforest":
            return preview_deforest(cell)
        return preview_place_settlement(cell)

    def click_cell(self, cell):
        self.selected_cell = cell
        preview = self.preview(cell)
        self.last_preview = preview

        if preview["blocked"]:
            self.last_message = preview["reason"]
            return {"ok": False, "message": preview["reason"], "preview": preview}

        year = self._year()
        if self.selected_tool == "plant_forest":
            result = plant_forest(cell, year)
        elif self.selected_tool == "deforest":
            result = deforest(cell, year)
        else:
            result = place_settlement(cell, year)

        self.last_message = result["message"]
        result["preview"] = preview
        return result