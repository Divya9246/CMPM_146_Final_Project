from src.world.world_grid import World
from src.simulation import climate
from src.simulation import environmental_rules
from src.simulation import cellular_automata
from src.core.constants import(WATER,GRASSLAND,FOREST,DESERT)

import random
import time

#for visualization so can comment out 
import matplotlib.pyplot as plt
biome_values = {
    WATER: 0,
    GRASSLAND: 1,
    FOREST: 2,
    DESERT: 3
}

wait_time = 20

def main():
    print("Echo Earth")
    print("simulation_test")
    print("Project initialized successfully.")
    print("Initializing world")
    #random.seed(123)
    world = World()
    

    # randomize world
    for row in world.grid:
        for cell in row:
            cell.height = random.randint(0, 50)
    for row in world.grid:
        for cell in row:
            cell.biome = environmental_rules.calculate_biomeType(cell)
    for row in world.grid:
        for cell in row:
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
    for row in world.grid:
        for cell in row: 
            cell.moisture = climate.calculate_moisture(cell,world)
    for row in world.grid:
        for cell in row:
            cell.biome = environmental_rules.calculate_biomeType(cell)
    
    
    #printing the hieght map
    for row in world.grid: 
        for cell in row:
            print(f"{cell.height:5.1f}", end=" ")
        print()

    print("printing temperature")
    for row in world.grid:
            for cell in row:
                print(f"{cell.temperature:5.1f}", end=" ")
            print()
    
    print("printing moisture")
    for row in world.grid:
            for cell in row:
                 print(f"{cell.moisture:5.1f}", end="")
            print()

    print("printing water")
    for row in world.grid:
            for cell in row:
                if(cell.biome == WATER):
                    print("W", end=" ")
                elif(cell.biome == GRASSLAND):
                    print("G", end=" ")
                elif(cell.biome == FOREST):
                    print("F", end=" ")
                else:
                    print("D", end=" ")
            print()
    i = 0
    # while(True):
    #     print(f"{i}th Year ---------------------------------------")
    #     cellular_automata.biome_spread(world)
    #     for row in world.grid:
    #             for cell in row:
    #                 if(cell.biome == WATER):
    #                     print("W", end="")
    #                 elif(cell.biome == GRASSLAND):
    #                     print("G", end="")
    #                 elif(cell.biome == FOREST):
    #                     print("F", end="")
    #                 else:
    #                     print("D", end="")
    #             print()
    #     i+=1
    #     time.sleep(wait_time)

    #for visualization 
    plt.ion()

    i = 0
    while True:
        print(f"{i}th Year ---------------------------------------")
        print(f"{world.count_biomes()}")
        for row in world.grid:
            for cell in row:
                cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for wate
        for row in world.grid:
            for cell in row: 
                cell.moisture = climate.calculate_moisture(cell,world)
        

        cellular_automata.biome_spread(world)

        visual_grid = []

        for row in world.grid:
            visual_row = []

            for cell in row:
                visual_row.append(biome_values[cell.biome])

            visual_grid.append(visual_row)

        plt.clf()
        plt.imshow(visual_grid)
        plt.title(f"Year {i}")
        plt.pause(1)

        i += 1
                

if __name__ == "__main__":
    main()