'''generate sensor data, sensor is in continuous locations, i.e., not confined at the center of a grid cell
'''
import json


def one_level_4sensor(filename):
    '''one level 4 sensors in a 4 by 4 grid
    '''
    sensor = [(2, 0), (4, 2), (2, 4), (0, 2)]
    levels = {}
    sets = {}
    sensordict = {}
    for i, loc in enumerate(sensor):
        sensordict[i] = loc
    sets['set-1'] = sensordict
    levels['level-1'] = sets

    with open(filename, 'w') as f:
        json.dump(levels, f)


def two_level_4sensor(filename):
    '''two level 4 sensors in a 4 by 4 grid
    '''
    # level 1 has 1 set of 4 sensors
    sensor = [(2, 0), (4, 2), (2, 4), (0, 2)]
    levels = {}
    sets = {}
    sensordict = {}
    for i, loc in enumerate(sensor):
        sensordict[i] = loc
    sets['set-1'] = sensordict
    levels['level-1'] = sets

    # level 2 has 4 set of 4 sensors
    sensor = [[(0.5, 0.5), (0.5, 1.5), (1.5, 0.5), (1.5, 1.5)],
              [(0.5, 2.5), (0.5, 3.5), (1.5, 2.5), (1.5, 3.5)],
              [(2.5, 0.5), (2.5, 1.5), (3.5, 0.5), (3.5, 1.5)],
              [(2.5, 2.5), (2.5, 3.5), (3.5, 2.5), (3.5, 3.5)]]
    
    sets = {}
    for set_num, set_sensor in enumerate(sensor):
        sensordict = {}
        for i, loc in enumerate(set_sensor):
            sensordict[i] = loc
        sets[f'set-{set_num}'] = sensordict
    levels['level-2'] = sets

    with open(filename, 'w') as f:
        json.dump(levels, f)




if __name__ == '__main__':
    filename = '4x4-onelevel.json'
    one_level_4sensor(filename)
    
    filename = '4x4-twolevel.json'
    two_level_4sensor(filename)
