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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
        0: (1, 3),
        1: (3, 1),
        2: (3, 5),
        3: (5, 3)
    }

    sensor_data['sensors'] = sensors
    # one levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
    levels['level-0'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


'''one level, 8 sensors in a 9 by 9 grid'''
def onelevel_9x9grid_8sen(filename, fig_filename):
    grid_len = 9
    sensor_data = {}
    # information
    info = "grid size is 8x8, 8 sensors in one level."
    sensor_data['info'] = info
    sensors = {
        0: (0, 4.5),
        1: (2, 2),
        2: (2, 7),
        3: (4.5, 0),
        4: (4.5, 9),
        5: (7, 2),
        6: (7, 7),
        7: (9, 4.5)
    }
    sensor_data['sensors'] = sensors
    # one level
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_len, grid_len]], 'block_cell_ratio': 1}
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
        0:  (0,    0), 
        1:  (0,    16/3), 
        2:  (0,    32/3), 
        3:  (0,    16),
        4:  (16/3, 0), 
        5:  (16/3, 16/3), 
        6:  (16/3, 32/3), 
        7:  (16/3, 16),
        8:  (32/3, 0), 
        9:  (32/3, 16/3), 
        10: (32/3, 32/3), 
        11: (32/3, 16),
        12: (16,   0), 
        13: (16,   16/3), 
        14: (16,   32/3), 
        15: (16,   16),
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
        0:  (0,    0), 
        1:  (0,    14/3), 
        2:  (0,    28/3), 
        3:  (0,    14),
        4:  (14/3, 0), 
        5:  (14/3, 14/3), 
        6:  (14/3, 28/3), 
        7:  (14/3, 14),
        8:  (28/3, 0), 
        9:  (28/3, 14/3), 
        10: (28/3, 28/3), 
        11: (28/3, 14),
        12: (14,   0), 
        13: (14,   14/3), 
        14: (14,   28/3), 
        15: (14,   14),
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


'''one level 16 sensors in a 12 by 12 grid'''
def onelevel_12x12grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 12x12, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 12
    sensors = {
        0:  (0, 0), 
        1:  (0, 4), 
        2:  (0, 8), 
        3:  (0, 12),
        4:  (4, 0), 
        5:  (4, 4), 
        6:  (4, 8), 
        7:  (4, 12),
        8:  (8, 0), 
        9:  (8, 4), 
        10: (8, 8), 
        11: (8, 12),
        12: (12, 0), 
        13: (12, 4), 
        14: (12, 8), 
        15: (12, 12),
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


'''one level 16 sensors in a 10 by 10 grid'''
def onelevel_10x10grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 10x10, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 10
    sensors = {
        0:  (0,    0),
        1:  (0,    10/3),
        2:  (0,    20/3),
        3:  (0,    10),
        4:  (10/3, 0),
        5:  (10/3, 10/3),
        6:  (10/3, 20/3),
        7:  (10/3, 10),
        8:  (20/3, 0),
        9:  (20/3, 10/3),
        10: (20/3, 20/3),
        11: (20/3, 10),
        12: (10,   0),
        13: (10,   10/3),
        14: (10,   20/3), 
        15: (10,   10),
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
        0:  (0,    0), 
        1:  (0,    8/3), 
        2:  (0,    16/3), 
        3:  (0,    8),
        4:  (8/3,  0), 
        5:  (8/3,  8/3), 
        6:  (8/3,  16/3), 
        7:  (8/3,  8),
        8:  (16/3, 0), 
        9:  (16/3, 8/3), 
        10: (16/3, 16/3), 
        11: (16/3, 8),
        12: (8,    0), 
        13: (8,    8/3), 
        14: (8,    16/3), 
        15: (8,    8),
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
    sets['set-0'] = {'sensors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'area': [[0, 0], [grid_length, grid_length]], 'area': [[0, 0], [grid_length, grid_length]], 'block_cell_ratio': 1}
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
        0:  (0,   0), 
        1:  (0,   4/3), 
        2:  (0,   8/3), 
        3:  (0,   4),
        4:  (4/3, 0), 
        5:  (4/3, 4/3), 
        6:  (4/3, 8/3), 
        7:  (4/3, 4),
        8:  (8/3, 0), 
        9:  (8/3, 4/3), 
        10: (8/3, 8/3), 
        11: (8/3, 4),
        12: (4,   0), 
        13: (4,   4/3), 
        14: (4,   8/3), 
        15: (4,   4),
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


'''one level 16 sensors in a 2 by 2 grid'''
def onelevel_2x2grid_16sen(filename, fig_filename):
    sensor_data = {}
    # information
    info = "grid size is 4x4, 16 sensors at 1 levels."
    sensor_data['info'] = info
    grid_length = 2
    sensors = {
        0:  (0,   0), 
        1:  (0,   2/4), 
        2:  (0,   4/4), 
        3:  (0,   6/4),
        4:  (0,   2), 
        5:  (2/4, 0), 
        6:  (2/4, 2), 
        7:  (1,   0),
        8:  (1,   2), 
        9:  (3/2, 0), 
        10: (3/2, 2), 
        11: (2,   0),
        12: (2,   2/4), 
        13: (2,   4/4), 
        14: (2,   6/4), 
        15: (2,   2),
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



# level-0: 1 set of 4 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 16 state discrimination
def two_level_16by16grid_4sen(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 16x16, 2 levels, 4 sensors in the first level'
    sensor_data['info'] = info
    # level 0
    level0_sen = 4
    sensors = {
        0: (3, 8),
        1: (8, 3),
        2: (8, 13),
        3: (13, 8),
    }

    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(level0_sen))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)], 'block_cell_ratio': 4}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = level0_sen
    # level 1
    set_i = 0
    sets = {}
    for i in range(4):
        for j in range(4):
            sensor_list = []
            base = (i * 4, j * 4)
            relative = [(0, 2), (2, 0), (2, 4), (4, 2)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * 4, j * 4), ((i + 1) * 4, (j + 1) * 4)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    grid_len = 16
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 8 sensors that do 4 state discrimination
# level-1: 4 set of 4 sensors, each set do 4 state discrimination
def two_level_4by4grid_8sen(filename: str, fig_filename: str):
    grid_len = 4
    levels = {}
    sensor_data = {}
    info = f'grid size is {grid_len}x{grid_len}, 2 levels, 8 sensors in the first level'
    sensor_data['info'] = info
    # level 0
    level0_sen = 8
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

    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(level0_sen))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (grid_len, grid_len)], 'block_cell_ratio': 2}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = level0_sen
    block_len = level0_set['block_cell_ratio']
    grid_len_block = grid_len // block_len
    # level 1
    set_i = 0
    sets = {}
    for i in range(grid_len_block):
        for j in range(grid_len_block):
            sensor_list = []
            base = (i * block_len, j * block_len)
            relative = [(0, 1), (1, 0), (1, 2), (2, 1)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * block_len, j * block_len), ((i + 1) * block_len, (j + 1) * block_len)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 8 sensors that do 9 state discrimination
# level-1: 9 set of 4 sensors, each set do 9 state discrimination
def two_level_9by9grid_8sen(filename: str, fig_filename: str):
    grid_len = 9
    levels = {}
    sensor_data = {}
    info = f'grid size is {grid_len}x{grid_len}, 2 levels, 8 sensors in the first level'
    sensor_data['info'] = info
    # level 0
    level0_sen = 8
    sensors = {
        0: (0, 4.5),
        1: (2, 2),
        2: (2, 7),
        3: (4.5, 0),
        4: (4.5, 9),
        5: (7, 2),
        6: (7, 7),
        7: (9, 4.5)
    }

    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(level0_sen))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (grid_len, grid_len)], 'block_cell_ratio': 3}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = level0_sen
    block_len = level0_set['block_cell_ratio']
    grid_len_block = grid_len // block_len
    # level 1
    set_i = 0
    sets = {}
    for i in range(grid_len_block):
        for j in range(grid_len_block):
            sensor_list = []
            base = (i * block_len, j * block_len)
            relative = [(0, 1.5), (1.5, 0), (1.5, 3), (3, 1.5)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * block_len, j * block_len), ((i + 1) * block_len, (j + 1) * block_len)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 8 sensors that do 16 state discrimination
# level-1: 9 set of 4 sensors, each set do 9 state discrimination
def two_level_12by12grid_8sen(filename: str, fig_filename: str):
    grid_len = 12
    levels = {}
    sensor_data = {}
    info = f'grid size is {grid_len}x{grid_len}, 2 levels, 8 sensors in the first level'
    sensor_data['info'] = info
    # level 0
    level0_sen = 8
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

    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(level0_sen))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (grid_len, grid_len)], 'block_cell_ratio': 3}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = level0_sen
    block_len = level0_set['block_cell_ratio']
    grid_len_block = grid_len // block_len
    # level 1
    set_i = 0
    sets = {}
    for i in range(grid_len_block):
        for j in range(grid_len_block):
            sensor_list = []
            base = (i * 3, j * 3)
            relative = [(0, 1.5), (1.5, 0), (1.5, 3), (3, 1.5)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * block_len, j * block_len), ((i + 1) * block_len, (j + 1) * block_len)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 8 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 16 state discrimination
def two_level_16by16grid_8sen(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 16x16, 2 levels, 8 sensors in the first level'
    sensor_data['info'] = info
    # level 0
    level0_sen = 8
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

    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(level0_sen))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)], 'block_cell_ratio': 4}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = level0_sen
    # level 1
    set_i = 0
    sets = {}
    for i in range(4):
        for j in range(4):
            sensor_list = []
            base = (i * 4, j * 4)
            relative = [(0, 2), (2, 0), (2, 4), (4, 2)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * 4, j * 4), ((i + 1) * 4, (j + 1) * 4)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    grid_len = 16
    Plot.visualize_sensors(grid_len, sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


# level-0: 1 set of 16 sensors that do 16 state discrimination
# level-1: 16 set of 4 sensors, each set do 16 state discrimination
def two_level_16by16grid_16sen(filename: str, fig_filename: str):
    levels = {}
    sensor_data = {}
    info = 'grid size is 16x16, xx sensors, 2 levels'
    sensor_data['info'] = info
    # level 0
    sensors = {
        0:  (0,    0), 1:  (0,    16/3), 2:  (0,    32/3), 3:  (0,    16),
        4:  (16/3, 0), 5:  (16/3, 16/3), 6:  (16/3, 32/3), 7:  (16/3, 16),
        8:  (32/3, 0), 9:  (32/3, 16/3), 10: (32/3, 32/3), 11: (32/3, 16),
        12: (16,   0), 13: (16,   16/3), 14: (16,   32/3), 15: (16,   16),
    }
    sensors_reverse = {val: key for key, val in sensors.items()}
    level0_sensors = list(range(16))
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)], 'block_cell_ratio': 4}
    levels['level-0'] = {'set-0': level0_set}
    sensor_i = 16
    # level 1
    set_i = 0
    sets = {}
    for i in range(4):
        for j in range(4):
            sensor_list = []
            base = (i * 4, j * 4)
            relative = [(0, 2), (2, 0), (2, 4), (4, 2)]
            for r in relative:
                loc = (base[0] + r[0], base[1] + r[1])
                if loc not in sensors_reverse:
                    sensors[sensor_i] = loc
                    sensors_reverse[loc] = sensor_i
                    sensor_list.append(sensor_i)
                    sensor_i += 1
                else:
                    sensor_list.append(sensors_reverse[loc])
            sets[f'set-{set_i}'] = {'sensors': sensor_list, 'area': [(i * 4, j * 4), ((i + 1) * 4, (j + 1) * 4)], 'block_cell_ratio': 1}
            set_i += 1

    sensor_data['sensors'] = sensors
    levels['level-1'] = sets
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
    # filename = 'sensordata/onelevel.9x9.8.json'
    # onelevel_9x9grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.10x10.8.json'
    # onelevel_10x10grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.12x12.8.json'
    # onelevel_12x12grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.14x14.8.json'
    # onelevel_14x14grid_8sen(filename, fig_filename)
    # filename = 'sensordata/onelevel.16x16.8.json'
    # onelevel_16x16grid_8sen(filename, fig_filename)

    # ONE level 16 sensor

    # filename = 'sensordata/onelevel.2x2.16.json'
    # onelevel_2x2grid_16sen(filename, fig_filename)
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
    # filename = 'sensordata/onelevel.40x40.16.json'
    # onelevel_40x40grid_16sen(filename, fig_filename)


    fig_filename = 'sensordata/tmp.twolevel.png'
    # TWO level 4 sensor
    # filename = 'sensordata/twolevel.16x16.4.json'
    # two_level_16by16grid_4sen(filename, fig_filename)
    
    # TWO level 8 sensor
    # filename = 'sensordata/twolevel.4x4.8.json'
    # two_level_4by4grid_8sen(filename, fig_filename)
    # filename = 'sensordata/twolevel.9x9.8.json'
    # two_level_9by9grid_8sen(filename, fig_filename)
    filename = 'sensordata/twolevel.12x12.8.json'
    two_level_12by12grid_8sen(filename, fig_filename)
    # filename = 'sensordata/twolevel.16x16.8.json'
    # two_level_16by16grid_8sen(filename, fig_filename)

    # TWO level 16 sensor
    # filename = 'sensordata/twolevel.16x16.16.json'
    # two_level_16by16grid_16sen(filename, fig_filename)

