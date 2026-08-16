#updates based on the surrounding cells and local 
# (climate of surrounding cell)*0.3 + (climate of cell)*0.7
#updates the climate of the cell 

#neighbors influence each others climate
from src.core.constants import(MAX_TEMPERATURE,MAX_MOISTURE,WATER,GRASSLAND,FOREST,DESERT)
from src.simulation.environmental_rules import(calculate_biomeType)

#neighbors influence the biome spread 
    #find neighbors of cell
    #count majority 
        #if no majority let python pick one
    #is the cell the correct climate for the majority?
        #yes->change biome
        #no->keep biome
    #only apply all changes at the end

def biome_spread(world):
    new_biomes = []
    for row in world.grid:
        for cell in row:
            cell_neighbors = world.get_neighbors(cell.x,cell.y)
            neighbor_biomes = []
            for neighbor in cell_neighbors:
                neighbor_biomes.append(neighbor.biome)
            target_biome = max(set(neighbor_biomes), key=neighbor_biomes.count)
            if (valid_spreadBiome(cell,target_biome)):
                new_biomes.append(target_biome)
            else:
                new_biomes.append(cell.biome)
    i = 0
    for row in world.grid:
        for cell in row:
            cell.biome = new_biomes[i]
            i+=1
    return


    

#returns true if the cell is a valid change to the target biome
#the cell's biome shouldnt be the target biome
def valid_spreadBiome(cell,target_biome):
    #biome =environmental_rules.calculate_biomeType(cell)
    if(cell.biome == target_biome):
        return False
    biome =calculate_biomeType(cell)
    if((target_biome == biome)):
        return True
    else:
        return False
    return False
    

    
