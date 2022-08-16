'''
Quantum enhanced localization
'''

import numpy as np
import json
from utility import Utility
from unitary_operator import UnitaryOperator
from povm import Povm
from quantum_state import QuantumState


class QuantumLocalization:
    def __init__(self, grid_length: int, cell_length: int, sensordata_filename: str, unitary_operator: UnitaryOperator):
        self.grid_length = grid_length               # assume the grid is a square, size is (grid_len, grid_len)
        self.cell_length = cell_length               # the length of grid cell
        self.unitary_operator = unitary_operator     # the model for unitary operator
        with open(sensordata_filename, 'r') as f:
            self.sensordata = json.load(f)
        self.povms = {}                              # the trained POVMs

    def get_simple_initial_state(self, num: int) -> np.array:
        '''get an initial state that all amplitudes are equal real numbers
        '''
        amplitude = np.sqrt(1/(2**num))
        return np.array([amplitude]*2**num)

    def training_fourstate_povm(self, initial_state: str):
        '''train the POVM for each set of sensors (similar to classifier)
           each POVM is doing a 4 state discrimination
        Args:
            initial_state -- 'simple' or 'optimal', different ways to get the initial state
        '''
        povm = Povm()
        priors = [1/4] * 4
        levels = self.sensordata['levels']
        for level, sets in levels.items():
            for set_i, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                info = f'level={level}, set={set_i}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                tx0 = (a[0] + (b[0] - a[0])/4,   a[1] + (b[1] - a[1])/4)
                tx1 = (a[0] + 3*(b[0] - a[0])/4, a[1] + (b[1] - a[1])/4)
                tx2 = (a[0] + (b[0] - a[0])/4,   a[1] + 3*(b[1] - a[1])/4)
                tx3 = (a[0] + 3*(b[0] - a[0])/4, a[1] + 3*(b[1] - a[1])/4)
                evolve_operators = []
                tx_loc = {}
                for i, tx in enumerate([tx0, tx1, tx2, tx3]):  # each tx leads to one evolve operator
                    tx_loc[i] = tx
                    evolve = 1
                    for rx_i in sensors:         # each evolve operator is a product state of some unitary operators
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        _, uo = self.unitary_operator.compute(distance)
                        evolve = np.kron(evolve, uo)
                    evolve_operators.append(evolve)
                if initial_state == 'simple':
                    init_state = self.get_simple_initial_state(4)
                    qstates = []
                    for evolve in evolve_operators:
                        qstates.append(QuantumState(num_sensor=4, state_vector=np.dot(evolve, init_state)))
                    povm.semidefinite_programming_minerror(qstates, priors, debug=False)
                    key = f'{level}-{set_i}'
                    self.povms[key] = {'povm': povm.operators, 'info':tx_loc}
                elif initial_state == 'optimal':
                    raise NotImplementedError('initial state optimization')
        print('training POVM done!')

    def testing_fourstate_povm(self, inital):
        pass