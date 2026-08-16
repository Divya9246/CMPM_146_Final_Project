from src.simulation import climate
from src.simulation import cellular_automata
from src.core.constants import(WATER,GRASSLAND,FOREST,DESERT)


def simulate_year(world):
    for row in world.grid:
        for cell in row:
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid:
        for cell in row: 
            cell.moisture = climate.calculate_moisture(cell,world)
    cellular_automata.biome_spread(world)
    return