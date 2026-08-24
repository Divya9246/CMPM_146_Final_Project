# Turns saved events into short story lines for the History panel.


class HistoryGenerator:
    def generate(self, events):
        lines = []
        seen_settlement = False
        seen_deforest = False

        for event in events:
            title = None
            if event.event_type == "PLAYER_PLACED_SETTLEMENT" and not seen_settlement:
                title = "The First Settlement"
                seen_settlement = True
            elif event.event_type == "PLAYER_DEFORESTED" and not seen_deforest:
                title = "The Great Clearing"
                seen_deforest = True
            elif event.event_type == "DROUGHT_STARTED":
                title = "The Heat Wave"
            elif event.event_type == "HEAVY_RAIN_STARTED":
                title = "The Heavy Rains"
            elif event.event_type == "DESERT_SPREAD":
                title = "A Drying Land"
            elif event.event_type == "SETTLEMENT_MIGRATED":
                title = "The Migration"
            elif event.event_type == "SETTLEMENT_COLLAPSED":
                title = "A Lost Home"

            if title:
                lines.append(f"Year {event.year} — {title}: {event.description}")
            else:
                lines.append(f"Year {event.year}: {event.description}")

        return "\n".join(lines)