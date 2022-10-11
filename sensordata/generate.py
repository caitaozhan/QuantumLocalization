'''generate sensor data, sensor is in continuous locations, i.e., not confined at the center of a grid cell
'''

import numpy as np
from plot import Plot
import json
import random
from my_encoder import MyJSONEncoder


def random_sensors(grid_length: int, num_sensor: int):
    all_sensors = [(i, j) for i in range(grid_length+1) for j in range(grid_length+1)]
    random_index = np.random.permutation(len(all_sensors))[:num_sensor]
    selected_sensors = [all_sensors[i] for i in random_index]
    return selected_sensors

########################################################
############### one level, 4 sensors ###################

'''one levels, 4 sensors, 2 by 2 grid'''
def onelevel_2x2grid_4sen(filename, fig_filename):
    grid_len = 2
    sensor_data = {}
    # information
    info = "grid size is 2x2, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 1),
        1: (1, 0),
        2: (1, 2),
        3: (2, 1),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors, 4 by 4 grid'''
def onelevel_4x4grid_4sen(filename, fig_filename):
    grid_length = 4
    sensor_data = {}
    # information
    info = "grid size is 4x4, 4 sensors at 1 levels."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 2),
        1: (2, 0),
        2: (2, 4),
        3: (4, 2)
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors, 6 by 6 grid'''
def onelevel_6x6grid_4sen(filename, fig_filename):
    grid_length = 6
    sensor_data = {}
    # information
    info = "grid size is 4x4, 6 sensors at 1 levels."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (1, 1),
        1: (1, 5),
        2: (5, 1),
        3: (5, 5)
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors in a 8 by 8 grid'''
def onelevel_8x8grid_4sen(filename, fig_filename):
    grid_len = 8
    sensor_data = {}
    # information
    info = "grid size is 8x8, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (1, 4),
        1: (4, 1),
        2: (4, 7),
        3: (7, 4),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors in a 10 by 10 grid'''
def onelevel_10x10grid_4sen(filename, fig_filename):
    grid_len = 10
    sensor_data = {}
    # information
    info = "grid size is 10x10, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (2, 5),
        1: (5, 2),
        2: (5, 8),
        3: (8, 5),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors in a 12 by 12 grid'''
def onelevel_12x12grid_4sen(filename, fig_filename):
    grid_len = 12
    sensor_data = {}
    # information
    info = "grid size is 12x12, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (2, 6),
        1: (6, 2),
        2: (6, 10),
        3: (10, 6),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



'''one level 4 sensors in a 16 by 16 grid'''
def onelevel_16x16grid_4sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 16x16, 4 sensors at 1 levels."
    sensor_data['info'] = info
    # num_sensor = 8
    grid_length = 16
    # selected_sensors = random_sensors(grid_length, num_sensor)
    # sensors = {i: tuple(loc) for i, loc in zip(range(num_sensor), selected_sensors)}
    
    sensors = {
        0: (3, 8),
        1: (8, 3),
        2: (8, 13),
        3: (13, 8),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


#################################################
########## one level, 8 sensors #################


'''one levels, 8 sensors, 2 by 2 grid'''
def onelevel_2x2grid_8sen(filename, fig_filename):
    grid_len = 2
    sensor_data = {}
    # information
    info = "grid size is 2x2, 8 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 0),
        1: (0, 1),
        2: (0, 2),
        3: (1, 0),
        4: (1, 2),
        5: (2, 0),
        6: (2, 1),
        7: (2, 2),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 4 sensors, 4 by 4 grid'''
def onelevel_4x4grid_8sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 4x4, 8 sensors at 1 levels."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 0),
        1: (0, 2),
        2: (0, 4),
        3: (2, 0),
        4: (2, 4),
        5: (4, 0),
        6: (4, 2),
        7: (4, 4)
    }
    grid_length = 4

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 8 sensors, 6 by 6 grid'''
def onelevel_6x6grid_8sen(filename, fig_filename):
    grid_length = 6
    sensor_data = {}
    # information
    info = "grid size is 4x4, 6 sensors at 1 levels."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 3),
        1: (2, 2),
        2: (2, 4),
        3: (3, 0),
        4: (3, 6),
        5: (4, 2),
        6: (4, 4),
        7: (6, 3),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 8 sensors in a 8 by 8 grid'''
def onelevel_8x8grid_8sen(filename, fig_filename):
    grid_len = 8
    sensor_data = {}
    # information
    info = "grid size is 8x8, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 4),
        1: (2, 2),
        2: (2, 6),
        3: (4, 0),
        4: (4, 8),
        5: (6, 2),
        6: (6, 6),
        7: (8, 4)
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 8 sensors in a 10 by 10 grid'''
def onelevel_10x10grid_8sen(filename, fig_filename):
    grid_len = 10
    sensor_data = {}
    # information
    info = "grid size is 10x10, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 5),
        1: (3, 3),
        2: (3, 7),
        3: (5, 0),
        4: (5, 10),
        5: (7, 3),
        6: (7, 7),
        7: (10, 5)
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 8 sensors in a 12 by 12 grid'''
def onelevel_12x12grid_8sen(filename, fig_filename):
    grid_len = 12
    sensor_data = {}
    # information
    info = "grid size is 12x12, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 6),
        1: (3, 3),
        2: (3, 9),
        3: (6, 0),
        4: (6, 12),
        5: (9, 3),
        6: (9, 9),
        7: (12, 6),
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 8 sensors in a 16 by 16 grid'''
def onelevel_16x16grid_8sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 16x16, 8 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 16
    sensors = {
        0: (4, 4), 
        1: (4, 12), 
        2: (12, 4), 
        3: (12, 12),
        4: (0, 8), 
        5: (8, 0), 
        6: (8, 16), 
        7: (16, 8)
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)




# level-0: 1 set of 4 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 16 state discrimination
def two_level_16by16grid_old(filename: str, fig_filename: str):
    sensor_data = {}
    info = 'grid size is 16x16, 64 sensors, 2 levels'
    sensor_data['info'] = info
    sensors = {}
    levels = {}
    sets = {}
    set_i = 0
    sensor_i = 0
    for i in range(4):
        for j in range(4):
            topleft = (4 * i, 4 * j)
            bottomright = (4 * (i + 1), 4 * (j + 1))
            local_set = {"sensors": [], "area": [topleft, bottomright]}
            level0_sensors = [(0, 1), (2, 1), (2, 3), (4, 3)]
            for sen in level0_sensors:
                global_sensor = (sen[0] + 4 * i, sen[1] + 4 * j)
                sensors[sensor_i] = global_sensor
                local_set['sensors'].append(sensor_i)
                sensor_i += 1
            sets[f'set-{set_i}'] = local_set
            set_i += 1
    sensor_data['sensors'] = sensors
    # random.seed(8)
    # level0_set_i = random.sample(range(16), 10)
    # level0_sensors = []
    # for i in sorted(level0_set_i):
    #     local_sensors = sets[f'set-{i}']['sensors']
    #     level0_sensors.append(random.sample(local_sensors, 1)[0])

    level0_sensors = [3, 28, 35, 60]
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)]}
    levels['level-0'] = {'set-0': level0_set}
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    grid_len = 16
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



# level-0: 1 set of 8 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 9 state discrimination
def two_level_16by16grid(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 16x16, 48 sensors, 2.5 levels'
    sensor_data['info'] = info
    # level 0
    num_sensor = 8
    selected_sensors = random_sensors(grid_length=16, num_sensor=num_sensor)
    sensors = {i: tuple(loc) for i, loc in zip(range(num_sensor), selected_sensors)}
    # sensors = {0: (4, 4), 1: (4, 12), 2: (12, 4), 3: (12, 12), 4: (0, 8), 5: (8, 0), 6: (8, 16), 7: (16, 8)}
    # sensors = {0: (4, 5), 1: (3, 12), 2: (7, 6), 3: (10, 14), 4: (3, 9), 5: (4, 2), 6: (13, 4), 7: (11, 9)}
    level0_sensors = [0, 1, 2, 3, 4, 5, 6, 7]
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)]}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = 8
    sensors_reverse = {}
    for i in range(5):
        for j in range(4):
            sensors[sensor_i] = (4 * i, 4 * (j + 0.5))
            sensors_reverse[(4 * i, 4 * (j + 0.5))] = sensor_i
            sensor_i += 1
        if i == 4:
            continue
        for j in range(5):
            sensors[sensor_i] = (4 * (i + 0.5), 4 * j)
            sensors_reverse[(4 * (i + 0.5), 4 * j)] = sensor_i
            sensor_i += 1
    sensor_data['sensors'] = sensors
    # level 1
    sets = {}
    set_i = 0
    for i in range(4):
        for j in range(4):
            sensor_list = []
            for x, y in [(0, 0.5), (0.5, 0), (0.5, 1), (1, 0.5)]:
                loc = (4 * (i + x), 4 * (j + y))
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))]}
            set_i += 1
    levels['level-1'] = sets
    # level 2
    sets = {}
    set_i = 0
    for i in [0.5, 1.5, 2.5]:
        for j in [0.5, 1.5, 2.5]:
            sensor_list = []
            for x, y in [(0, 0.5), (0.5, 0), (0.5, 1), (1, 0.5)]:
                loc = (4 * (i + x), 4 * (j + y))
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))]}
            set_i += 1
    levels['level-1.5'] = sets
    sensor_data['levels'] = levels
    grid_len = 16
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)




if __name__ == '__main__':
    
    fig_filename = 'sensordata/tmp.png'

    # ONE level 4 sensor
    # filename = 'sensordata/onelevel.2x2.4.json'
    # onelevel_2x2grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.4x4.4.json'
    # onelevel_4x4grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.6x6.4.json'
    # onelevel_6x6grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.8x8.4.json'
    # onelevel_8x8grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.4.json'
    # onelevel_10x10grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.4.json'
    # onelevel_12x12grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.4.json'
    # onelevel_16x16grid_4sen(filename, fig_filename)

    # ONE level 8 sensor
    # filename = 'sensordata/onelevel.2x2.8.json'
    # onelevel_2x2grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.4x4.8.json'
    # onelevel_4x4grid_8sen(filename, fig_filename)
    filename = 'sensordata/onelevel.6x6.8.json'
    onelevel_6x6grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.8x8.8.json'
    # onelevel_8x8grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.8.json'
    # onelevel_10x10grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.8.json'
    # onelevel_12x12grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.8.json'
    # onelevel_16x16grid_8sen(filename, fig_filename)



    # filename = 'sensordata/16x16-onelevel.json'
    # fig_filename = 'sensordata/tmp.16x16grid.png'
    # one_level_16by16grid(filename, fig_filename)


    # filename = 'sensordata/16x16-twolevel.random.json'
    # fig_filename = 'sensordata/tmp.16x16grid.png'
    # two_level_16by16grid(filename, fig_filename)

    # filename = 'sensordata/16x16-threelevel.json'
    # fig_filename = 'sensordata/tmp.16x16grid.png'
    # three_level_16by16grid(filename, fig_filename)

    # filename = 'sensordata/6x6-onelevel.json'
    # fig_filename = 'sensordata/tmp.6x6grid.png'
    # one_level_6by6grid(filename, fig_filename)

    # filename = 'sensordata/15x15-twolevel.json'
    # fig_filename = 'sensordata/tmp.15x15grid.png'
    # two_level_15by15grid(filename, fig_filename)