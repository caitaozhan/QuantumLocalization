'''generate sensor data, sensor is in continuous locations, i.e., not confined at the center of a grid cell
'''

from plot import Plot
import json
import random
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
    levels['level-0'] = sets
    sets = {}
    sets['set-0'] = {'sensors': [0, 2, 3, 5],  'area': [[0, 0], [2, 2]]}
    sets['set-1'] = {'sensors': [1, 3, 4, 6],  'area': [[0, 2], [2, 4]]}
    sets['set-2'] = {'sensors': [5, 7, 8, 10], 'area': [[2, 0], [4, 2]]}
    sets['set-3'] = {'sensors': [6, 8, 9, 11], 'area': [[2, 2], [4, 4]]}
    levels['level-1'] = sets
    sensor_data['levels'] = levels

    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)


def two_level_16by16grid(filename: str, fig_filename: str):
    # level-0: 1 set of 10 sensors that do 16 state discrimination
    # level-1: 16 set of 4 sensors, each set do 16 state discrimination
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
    random.seed(8)
    level0_set_i = random.sample(range(16), 10)
    level0_sensors = []
    for i in sorted(level0_set_i):
        local_sensors = sets[f'set-{i}']['sensors']
        level0_sensors.append(random.sample(local_sensors, 1)[0]) 
    level0_set = {'sensors': level0_sensors, 'area': [(0, 0), (16, 16)]}
    levels['level-0'] = level0_set
    levels['level-1'] = sets
    sensor_data['levels'] = levels
    Plot.visualize_sensors(sensors, level0_sensors, fig_filename)
    with open(filename, 'w') as f:
        json.dump(sensor_data, f, indent=4, cls=MyJSONEncoder)



if __name__ == '__main__':
    
    # filename = '4x4-twolevel.json'
    # two_level_4by4grid(filename)

    filename = 'sensordata/16x16-twolevel.json'
    fig_filename = 'sensordata/tmp.16x16grid.png'
    two_level_16by16grid(filename, fig_filename)

