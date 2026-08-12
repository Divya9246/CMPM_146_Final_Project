class HistoryGenerator:
    def generate(self, events):
        lines = []

        for event in events:
            lines.append(
                f"Year {event.year}: {event.description}"
            )

        return "\n".join(lines)