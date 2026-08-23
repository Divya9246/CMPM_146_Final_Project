from src.simulation import climate
from src.simulation import cellular_automata
from src.core.constants import(WATER,GRASSLAND,FOREST,DESERT,MAX_TEMPERATURE,MAX_MOISTURE,MIN_TEMPERATURE,MIN_MOISTURE)
from src.core.event_bus import(event_bus)
import random

year_counter = 0
def simulate_year(world):
    global year_counter
    if(year_counter != 0):
         year_counter -= 1
    for row in world.grid:
        for cell in row:
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid:
        for cell in row: 
            cell.moisture = climate.calculate_moisture(cell,world)

    #determine climate event
    #chance of climate event 
    climate_event_chance = random.uniform(0.1,0.25)
    chance = random.uniform(0.0,1.0)
    if(year_counter == 0):
        if(chance<climate_event_chance):
            year_counter = random.randint(5,15)
            chance = random.uniform(0.0,1.0)
            if(chance>0.6):
                heavy_rain(world)
            else: 
                heat_wave(world)

    biome_count_before = world.count_biomes()
    cellular_automata.biome_spread(world)
    biome_count_after = world.count_biomes()
    # P5 INTEGRATION PATCH — was `> before`, which fired nearly every year and
    # flooded the history panel. Now only reports meaningful expansions.
    # — Winston (P5). P2 please review / tune the threshold.
    if biome_count_after.get(DESERT, 0) >= biome_count_before.get(DESERT, 0) + 5:
        event_bus.emit("DESERT_SPREAD", { "year": world.year, "cause": "dry climate", "description": "Desert spread as the land got drier.", })


    
    world.year+=1
    return


def heavy_rain(world):
    print(f"Heavy Rain Event for {year_counter} years")
    # P5 INTEGRATION PATCH — emit so the UI/history can show it, not just the console.
    event_bus.emit("HEAVY_RAIN_STARTED", {
        "year": world.year, "cause": "climate event",
        "description": f"Years of heavy rain began, soaking the land.",
    })
    # for row in world.grid:
    #     for cell in row:
    #         cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid:
        for cell in row: 
            cell.moisture = cell.moisture*1.8+35
            if(cell.moisture<MIN_MOISTURE):
                    cell.moisture = MIN_MOISTURE
            if(cell.moisture>MAX_MOISTURE):
                cell.moisture = MAX_MOISTURE
    for row in world.grid:
        for cell in row: 
            cell.temperature = cell.temperature*0.3+15
            if(cell.temperature<MIN_TEMPERATURE):
                    cell.temperature = MIN_TEMPERATURE
            if(cell.temperature>MAX_TEMPERATURE):
                cell.temperature = MAX_TEMPERATURE
    
    return

def heat_wave(world):
    print(f"Heat Wave Event for {year_counter} years")
    # P5 INTEGRATION PATCH — DROUGHT_STARTED is already in history's LISTEN_TO.
    event_bus.emit("DROUGHT_STARTED", {
        "year": world.year, "cause": "climate event",
        "description": f"A heat wave gripped the planet, drying the land.",
    })
    for row in world.grid:
        for cell in row: 
            cell.temperature = cell.temperature*1.5+50
            if(cell.temperature<MIN_TEMPERATURE):
                    cell.temperature = MIN_TEMPERATURE
            if(cell.temperature>MAX_TEMPERATURE):
                cell.temperature = MAX_TEMPERATURE
    for row in world.grid:
            for cell in row: 
                cell.moisture = cell.moisture*0.3
                if(cell.moisture<MIN_MOISTURE):
                    cell.moisture = MIN_MOISTURE
                if(cell.moisture>MAX_MOISTURE):
                    cell.moisture = MAX_MOISTURE
    return