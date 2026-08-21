# tuning values for the settlement AI
# keeping these here instead of core/constants.py so we dont get merge conflicts

# how far a settlement farms/reads around itself
SETTLEMENT_RADIUS = 2
WATER_ADJACENCY_BONUS = 30.0   # bonus for having a water tile nearby

# population
STARTING_POPULATION = 50
MAX_POPULATION = 500
MIN_POPULATION = 10            # below this = collapse
GROWTH_RATE = 0.10
DECLINE_RATE = 0.12

# thresholds, same 0-100 scale as cell.food / cell.moisture
GOOD_FOOD = 45.0
GOOD_WATER = 40.0
BAD_FOOD = 30.0
BAD_WATER = 25.0
CRITICAL_FOOD = 20.0
CRITICAL_WATER = 15.0

# migration
MIGRATION_PATIENCE = 3            # bad years in a row before leaving
MIGRATION_SEARCH_RADIUS = 8
MIGRATION_MIN_IMPROVEMENT = 10.0  # new spot has to be actually better, not marginal

# states
STATE_GROWING = "growing"
STATE_STABLE = "stable"
STATE_DECLINING = "declining"
STATE_COLLAPSED = "collapsed"

# event names divya's history listens for
SETTLEMENT_CREATED = "SETTLEMENT_CREATED"
SETTLEMENT_GREW = "SETTLEMENT_GREW"
SETTLEMENT_DECLINED = "SETTLEMENT_DECLINED"
SETTLEMENT_MIGRATED = "SETTLEMENT_MIGRATED"
SETTLEMENT_COLLAPSED = "SETTLEMENT_COLLAPSED"