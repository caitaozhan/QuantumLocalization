'''for testing purpose
'''

import time
import numpy as np
import random
import matplotlib.pyplot as plt
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator




'''16x16 grid, two level localization'''
def localization_twolevel_16x16grid():
    np.random.seed(0)
    sensordata = 'sensordata/twolevel.16x16.json'
    # sensordata = 'sensordata/16x16-twolevel.random.json'
    unitary_operator = UnitaryOperator(Default.alpha, 1, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length, cell_length=Default.cell_length,
                             sensordata=sensordata, unitary_operator=unitary_operator)
    ql.training_twolevel_16x16grid()
    level_0_right = 0
    level_1_right = 0
    tx_list = []
    for x in range(16):
        for y in range(16):
            tx_list.append((x + 0.5 + np.random.uniform(-0.5, 0.5), y + 0.5 + np.random.uniform(-0.5, 0.5)))
            # tx_list.append((x + 0.5, y + 0.5))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        # if i not in [7]:
        #     continue
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        # ret0, ret1 = ql.testing_twolevel_16x16grid(tx)
        ret0, ret1 = ql.testing_twolevel_16x16grid_pro(tx)
        if ret0:
            level_0_right += 1
            if ret1:
                level_1_right += 1
                right_x.append(tx[0])
                right_y.append(tx[1])
            else:
                wrong_x.append(tx[0])
                wrong_y.append(tx[1])
        else:
            if ret1:  # level_0 False but level_1 True could happen
                level_1_right += 1
                right_x.append(tx[0])
                right_y.append(tx[1])
            else:
                wrong_x.append(tx[0])
                wrong_y.append(tx[1])
        print()
    print(f'level-0 accuracy={level_0_right/len(tx_list)}')
    print(f'level-1 accuracy={level_1_right/len(tx_list)}')
    
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    level_i, set_i = 0, 0
    sensors = ql.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']['sensors']
    sen_x, sen_y = [], []
    for sen_i in sensors:
        sen = ql.sensordata['sensors'][f'{sen_i}']
        sen_x.append(sen[0])
        sen_y.append(sen[1])

    ax.set_xlim([-0.1, 16.1])
    ax.set_ylim([-0.1, 16.1])
    ax.scatter(sen_x, sen_y, c='black', marker='^', s=100)
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right2.png')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim([-0.1, 16.1])
    ax.set_ylim([-0.1, 16.1])
    ax.scatter(sen_x, sen_y, c='black', marker='^', s=100)
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.set_xticks(range(17))
    ax.set_yticks(range(17))
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    fig.savefig('tmp.wrong.png')




if __name__ == '__main__':

    # 4x4 grid
    # localization_onelevel_4sensor_discrete()
    # localization_onelevel_12sensor()
    # localization_onelevel_12sensor_discrete()
    # localization_twolevel_4x4grid()

    # 16x16 grid
    # localization_onelevel_16x16grid()
    localization_twolevel_16x16grid()        # this one
    # localization_threelevel_16x16grid()

    # 6x6 grid
    # localization_onelevel_4sensor_6x6grid()

    # 15x15 grid
    # localization_twolevel_15x15grid()