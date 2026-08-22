from src.core.constants import *
'''
biome_set = {
Water
Grassland
Forest
Desert
}
'''
'''

                temperature, moisture 
                0 -> temperature<0.5
                0 -> moisture<0.5
                1 -> temperature>=0.5
                1 -> moisture>=0.5

                maybe add hysteresis bound?

                
                0 -> temperature<0.45
                0 -> moisture<0.45
                1 -> temperature>=0.55
                1 -> moisture>=0.55
                retain same  temperature state  if temperature>0.45 and  temperature<0.55
                retain same  moisture    state  if moisture>0.45 and  moisture<0.55

                if height < water height level:
                    water 
                else 
                temperature, moisture,  biome 
                0            0          Grassland
                0            1          Forest
                1            0          Desert
                1            1          Forest

'''


'''
calcualtes the type of biome that a cell should be based on the bioclimatic variablse 
returns the biome that the cell should turn into 
calculate_biomeType(cell):
    temperature_state = check_highTemperature(cell)
    moisture_state =check_highMoisture(cell)
    truth_values = [temperature_state,moisture_state]
    height = cell.height

    if(height =< water height threshold):
        biome_type = water
    elif(truth_values == [0,0]):
        biome_type = Grassland
    elif(truth_values == [0,1]):
        biome_type = Forest
    elif(truth_values == [1,0]):
        biome_type = Desert
    elif(truth_values == [1,1]):
        biome_type = Forest
    else: # shld never happen though
         biome_type = Grassland
    return biome_type
'''

'''
WATER_HEIGHT_MAX = 25.0          
DESERT_MOISTURE_MAX = 25.0        
FOREST_MOISTURE_MIN = 55.0        
'''

def calculate_biomeType(cell):
    height_val = cell.height
    temperature_val = cell.temperature
    moisture_val = cell.moisture
    if height_val < WATER_HEIGHT_MAX:
        return WATER
    if ((moisture_val > FOREST_MOISTURE_MIN) and (temperature_val < FOREST_TEMPERATURE_MAX)):
        return FOREST
    # if ((moisture_val < DESERT_MOISTURE_MAX) and (temperature_val > DESERT_TEMPERATURE_MIN)):
    #     return DESERT
    if ((moisture_val < DESERT_MOISTURE_MAX)):
        return DESERT
    return GRASSLAND