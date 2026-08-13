# since I dont know what the thing storing the world actually looks like just using pseudoceopde

#get_moisture 
#where mositure 

'''
moisture (precipitation) is a function of height and temperature 

'''

'''
where cell is an entry in the matrix
returns the moisture level of that cell
get_moisture(cell):
    return cell.moisture
'''

#get_temperature
'''
where cell is an entry in the matrix
returns the temperature level of that cell
get_temperature(cell):
    return cell.temperature
'''

#set_moisture
'''
setts the moisture in a cell
where cell is an entry in the matrix
moisture level is the level of mositure in that cell 0-1
returns nothing
set_moisture(cell,moisture_lvl):
    cell.moisture = moisture_lvl
    return 
'''


#set_temperature
'''
sets the temperature in a cell
where cell is an entry in the matrix
temperature level is the level of temperature in that cell 0-1
returns nothing
set_temperature(cell,temperature_lvl):
    cell.temperature = temperature_lvl
    return 
'''

#calculate_temperature (as a function of height with a little bit of randomness )
'''
calculates the temperature in a cell as a function of height
where cell is an entry in the matrix 
returns the calculated temperature 
calculate_temperature(cell):
    height = cell.height (assuming 0-1)
    randomness_scalar = 0.05
    base_temperature = (1-height)
    random_temperature = randomness_scalar*base_temperature
    random_number = 0 or 1
    if(random_number):
        random_temperature = random_temperature*-1

    new_temperature = base_temperature+random_temperature
    if(new_temperature<0):
        new_temperature = 0
    if(new_temperature>1):
        new_temperature = 1
    return new_temperature
'''

#calculate_moisture (as a function of height and temperture and proximity to ocean and with a little bit of randomness )
'''
calculates the moisture in a cell as a function of height and temperature 
where cell is an entry in the matrix 
returns the calculated moisture 
calculate_moisture(cell):
    height = cell.height (assuming 0-1)
    temperature = cell.temperature
    randomness_scalar = 0.05
    proximity_to_ocean = closest_ocean(cell) (1-(closest ocean euclidan distantance / farthest tile euclidian distnace ))
            #maybe ocean proximity can be stored within a cell and only recalculated when an ocean is created or destroyed
    base_moisture = 0.2*(height)+0.3*(1-temperature)+0.5*(proximity_to_ocean)
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