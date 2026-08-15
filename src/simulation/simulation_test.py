from src.world.world_grid import World
from src.simulation import climate
from src.simulation import environmental_rules
from src.core.constants import(WATER,GRASSLAND,FOREST,DESERT)

import random

def main():
    print("Echo Earth")
    print("simulation_test")
    print("Project initialized successfully.")
    print("Initializing world")
    random.seed(123)
    world = World()
    

    # randomize world
    for row in world.grid:
        for cell in row:
           
            cell.height = random.randint(0, 50)
            cell.biome = environmental_rules.calculate_biomeType(cell)
            cell.temperature = climate.calculate_temperature(cell) #seems to work, maybe create different calculate temperature but for water 
            cell.moisture = climate.calculate_moisture(cell,world)
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
    


if __name__ == "__main__":
    main()