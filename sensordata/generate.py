'''generate sensor data, sensor is in continuous locations, i.e., not confined at the center of a grid cell
'''
import json
from my_encoder import MyJSONEncoder


def two_level_4by4grid(filename):
    '''two level 4 sensors in a 4 by 4 grid
    '''
    sensor_data = {}
    
    info = "grid size is 4x4, 12 sensors at 2 levels."
    sensor_data['info'] = info

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

    levels = {}
    sets = {}
    sets['set-0'] = [0, 4, 11, 7]  # sensor ID
    levels['level-1'] = sets
    sets = {}
    sets['set-0'] = [0, 2, 3, 5]
    sets['set-1'] = [1, 3, 4, 6]
    sets['set-2'] = [5, 7, 8, 10]
    sets['set-3'] = [6, 8, 9, 11]
    levels['level-2'] = sets
    sensor_data['levels'] = levels

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=2, cls=MyJSONEncoder)

    print(json.dumps(sensor_data, indent=2, cls=MyJSONEncoder))



if __name__ == '__main__':
    
    filename = '4x4-twolevel.json'
    two_level_4by4grid(filename)
