'''
Quantum enhanced localization
'''

import pickle
import time
import numpy as np
import json
from utility import Utility
from unitary_operator import UnitaryOperator
from povm import Povm
from quantum_state import QuantumState
from qiskit.quantum_info.operators.operator import Operator


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

    def training_onelevel_fourstate_povm(self, initial_state: str):
        '''train the POVM for each set of sensors (similar to classifier) -- two levels
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
                tx1 = (a[0] + (b[0] - a[0])/4,   a[1] + 3*(b[1] - a[1])/4)
                tx2 = (a[0] + 3*(b[0] - a[0])/4, a[1] + (b[1] - a[1])/4)
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
                    self.povms[key] = {'povm': povm.operators, 'tx_loc':tx_loc}
                elif initial_state == 'optimal':
                    raise NotImplementedError('initial state optimization')
        print('training POVM done!')

    def check_correct(self, tx_truth: tuple, tx: tuple, grid_len: int) -> bool:
        x1 = int(tx_truth[0] / grid_len)
        y1 = int(tx_truth[1] / grid_len)
        x2 = int(tx[0] / grid_len)
        y2 = int(tx[1] / grid_len)
        if x1 == x2 and y1 == y2:
            return True
        else:
            return False

    def testing_twolevel_fourstate_povm(self, tx_truth: tuple, inital_state: str):
        '''currently only supports two level
        Args:
            tx            -- the location of the transmitter
            initial_state -- 'simple' or 'optimal'
        '''
        # print(f'tx={tx}', end='  ')
        # level 0, only has one set of sensors
        level_i = 0
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        evolve = 1
        for rx_i in set_['sensors']:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx_truth, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance)
            evolve = np.kron(evolve, uo)
        init_state = self.get_simple_initial_state(4)
        qstate = QuantumState(num_sensor=4, state_vector=np.dot(evolve, init_state))
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        probs = []
        for operator in povm['povm']:
            prob = np.trace(np.dot(operator.data, qstate.density_matrix))
            probs.append(prob)
        # print('level-0', probs)
        max_i = 0
        maxx = 0
        for i, prob in enumerate(probs):
            if prob > maxx:
                max_i = i
                maxx = prob
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, grid_len=2)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        min_distance = float('inf')
        mapping_set = 0
        for set_i in range(4):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level0, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        evolve = 1
        for rx_i in set_['sensors']:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx_truth, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance)
            evolve = np.kron(evolve, uo)
        init_state = self.get_simple_initial_state(4)
        qstate = QuantumState(num_sensor=4, state_vector=np.dot(evolve, init_state))
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        probs = []
        for operator in povm['povm']:
            prob = np.trace(np.dot(operator.data, qstate.density_matrix))
            probs.append(prob)
        # print('level-0', probs)
        max_i = 0
        maxx = 0
        for i, prob in enumerate(probs):
            if prob > maxx:
                max_i = i
                maxx = prob
        tx = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx, grid_len=1)
        print('level-2 tx', tx, level_1_correct)
        if level_0_correct is False and level_1_correct is True:
            raise Exception()
        return level_0_correct, level_1_correct

    def training_onelevel_16state_povm(self, file: str = ''):
        '''pretty good measurement, using a simple initial state
        '''
        if file != '':
            key = 'level-0-set-0'
            with open(file, 'rb') as f:
                self.povms[key] = pickle.load(f)
            return
        else:
            file = 'tmp-folder/16povm'

        povm = Povm()
        priors = [1/16] * 16
        txs = []
        tx_loc = {}
        for i in range(4):
            for j in range(4):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*4 + j] = (x, y)
        qstates = []
        sensors = sorted(self.sensordata['sensors'].keys())
        for tx in txs:
            evolve = 1
            for rx_i in sensors:  # rx_i is in str
                rx = self.sensordata['sensors'][rx_i]
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance)
                evolve = np.kron(evolve, uo)
            initial_state = self.get_simple_initial_state(len(sensors))
            qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state)))
        povm.pretty_good_measurement(qstates, priors, debug=False)
        key = 'level-0-set-0'
        self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        with open(file, 'wb') as f:
            pickle.dump(self.povms[key], f)
        print('training POVM done!')
    
    def testing_onelevel_16state_povm(self, tx_truth: tuple):
        '''single level 16 state discrimination
        '''
        sensors = sorted(self.sensordata['sensors'].keys())
        evolve = 1
        for rx_i in sensors:
            rx = self.sensordata['sensors'][rx_i]
            distance = Utility.distance(tx_truth, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance)
            evolve = np.kron(evolve, uo)
        initial_state = self.get_simple_initial_state(len(sensors))
        qstate = QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state))
        key = 'level-0-all'
        povm = self.povms[key]
        probs = []
        for operator in povm['povm']:
            prob = np.trace(np.dot(operator.data, qstate.density_matrix))
            probs.append(prob)
        max_i = 0
        maxx = 0
        for i, prob in enumerate(probs):
            if prob > maxx:
                max_i = i
                maxx = prob
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, grid_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct

    def training_onelevel_4state_povm(self):
        '''pretty good measurement, using a simple initial state
        '''
        povm = Povm()
        priors = [1/16] * 16
        txs = []
        tx_loc = {}
        for i in range(4):
            for j in range(4):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*4 + j] = (x, y)
        qstates = []
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        for tx in txs:
            evolve = 1
            for rx_i in sensors:  # rx_i is in str
                rx = self.sensordata['sensors'][f'{rx_i}']
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance)
                evolve = np.kron(evolve, uo)
            initial_state = self.get_simple_initial_state(len(sensors))
            qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state)))
        povm.pretty_good_measurement(qstates, priors, debug=False)
        key = f'level-{level_i}-set-{set_i}'
        self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        print('training POVM done!')
    
    def testing_onelevel_4state_povm(self, tx_truth: tuple):
        '''single level 4 state discrimination
        '''
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        evolve = 1
        for rx_i in sensors:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx_truth, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance)
            evolve = np.kron(evolve, uo)
        initial_state = self.get_simple_initial_state(len(sensors))
        qstate = QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state))
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        probs = []
        for operator in povm['povm']:
            prob = np.trace(np.dot(operator.data, qstate.density_matrix))
            probs.append(prob)
        max_i = 0
        maxx = 0
        for i, prob in enumerate(probs):
            if prob > maxx:
                max_i = i
                maxx = prob
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, grid_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct



