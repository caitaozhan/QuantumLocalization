'''for testing purpose
'''

import random
import matplotlib.pyplot as plt
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator


def localization_twolevel():
    '''4x4 grid, two level localization
    '''
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    initial_state = 'simple'
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_onelevel_fourstate_povm(initial_state)
    # tx_list = [(1, 1)]
    repeat = 1000
    level_0_right = 0
    level_1_right = 0
    tx_list = []
    for _ in range(repeat):
        # tx_list.append((1 + (2*random.random()-1)/2, 1 + (2*random.random()-1)/2))
        # tx_list.append((1 + (2*random.random()-1)/10, 1 + (2*random.random()-1)/10))
        tx_list.append((random.random()*4, random.random()*4))
    right_x, right_y = [], []
    wrong_x, wrong_y     = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        # print(f'distance={Utility.distance((1, 1), tx, Default.cell_length):.3f}', end=' ')
        ret0, ret1 = ql.testing_twolevel_fourstate_povm(tx, initial_state)
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
    print(f'level-0 accuracy={level_0_right/repeat}')
    print(f'level-1 accuracy={level_1_right/repeat}')
    
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


def localization_onelevel_12sensor_discrete():
    '''4x4 grid, one level localization
    '''
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    save = 'tmp-folder/onelevel_16state.povm'
    # save = ''
    ql.training_onelevel_16state_povm(save)
    level_0_right = 0
    tx_list = []
    for x in range(4):
        for y in range(4):
            tx_list.append((x + 0.5, y + 0.5))

    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_16state_povm(tx)
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


def localization_onelevel_12sensor():
    '''4x4 grid, one level localization
    '''
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    save = 'tmp-folder/onelevel_16state.povm'
    # save = ''
    ql.training_onelevel_16state_povm(save)
    repeat = 100
    level_0_right = 0
    tx_list = []
    for _ in range(repeat):
        tx_list.append((random.random()*4, random.random()*4))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_16state_povm(tx)
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/repeat}')
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


def localization_onelevel_4sensor():
    '''4x4 grid, one level localization
    '''
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_onelevel_4state_povm()
    repeat = 100
    level_0_right = 0
    tx_list = []
    for _ in range(repeat):
        tx_list.append((random.random()*4, random.random()*4))
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_4state_povm(tx)
        if ret:
            level_0_right += 1
            right_x.append(tx[0])
            right_y.append(tx[1])
        else:
            wrong_x.append(tx[0])
            wrong_y.append(tx[1])
    print()

    print(f'accuracy = {level_0_right/repeat}')
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


def localization_onelevel_4sensor_discrete():
    '''4x4 grid, one level localization
    '''
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_onelevel_4state_povm()
    tx_list = []
    for x in range(4):
        for y in range(4):
            tx_list.append((x + 0.5, y + 0.5))
    
    level_0_right = 0
    right_x, right_y = [], []
    wrong_x, wrong_y = [], []
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        ret = ql.testing_onelevel_4state_povm(tx)
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



if __name__ == '__main__':
    # localization_onelevel_4sensor()
    localization_onelevel_4sensor_discrete()
    # localization_onelevel_12sensor()
    # localization_onelevel_12sensor_discrete()
    # localization_twolevel()

