from src.world.world_grid import World
from src.core.constants import WATER, GRASSLAND, FOREST, DESERT

from src.simulation.biome_simulation import simulate_year

from ursina import Ursina, EditorCamera, invoke

from src.world.terrain_generator import generate_world
from src.world.biome_renderer import build_terrain, update_cell_visual
from src.simulation.environmental_rules import calculate_biomeType
import random

YEAR_DELAY = 3


def main():
    print("Echo Earth")
    print("simulation_test")
    print("Project initialized successfully.")
    print("Initializing world")

    app = Ursina()

    # Generate Saurav's initial world
    random_seed = random.randint(1,999)
    world = World(seed=random_seed)
    generate_world(world, random_seed)

    print("printing temperature")
    for row in world.grid:
        for cell in row:
            print(f"{cell.temperature:5.1f}", end="")
        print()

    print("printing environment")
    for row in world.grid:
        for cell in row:
            if cell.biome == WATER:
                print("W", end=" ")
            elif cell.biome == GRASSLAND:
                print("G", end=" ")
            elif cell.biome == FOREST:
                print("F", end=" ")
            else:
                print("D", end=" ")
        print()

    # Build initial 3D world
    build_terrain(world)

    EditorCamera()

    year = 0

    def run_year():
        nonlocal year

        print(f"Year {year}")
        print(world.count_biomes())
        ideal_counts = {
            WATER: 0,
            GRASSLAND: 0,
            FOREST: 0,
            DESERT: 0
        }

        for row in world.grid:
            for cell in row:
                ideal_biome = calculate_biomeType(cell)
                ideal_counts[ideal_biome] += 1

        print("Climate suitability:", ideal_counts)
        print("Actual biomes:", world.count_biomes())

        simulate_year(world)
        for row in world.grid:
            for cell in row:
                update_cell_visual(cell)
        
        

        year += 1

        invoke(run_year, delay=YEAR_DELAY)

    invoke(run_year, delay=YEAR_DELAY)

    app.run()


if __name__ == "__main__":
    main()