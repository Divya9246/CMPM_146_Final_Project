# Simple end-of-demo numbers. Not a science report.


def summarize_planet(world, events):
    events = events or []
    player_actions = [e for e in events if str(e.event_type).startswith("PLAYER_")]
    migrations = [e for e in events if e.event_type == "SETTLEMENT_MIGRATED"]
    collapses = [e for e in events if e.event_type == "SETTLEMENT_COLLAPSED"]

    biome_counts = {}
    year = 0
    if world is not None:
        year = getattr(world, "year", 0)
        if hasattr(world, "count_biomes"):
            biome_counts = world.count_biomes()

    return {
        "year": year,
        "forest": biome_counts.get("forest", 0),
        "desert": biome_counts.get("desert", 0),
        "grassland": biome_counts.get("grassland", 0),
        "water": biome_counts.get("water", 0),
        "player_interventions": len(player_actions),
        "migrations": len(migrations),
        "collapses": len(collapses),
    }


def format_summary(summary):
    return (
        f"Year {summary['year']}: "
        f"forest {summary['forest']}, desert {summary['desert']}, "
        f"player actions {summary['player_interventions']}, "
        f"migrations {summary['migrations']}."
    )