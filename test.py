'''for testing purpose
'''

import time
import random
import matplotlib.pyplot as plt
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator



'''4x4 grid, one level localization'''
def localization_onelevel_12sensor_discrete():
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    save = 'tmp-folder/onelevel_16state.povm'
    # save = ''
    ql.training_onelevel_16state_12sensor(save)
    level_0_right = 0
    tx_list = []
    for x in range(4):
        for y in range(4):
            tx_list.append((x + 0.5, y + 0.5))

    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_16state_12sensor(tx)
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/len(tx_list)}')
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    fig.savefig('tmp.wrong.png')



'''4x4 grid, one level localization'''
def localization_onelevel_4sensor_discrete():

    random.seed(3)
    # sensordata = 'sensordata/4x4-twolevel.json'
    sensordata = 'sensordata/4x4-onelevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_onelevel_16state_level_0_set_0()
    # ql.training_onelevel_16state_level_0_set_0_initstate()    # optimizes initial state

    tx_list = []
    for x in range(4):
        for y in range(4):
            tx_list.append((x + 0.5, y + 0.5))
    level_0_right = 0
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_16state_level_0_set_0(tx, grid_length=4)
        # ret = ql.testing_onelevel_16state_level_0_set_0_initstate(tx, grid_length=4)
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/len(tx_list)}')
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    
    fig.savefig('tmp.wrong.png')


'''6x6 grid, one level localization'''
def localization_onelevel_4sensor_6x6grid():
    random.seed(3)
    grid_len = 6
    sensordata = 'sensordata/6x6-onelevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    # ql.training_onelevel_36state_level_0_set_0()              # simple initial state
    ql.training_onelevel_36state_level_0_set_0_initstate()    # optimizes initial state

    tx_list = []
    for x in range(6):
        for y in range(6):
            tx_list.append((x + 0.5, y + 0.5))
    level_0_right = 0
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_36state_level_0_set_0(tx, grid_length=grid_len, opt_init_state=True)
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/len(tx_list)}')
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    fig.savefig('tmp.wrong.png')


'''16x16 grid, one level localization, testing locations are discrete'''
def localization_onelevel_16x16grid():
    grid_length = 16
    random.seed(3)
    sensordata = 'sensordata/16x16-twolevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    # filename = 'tmp-folder/grid16_onelevel.povm'
    filename = ''
    ql.training_onelevel_16x16grid(filename)

    tx_list = []
    for x in range(16):
        for y in range(16):
            tx_list.append((x + 0.5, y + 0.5))
    level_0_right = 0
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        start = time.time()
        ret = ql.testing_onelevel_16x16grid(tx, grid_length=grid_length)
        print(f'time = {time.time() - start}')
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/len(tx_list)}')
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    fig.savefig('tmp.wrong.png')


'''16x16 grid, two level localization'''
def localization_twolevel_16x16grid():
    # sensordata = 'sensordata/16x16-twolevel.3.json'
    sensordata = 'sensordata/16x16-twolevel.4.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_twolevel_16x16grid()
    level_0_right = 0
    level_1_right = 0
    tx_list = []
    for x in range(16):
        for y in range(16):
            tx_list.append((x + 0.5, y + 0.5))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        # ret0, ret1 = ql.testing_twolevel_16x16grid(tx)
        ret0, ret1 = ql.testing_twolevel_16x16grid_plus(tx)
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
    fig.savefig('tmp.right.png')

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


def localization_twolevel_15x15grid():
    random.seed(3)
    sensordata = 'sensordata/15x15-twolevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_twolevel_15x15grid()
    level_0_right = 0
    level_1_right = 0
    tx_list = []
    for x in range(15):
        for y in range(15):
            tx_list.append((x + 0.5, y + 0.5))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret0, ret1 = ql.testing_twolevel_15x15grid(tx)
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
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
        print()
    print(f'level-0 accuracy={level_0_right/len(tx_list)}')
    print(f'level-1 accuracy={level_1_right/len(tx_list)}')
    
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])
    ax.scatter(wrong_x, wrong_y, c='red')
    ax.grid()
    ax.set_title('Scatter Plot for Wrong Test Sample')
    fig.savefig('tmp.wrong.png')


'''16x16 grid, three level localization'''
def localization_threelevel_16x16grid():
    random.seed(3)
    sensordata = 'sensordata/16x16-threelevel.json'
    unitary_operator = UnitaryOperator(Default.alpha, Default.std, Default.power_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_threelevel_16x16grid()
    level_0_right = 0
    level_1_right = 0
    level_2_right = 0
    tx_list = []
    for x in range(16):
        for y in range(16):
            tx_list.append((x + 0.5, y + 0.5))
    # for x in [0, 8]:
    #     for y in [0, 8]:
    #         tx_list.append((x, y))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret0, ret1, ret2 = ql.testing_threelevel_16x16grid(tx)
        correct = False
        if ret0:
            level_0_right += 1
            if ret1:
                level_1_right += 1
                if ret2:
                    correct = True
                    level_2_right += 1
                    right_x.append(tx[0])
                    right_y.append(tx[1])
        if correct is False:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
        print()
    print(f'level-0 accuracy={level_0_right/len(tx_list)}')
    print(f'level-1 accuracy={level_1_right/len(tx_list)}')
    print(f'level-2 accuracy={level_2_right/len(tx_list)}')
    
    plt.rcParams['font.size'] = 20
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    ax.scatter(right_x, right_y, c='green')
    ax.set_title('Scatter Plot for Right Test Sample')
    ax.grid()
    fig.savefig('tmp.right.png')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(wrong_x, wrong_y, c='red')
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
    localization_twolevel_16x16grid()
    # localization_threelevel_16x16grid()

    # 6x6 grid
    # localization_onelevel_4sensor_6x6grid()

    # 15x15 grid
    # localization_twolevel_15x15grid()