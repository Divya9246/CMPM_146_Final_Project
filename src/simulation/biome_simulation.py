from src.world.world_grid import World
from src.simulation import climate
from src.simulation import environmental_rules
from src.simulation import cellular_automata
from src.core.constants import(WATER,GRASSLAND,FOREST,DESERT)


def initialize_environment(world):
    for row in world.grid: #calculates water
        for cell in row:
            cell.biome = environmental_rules.calculate_biomeType(cell)
    for row in world.grid: #calculates temperature
        for cell in row:
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid: #calculates moisture
        for cell in row: 
            cell.moisture = climate.calculate_moisture(cell,world)
    for row in world.grid: #calculates the biome type
        for cell in row:
            cell.biome = environmental_rules.calculate_biomeType(cell)
    return 

def simulate_year(world):
    for row in world.grid:
        for cell in row:
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid:
        for cell in row: 
            cell.moisture = climate.calculate_moisture(cell,world)
    cellular_automata.biome_spread(world)
    return