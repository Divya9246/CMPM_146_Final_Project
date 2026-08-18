# since I dont know what the thing storing the world actually looks like just using pseudoceopde

#get_moisture 
#where mositure 
from src.core.constants import *
import random
#defines
MIN_RANDOMNESS_SCALAR = 0.05
MAX_RANDOMNESS_SCALAR = 0.15
MAX_DISTANCE = 10
'''
moisture (precipitation) is a function of height and temperature 
'''

# for the simulation
#calculate_temperature (as a function of height with a little bit of randomness )
# where cell is a cell in the world
# returns the new temperature of the cell
def calculate_temperature(cell): 
    height = cell.height #0-50
    original_temperature = cell.temperature
    latitude_factor = 1.0 - (cell.y / WORLD_HEIGHT) * TEMP_LATITUDE_FACTOR    
    normalized_height = height/WORLD_HEIGHT
    base_temperature = (1 - normalized_height)*100
    random_temperature = random.uniform(MIN_RANDOMNESS_SCALAR,MAX_RANDOMNESS_SCALAR)*base_temperature
    random_number = random.randint(0,1)
    if(random_number):
        random_temperature = random_temperature*-1
    target_temperature = (base_temperature*latitude_factor+random_temperature)
    new_temperature = (0.9)*original_temperature+target_temperature*(0.1)
    if(new_temperature<MIN_TEMPERATURE):
        new_temperature = MIN_TEMPERATURE
    if(new_temperature>MAX_TEMPERATURE):
        new_temperature = MAX_TEMPERATURE
    return new_temperature

#calculate moisture (as a function of height and proximity to "water", and temperature)
# where cell is a cell in the world
# returns the new moisture of the cell

'''
 height = cell.height #0-50
original_temperature = cell.temperature
latitude_factor = 1.0 - (cell.y / WORLD_HEIGHT) * TEMP_LATITUDE_FACTOR    
normalized_height = height/MAX_TERRAIN_HEIGHT
base_temperature = (1 - normalized_height)*100
random_temperature = random.uniform(MIN_RANDOMNESS_SCALAR,MAX_RANDOMNESS_SCALAR)*base_temperature
random_number = random.randint(0,1)
if(random_number):
    random_temperature = random_temperature*-1
target_temperature = (base_temperature*latitude_factor+random_temperature)
new_temperature = (0.9)*original_temperature+target_temperature*(0.1)
if(new_temperature<MIN_TEMPERATURE):
    new_temperature = MIN_TEMPERATURE
if(new_temperature>MAX_TEMPERATURE):
    new_temperature = MAX_TEMPERATURE
return new_temperature
'''
def calculate_moisture(cell,World): 
    height = cell.height #0-50
    temperature = cell.temperature
    base_moisture = cell.moisture
    normalized_height = height/WORLD_HEIGHT
    normalized_temperature = temperature/MAX_TEMPERATURE
    closness_to_water = proximity_to_water(cell,World)
    random_moisture = random.uniform(MIN_RANDOMNESS_SCALAR,MAX_RANDOMNESS_SCALAR)*base_moisture/MAX_MOISTURE
    random_number = random.randint(0,1)
    number_of_nearby_forest = 0 
    neighbors = World.get_neighbors(cell.x,cell.y)
    for neighbor in neighbors:
        if(neighbor.biome == FOREST):
            number_of_nearby_forest+=1
    ratio_of_forest = number_of_nearby_forest/len(neighbors)
    if(random_number):
        random_moisture = random_moisture*-1
    target_moisture = ((0.1)*normalized_height+(0.1)*(1-normalized_temperature)+(0.5)*closness_to_water+(0.15)*random_moisture+(0.15)*ratio_of_forest)*MAX_MOISTURE
    new_moisture = 0.9*base_moisture+0.1*target_moisture
    if(new_moisture<MIN_MOISTURE):
        new_moisture = MIN_MOISTURE
    if(new_moisture>MAX_MOISTURE):
        new_moisture = MAX_MOISTURE
    return new_moisture

#calculate_moisture (as a function of height and temperture and proximity to water and with a little bit of randomness )
'''
calculates the moisture in a cell as a function of height and temperature 
where cell is an entry in the matrix 
returns the calculated moisture 
calculate_moisture(cell):
    height = cell.height (assuming 0-1)
    temperature = cell.temperature
    randomness_scalar = 0.05
    proximity_to_water = closest_water(cell) (1-(closest water euclidan distantance / farthest tile euclidian distnace ))
            #maybe water proximity can be stored within a cell and only recalculated when an water is created or destroyed
    base_moisture = 0.2*(height)+0.3*(1-temperature)+0.5*(proximity_to_water)
    random_moisture = randomness_scalar*base_moisture
    random_number = 0 or 1
    if(random_number):
        random_moisture = random_moisture*-1

    new_moisture = base_moisture+random_moisture
    if(new_moisture<0):
        new_moisture = 0
    if(new_moisture>1):
        new_moisture = 1
    
    return new_moisture
'''

'''
helper functions
'''
#calculates closest euclidean distance from target_cell to world 
#(1-(closest water euclidan distantance / farthest tile euclidian distnace ))
#if target cell is water return 1 
#if no water and target cell is not water retun
def proximity_to_water(target_cell, world):
    if(target_cell.biome == WATER):
        return 1
    x1 = target_cell.x
    y1 = target_cell.y
    smallest_distance = None
    for row in world.grid:
        for cell in row:
            if(cell == target_cell):
                continue
            x2 = cell.x
            y2 = cell.y
            distance = ((x2-x1)**2+(y2-y1)**2)**0.5
            if((smallest_distance == None) and (cell.biome == WATER)):
                smallest_distance = distance
            if((cell.biome == WATER)and(distance < smallest_distance)):
                smallest_distance = distance
    if(smallest_distance == None):
        return 0
    if(smallest_distance >= MAX_DISTANCE):
        return 0
    return (1-(smallest_distance/MAX_DISTANCE))
                    
                