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


'''one level, 5 sensors, 4 by 4 grid'''
def onelevel_4x4grid_5sen(filename, fig_filename):
    grid_length = 4
    sensor_data = {}
    # information
    info = "grid size is 4x4, 4 sensors at 1 levels."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 0),
        1: (0, 4),
        2: (2, 2),
        3: (4, 0),
        4: (4, 4)
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


'''one level, 4 sensors in a 14 by 14 grid'''
def onelevel_14x14grid_4sen(filename, fig_filename):
    grid_len = 14
    sensor_data = {}
    # information
    info = "grid size is 14x14, 4 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (3, 7),
        1: (7, 3),
        2: (7, 11),
        3: (11, 7),
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
    info = "grid size is 6x6, 8 sensors at 1 levels."
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
    info = "grid size is 8x8, 8 sensors in one level."
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
    info = "grid size is 10x10, 8 sensors in one level."
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
    info = "grid size is 12x12, 8 sensors in one level."
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


'''one level, 8 sensors in a 14 by 14 grid'''
def onelevel_14x14grid_8sen(filename, fig_filename):
    grid_len = 14
    sensor_data = {}
    # information
    info = "grid size is 14x14, 8 sensors in one level."
    sensor_data['info'] = info
    # location of 4 sensors
    sensors = {
        0: (0, 7),
        1: (4, 4),
        2: (4, 10),
        3: (7, 0),
        4: (7, 14),
        5: (10, 4),
        6: (10, 10),
        7: (14, 7),
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


'''one level 16 sensors in a 16 by 16 grid'''
def onelevel_16x16grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 16x16, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 16
    sensors = {
        0: (2, 2), 
        1: (2, 6), 
        2: (2, 10), 
        3: (2, 14),
        4: (6, 2), 
        5: (6, 6), 
        6: (6, 10), 
        7: (6, 14),
        8: (10, 2), 
        9: (10, 6), 
        10: (10, 10), 
        11: (10, 14),
        12: (14, 2), 
        13: (14, 6), 
        14: (14, 10), 
        15: (14, 14),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 16 sensors in a 14 by 14 grid'''
def onelevel_14x14grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 14x14, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 14
    sensors = {
        0:  (1, 1), 
        1:  (1, 5), 
        2:  (1, 9), 
        3:  (1, 13),
        4:  (5, 1), 
        5:  (5, 5), 
        6:  (5, 9), 
        7:  (5, 13),
        8:  (9, 1), 
        9:  (9, 5), 
        10: (9, 9), 
        11: (9, 13),
        12: (13, 1), 
        13: (13, 5), 
        14: (13, 9), 
        15: (13, 13),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 16 sensors in a 12 by 12 grid'''
def onelevel_12x12grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 12x12, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 12
    sensors = {
        0:  (1, 1), 
        1:  (1, 4), 
        2:  (1, 7), 
        3:  (1, 10),
        4:  (4, 1), 
        5:  (4, 4), 
        6:  (4, 7), 
        7:  (4, 10),
        8:  (7, 1), 
        9:  (7, 4), 
        10: (7, 7), 
        11: (7, 10),
        12: (10, 1), 
        13: (10, 4), 
        14: (10, 7), 
        15: (10, 10),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 16 sensors in a 10 by 10 grid'''
def onelevel_10x10grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 10x10, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 10
    sensors = {
        0:  (0, 0), 
        1:  (0, 3), 
        2:  (0, 6), 
        3:  (0, 9),
        4:  (3, 0), 
        5:  (3, 3), 
        6:  (3, 6), 
        7:  (3, 9),
        8:  (6, 0), 
        9:  (6, 3), 
        10: (6, 6), 
        11: (6, 9),
        12: (9, 0), 
        13: (9, 3), 
        14: (9, 6), 
        15: (9, 9),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 16 sensors in a 8 by 8 grid'''
def onelevel_8x8grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 8x8, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 8
    sensors = {
        0:  (1, 1), 
        1:  (1, 3), 
        2:  (1, 5), 
        3:  (1, 7),
        4:  (3, 1), 
        5:  (3, 3), 
        6:  (3, 5), 
        7:  (3, 7),
        8:  (5, 1), 
        9:  (5, 3), 
        10: (5, 5), 
        11: (5, 7),
        12: (7, 1), 
        13: (7, 3), 
        14: (7, 5), 
        15: (7, 7),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



'''one level 16 sensors in a 6 by 6 grid'''
def onelevel_6x6grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 6x6, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 6
    sensors = {
        0:  (0, 0), 
        1:  (0, 2), 
        2:  (0, 4), 
        3:  (0, 6),
        4:  (2, 0), 
        5:  (2, 2), 
        6:  (2, 4), 
        7:  (2, 6),
        8:  (4, 0), 
        9:  (4, 2), 
        10: (4, 4), 
        11: (4, 6),
        12: (6, 0), 
        13: (6, 2), 
        14: (6, 4), 
        15: (6, 6),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



'''one level 16 sensors in a 4 by 4 grid'''
def onelevel_4x4grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 4x4, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 4
    sensors = {
        0:  (0, 0), 
        1:  (0, 1), 
        2:  (0, 2), 
        3:  (0, 3),
        4:  (1, 0), 
        5:  (1, 1), 
        6:  (1, 2), 
        7:  (1, 3),
        8:  (2, 3), 
        9:  (2, 1), 
        10: (2, 2), 
        11: (2, 3),
        12: (3, 0), 
        13: (3, 1), 
        14: (3, 2), 
        15: (3, 3),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



'''one level 16 sensors in a 24 by 24 grid'''
def onelevel_24x24grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 24x24, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 24
    sensors = {
        0:  (3, 3),
        1:  (3, 9),
        2:  (3, 15),
        3:  (3, 21),
        4:  (9, 3),
        5:  (9, 9),
        6:  (9, 15), 
        7:  (9, 21),
        8:  (15, 3), 
        9:  (15, 9), 
        10: (15, 15), 
        11: (15, 21),
        12: (21, 3), 
        13: (21, 9), 
        14: (21, 15), 
        15: (21, 21),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]]}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level 16 sensors in a 40 by 40 grid'''
def onelevel_40x40grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 40x40, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 40
    sensors = {
        0:  (5, 5),
        1:  (5, 15),
        2:  (5, 25),
        3:  (5, 35),
        4:  (15, 5),
        5:  (15, 15),
        6:  (15, 25), 
        7:  (15, 35),
        8:  (25, 5), 
        9:  (25, 15), 
        10: (25, 25), 
        11: (25, 35),
        12: (35, 5), 
        13: (35, 15), 
        14: (35, 25), 
        15: (35, 35),
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_length, sensors, sensors, fig_filename)

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



################ two level #######################################################

# level-0: 1 set of 8 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 16 state discrimination
def two_level_16by16grid(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 16x16, 48 sensors, 2.5 levels'
    sensor_data['info'] = info
    # level 0
    sensors = {0: (4, 4), 1: (4, 12), 2: (12, 4), 3: (12, 12), 4: (0, 8), 5: (8, 0), 6: (8, 16), 7: (16, 8)}
    level0_sensors = [0, 1, 2, 3, 4, 5, 6, 7]
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)], 'block_cell_ratio': 4}
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
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1
    levels['level-1'] = sets
    # level 1.5
    sets = {}
    set_i = 0
    # blocks not at the grid edge, 4 sensors per block
    for i in [0.5, 1.5, 2.5]:
        for j in [0.5, 1.5, 2.5]:
            sensor_list = []
            for x, y in [(0, 0.5), (0.5, 0), (0.5, 1), (1, 0.5)]:
                loc = (4 * (i + x), 4 * (j + y))
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1
    # blocks at the grid edge, 5 sensors per block
    for i in [0, 3]:
        for j in [0.5, 1.5, 2.5]:
            sensor_list = []
            for x, y in [(0, 0), (1, 0), (1, 0), (1, 1)]:
                loc = (4 * (i + x), 4 * (j + y))
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1
    for i in [0.5, 1.5, 2.5]:
        for j in [0, 3]:
            sensor_list = []
            for x, y in [(0, 0), (1, 0), (1, 0), (1, 1)]:
                loc = (4 * (i + x), 4 * (j + y))
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1

    levels['level-1.5'] = sets
    sensor_data['levels'] = levels
    grid_len = 16
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



# level-0: 1 set of 20 sensors that do 25 state discrimination
# level-1: 25 set of 8 sensors, each set do 64 state discrimination
def two_level_40by40grid(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 40x40, 48 sensors, 2 levels'
    sensor_data['info'] = info
    sensors = {}
    sensors_reverse = {}
    sensor_i = 0
    for i in range(5): # in level-0, there are 5x5 blocks
        for j in range(5):
            relative = [(0, 0), (8, 0), (4, 2), (2, 4), (6, 4), (4, 6), (0, 8), (8, 8)]
            base = (i * 8, j * 8)
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_i += 1
    sensors[sensor_i] = (0, 20)
    sensors_reverse[(0, 20)] = sensor_i
    sensor_i += 1
    sensors[sensor_i] = (20, 0)
    sensors_reverse[(20, 0)] = sensor_i
    sensor_i += 1
    sensors[sensor_i] = (20, 40)
    sensors_reverse[(20, 40)] = sensor_i
    sensor_i += 1
    sensors[sensor_i] = (40, 20)
    sensors_reverse[(40, 20)] = sensor_i
    sensor_data['sensors'] = sensors

    # level 0
    level0_sensors_loc = [(8, 8),  (8, 16),  (8, 24),  (8, 32),  (16, 8), (16, 16), (16, 24), (16, 32),
                          (24, 8), (24, 16), (24, 24), (24, 32), (32, 8), (32, 16), (32, 24), (32, 32),
                          (0, 20), (20, 0),  (20, 40), (40, 20)]
    
    level0_sensors = [sensors_reverse[loc] for loc in level0_sensors_loc]
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (40, 40)], 'block_cell_ratio': 8}
    levels['level-0'] = {'set-0': level0_set}
    # level 1
    sets = {}
    set_i = 0
    for i in range(5):
        for j in range(5):
            sensor_list = []
            relative = [(0, 0), (8, 0), (4, 2), (2, 4), (6, 4), (4, 6), (0, 8), (8, 8)]
            base = (i * 8, j * 8)
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(8 * i, 8 * j), (8 * (i + 1), 8 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1
    levels['level-1'] = sets
    # level 1.5
    # sets = {}
    # set_i = 0
    # # blocks not at the grid edge, 4 sensors per block
    # for i in [0.5, 1.5, 2.5]:
    #     for j in [0.5, 1.5, 2.5]:
    #         sensor_list = []
    #         for x, y in [(0, 0.5), (0.5, 0), (0.5, 1), (1, 0.5)]:
    #             loc = (4 * (i + x), 4 * (j + y))
    #             sensor_list.append(sensors_reverse[loc])
    #         sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
    #         set_i += 1
    # # blocks at the grid edge, 5 sensors per block
    # for i in [0, 3]:
    #     for j in [0.5, 1.5, 2.5]:
    #         sensor_list = []
    #         for x, y in [(0, 0), (1, 0), (1, 0), (1, 1)]:
    #             loc = (4 * (i + x), 4 * (j + y))
    #             sensor_list.append(sensors_reverse[loc])
    #         sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
    #         set_i += 1
    # for i in [0.5, 1.5, 2.5]:
    #     for j in [0, 3]:
    #         sensor_list = []
    #         for x, y in [(0, 0), (1, 0), (1, 0), (1, 1)]:
    #             loc = (4 * (i + x), 4 * (j + y))
    #             sensor_list.append(sensors_reverse[loc])
    #         sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(4 * i, 4 * j), (4 * (i + 1), 4 * (j + 1))], 'block_cell_ratio': 1}
    #         set_i += 1

    # levels['level-1.5'] = sets
    sensor_data['levels'] = levels
    grid_len = 40
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 20 sensors that do 100 state discrimination
# level-1: 100 set of 10 sensors, each set do 100 state discrimination
def two_level_100by100grid(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 100x100, 48 sensors, 2 levels'
    sensor_data['info'] = info
    sensors = {}
    sensors_reverse = {}
    sensor_i = 0
    for i in range(10):   # in level-0, there are 10x10 blocks
        for j in range(10):
            relative = [(0, 0), (0, 5), (0, 10), (3, 3), (3, 7), (5, 0), (5, 10), (7, 3), (7, 7), (10, 0), (10, 5), (10, 10)]
            base = (i * 10, j * 10)
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_i += 1
    sensor_data['sensors'] = sensors

    # level 0
    level0_sensors_loc = [(0, 50), (20, 20), (20, 40), (20, 60), (20, 80), 
                          (40, 20), (40, 40), (40, 60), (40, 80), (50, 0), (50, 100),
                          (60, 20), (60, 40), (60, 60), (60, 80), 
                          (80, 20), (80, 40), (80, 60), (80, 80), (100, 50)]
    
    level0_sensors = [sensors_reverse[loc] for loc in level0_sensors_loc]
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (100, 100)], 'block_cell_ratio': 10}
    levels['level-0'] = {'set-0': level0_set}
    # level 1
    sets = {}
    set_i = 0
    for i in range(10):
        for j in range(10):
            sensor_list = []
            relative = [(0, 0), (0, 5), (0, 10), (3, 3), (3, 7), (5, 0), (5, 10), (7, 3), (7, 7), (10, 0), (10, 5), (10, 10)]
            base = (i * 10, j * 10)
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(10 * i, 10 * j), (10 * (i + 1), 10 * (j + 1))], 'block_cell_ratio': 1}
            set_i += 1
    levels['level-1'] = sets

    sensor_data['levels'] = levels
    grid_len = 100
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
    # filename = 'sensordata/onelevel.4x4.5.json'
    # onelevel_4x4grid_5sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.6x6.4.json'
    # onelevel_6x6grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.6x6.4.json'
    # onelevel_6x6grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.8x8.4.json'
    # onelevel_8x8grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.4.json'
    # onelevel_10x10grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.4.json'
    # onelevel_12x12grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.14x14.4.json'
    # onelevel_14x14grid_4sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.4.json'
    # onelevel_16x16grid_4sen(filename, fig_filename)

    # ONE level 8 sensor
    # filename = 'sensordata/onelevel.2x2.8.json'
    # onelevel_2x2grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.4x4.8.json'
    # onelevel_4x4grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.6x6.8.json'
    # onelevel_6x6grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.8x8.8.json'
    # onelevel_8x8grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.8.json'
    # onelevel_10x10grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.8.json'
    # onelevel_12x12grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.14x14.8.json'
    # onelevel_14x14grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.8.json'
    # onelevel_16x16grid_8sen(filename, fig_filename)

    # ONE level 16 sensor
    # filename = 'sensordata/onelevel.4x4.16.json'
    # onelevel_4x4grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.6x6.16.json'
    # onelevel_6x6grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.8x8.16.json'
    # onelevel_8x8grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.16.json'
    # onelevel_10x10grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.16.json'
    # onelevel_12x12grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.14x14.16.json'
    # onelevel_14x14grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.16.json'
    # onelevel_16x16grid_16sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.24x24.16.json'
    # onelevel_24x24grid_16sen(filename, fig_filename)
    filename = 'sensordata/onelevel.40x40.16.json'
    onelevel_40x40grid_16sen(filename, fig_filename)


    # TWO level #

    # filename = 'sensordata/twolevel.16x16.json'
    # fig_filename = 'sensordata/tmp.16x16grid.png'
    # two_level_16by16grid(filename, fig_filename)
    # filename = 'sensordata/twolevel.40x40.json'
    # fig_filename = 'sensordata/tmp.40x40grid.png'
    # two_level_40by40grid(filename, fig_filename)
    # filename = 'sensordata/twolevel.100x100.json'
    # fig_filename = 'sensordata/tmp.100x100grid.png'
    # two_level_100by100grid(filename, fig_filename)
