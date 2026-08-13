# import climate.py
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
returns the biome type of cell 
get_biomeType(cell):
    return cell.biome
'''


'''
determines the biome type based on the cell 
set_biomeType(cell,biome_type):
    cell.biome = biome_type
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
helper function

returns true if above the threshold, false if otherwise 
no hysteresis version 
check_highTemperature(cell):
    temperature = cell.temperature
    if(temperature>=0.5):
        return True
    return false 

'''
'''
helper function

returns true if above the threshold, false if otherwise 
no hysteresis version 
check_highMoisture(cell):
    Moisture = cell.Moisture
    if(Moisture>=0.5):
        return True
    return false 

'''

'''
helper function

returns true if above the threshold, false if otherwise 
hysteresis version 
check_highTemperature_H(cell):
    temperature = cell.temperature
    if(temperature>=0.55):
        return_value = True
    elif(temperature<=0.45):
        return_value = False
    else                                              #((temperature>0.45) and(temperature<0.55))):
        return cell.temperature_state (True or false)
    cell.temperature_state =  return_value
    return cell.temperature_state

'''

'''
helper function

returns true if above the threshold, false if otherwise 
hysteresis version 
check_highmoisture_H(cell):
    moisture = cell.moisture
    if(moisture>=0.55):
        return_value = True
    elif(moisture<=0.45):
        return_value = False
    else                                              #((moisture>0.45) and(moisture<0.55))):
        return cell.moisture_state (True or false)
    cell.moisture_state =  return_value
    return cell.moisture_state

'''

