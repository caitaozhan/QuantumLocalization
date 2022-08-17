'''for testing purpose
'''

import random
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator


def test_localization():
    random.seed(3)
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    initial_state = 'simple'
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_fourstate_povm(initial_state)
    # tx_list = [(1, 1)]
    repeat = 1000
    level_0_correct = 0
    level_1_correct = 0
    tx_list = []
    for _ in range(repeat):
        # tx_list.append((1 + (2*random.random()-1)/2, 1 + (2*random.random()-1)/2))
        # tx_list.append((1 + (2*random.random()-1)/10, 1 + (2*random.random()-1)/10))
        tx_list.append((random.random()*4, random.random()*4))
    for i, tx in enumerate(tx_list):
        print(f'{i}, truth tx = ({tx[0]:.2f}, {tx[1]:.2f})')
        # print(f'distance={Utility.distance((1, 1), tx, Default.cell_length):.3f}', end=' ')
        ret0, ret1 = ql.testing_fourstate_povm(tx, initial_state)
        if ret0:
            level_0_correct += 1
            if ret1:
                level_1_correct += 1
        print()
    print(f'level-0 accuracy={level_0_correct/repeat}')
    print(f'level-1 accuracy={level_1_correct/repeat}')

if __name__ == '__main__':
    test_localization()
