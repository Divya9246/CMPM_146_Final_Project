# Echo Earth

Echo Earth is an interactive procedurally generated world where biomes evolve over time, players can intervene in the environment, settlements react to environmental changes, and important events become part of the world's history.

# Core Loop

World Generation
- Biome Evolution
- Player Intervention
- Environmental Consequences
- Settlement AI Reaction
- World Memory / History


The MVP includes:

- Procedurally generated terrain
- Four main biomes:
  - Water
  - Grassland
  - Forest
  - Desert
- Cellular-automata-based biome evolution
- Player actions:
  - Plant Forest
  - Deforest
  - Place Settlement
- Simple settlement AI
- Environmental consequences
- Event memory system
- History of the Planet

# Team Ownership

# Person 1 - World Generation

Owns:

`src/world/`

Responsibilities:

- Terrain generation
- Perlin noise
- Height/elevation map
- World grid
- Initial biome placement
- Terrain visualization

# Person 2 — Environment Simulation

Owns:

`src/simulation/`

Responsibilities:

- Cellular automata
- Forest spreading
- Desert spreading
- Moisture
- Temperature
- Environmental rules
- Environmental consequences

# Person 3 — Settlement AI

Owns:

`src/agents/`

Responsibilities:

- Settlement creation
- Population
- Food
- Water
- Behavior Tree / FSM
- Growth
- Decline
- Migration

# Person 4 — Player + History

Owns:

`src/player/`

`src/history/`

Responsibilities:

- Player tools
- Plant Forest
- Deforest
- Place Settlement
- Event system
- World memory
- Planet history
- History UI

# Shared

Shared files and folders include:

`src/core/`

`src/ui/`

`tests/`

`main.py`
