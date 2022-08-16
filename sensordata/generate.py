'''generate sensor data, sensor is in continuous locations, i.e., not confined at the center of a grid cell
'''
import json
from my_encoder import MyJSONEncoder


def two_level_4by4grid(filename):
    '''two level 4 sensors in a 4 by 4 grid
    '''
    sensor_data = {}
    # information
    info = "grid size is 4x4, 12 sensors at 2 levels."
    sensor_data['info'] = info
    # location of 12 sensors
    sensors = {
        0: (0, 1),
        1: (0, 3),
        2: (1, 0),
        3: (1, 2),
        4: (1, 4),
        5: (2, 1),
        6: (2, 3),
        7: (3, 0),
        8: (3, 2),
        9: (3, 4),
        10: (4, 1),
        11: (4, 3)
    }
    sensor_data['sensors'] = sensors
    # two levels
    levels = {}
    sets = {}
    sets['set-0'] = {'sensors': [0, 4, 7, 11], 'area': [[0, 0], [4, 4]]}
    levels['level-1'] = sets
    sets = {}
    sets['set-0'] = {'sensors': [0, 2, 3, 5],  'area': [[0, 0], [2, 2]]}
    sets['set-1'] = {'sensors': [1, 3, 4, 6],  'area': [[0, 2], [2, 4]]}
    sets['set-2'] = {'sensors': [5, 7, 8, 10], 'area': [[2, 0], [4, 2]]}
    sets['set-3'] = {'sensors': [6, 8, 9, 11], 'area': [[2, 2], [4, 4]]}
    levels['level-2'] = sets
    sensor_data['levels'] = levels
    # two level mapping -- level 1's sensor -> level 2's set
    mappings = {}
    mappings['level-1-sensor-0']  = 'level-2-set-0'
    mappings['level-1-sensor-4']  = 'level-2-set-1'
    mappings['level-1-sensor-7']  = 'level-2-set-2'
    mappings['level-1-sensor-11'] = 'level-2-set-3'
    sensor_data['mappings'] = mappings

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



if __name__ == '__main__':
    
    filename = '4x4-twolevel.json'
    two_level_4by4grid(filename)
