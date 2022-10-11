'''
Quantum enhanced localization
'''

import pickle
from typing import Tuple
import numpy as np
import json
from utility import Utility
from unitary_operator import UnitaryOperator
from povm import Povm
from quantum_state import QuantumState
from plot import Plot
from optimize_initstate import OptimizeInitialState
from default import Default
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

    def check_correct(self, tx_truth: tuple, tx: tuple, block_len: int) -> bool:
        '''for the case when the truth TX and the POVM location are not the same
           check if they are in the same block
        '''
        x1 = int(tx_truth[0] / block_len)
        y1 = int(tx_truth[1] / block_len)
        x2 = int(tx[0] / block_len)
        y2 = int(tx[1] / block_len)
        if x1 == x2 and y1 == y2:
            return True
        else:
            return False


    def training_twolevel_4state_4sensor(self, initial_state: str):
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

    def testing_twolevel_4state_4sensor(self, tx_truth: tuple, inital_state: str):
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
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=2)
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
        level_1_correct = self.check_correct(tx_truth, tx, block_len=1)
        print('level-2 tx', tx, level_1_correct)
        if level_0_correct is False and level_1_correct is True:
            raise Exception()
        return level_0_correct, level_1_correct


    def training_onelevel_16state_12sensor(self, file: str = ''):
        '''pretty good measurement, using a simple initial state
        '''
        if file != '':
            key = 'level-0-all'
            with open(file, 'rb') as f:
                self.povms[key] = pickle.load(f)
            return
        else:
            file = 'tmp-folder/onelevel_16povm.povm'

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
        key = 'level-0-all'
        self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        with open(file, 'wb') as f:
            pickle.dump(self.povms[key], f)
        print('training POVM done!')
    
    def testing_onelevel_16state_12sensor(self, tx_truth: tuple):
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
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        Plot.prob_heatmap(probs, n=4, filename=f'tmp-folder/truth={tx_truth}, pred={tx_level0}.png')
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct


    def training_onelevel_16x16grid(self, filename: str = ''):
        '''16x16 grid, 256 state, 10 sensors
           pretty good measurement
        '''
        if filename != '':
            key = 'level-0-set-0'
            with open(filename, 'rb') as f:
                self.povms[key] = pickle.load(f)
            return
        else:
            filename = 'tmp-folder/grid16_onelevel.povm'

        povm = Povm()
        priors = [1./256] * 256
        txs = []
        tx_loc = {}
        for i in range(16):
            for j in range(16):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[16*i + j] = (x, y)
        qstates = []
        level_i = 0
        set_i = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        for tx in txs:
            evolve = 1
            for rx_i in sensors:
                rx = self.sensordata['sensors'][f'{rx_i}']
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance)
                evolve = np.kron(evolve, uo)
            initial_state = self.get_simple_initial_state(len(sensors))
            state_vector = np.dot(evolve, initial_state)
            qstates.append(QuantumState(num_sensor=len(sensors), state_vector=state_vector))
        povm.pretty_good_measurement(qstates, priors, debug=False)
        key = f'level-{level_i}-set-{set_i}'
        self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        with open(filename, 'wb') as f:
            pickle.dump(self.povms[key], f)
        print('training POVM done')

    def testing_onelevel_16x16grid(self, tx_truth: tuple, grid_length: int):
        '''16x16 grid, one level 256 state discrimination, using set-0 in level-0
        '''
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        print(sum(probs))
        tx_level0 = povm['tx_loc'][max_i]
        # Plot.prob_heatmap(probs, n=grid_length, filename=f'tmp-folder/truth={tx_truth}, pred={tx_level0}.png')
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct


    def training_twolevel_16x16grid(self):
        '''train the POVM for each set of sensors (similar to classifier) -- two levels
           each POVM is doing a 16 state discrimination
        '''
        def get_16txloc(a: list, b: list) -> list:
            '''
            Args:
                a -- top left location
                b -- bottom right location
            Return:
                a list of 16 tx locations, each location is a tuple
            '''
            tx_list = []
            for i in range(4):
                for j in range(4):
                    tx = (a[0] + (2*i+1)*(b[0] - a[0])/8, a[1] + (2*j+1)*(b[1] - a[1])/8)
                    tx_list.append(tx)
            return tx_list

        povm = Povm()
        # 16 state discrimination, pretty good measurement
        priors = [1/16] * 16
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            for set_, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                info = f'level={level_}, set={set_}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                tx_list = get_16txloc(a, b)
                evolve_operators = []
                tx_loc = {}
                qstates = []
                init_state = self.get_simple_initial_state(num=len(sensors))
                for i, tx in enumerate(tx_list):  # each tx leads to one evolve operator
                    tx_loc[i] = tx
                    evolve = 1
                    for rx_i in sensors:          # each evolve operator is a product state of some unitary operators
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        disp, uo = self.unitary_operator.compute(distance)
                        evolve = np.kron(evolve, uo)
                    evolve_operators.append(evolve)
                    qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state)))
                povm.pretty_good_measurement(qstates, priors, debug=False)
                key = f'{level_}-{set_}'
                self.povms[key] = {'povm': povm.operators, 'tx_loc':tx_loc}
        print('training POVM done!')

    def testing_twolevel_16x16grid(self, tx_truth: tuple):
        '''currently only supports two level
        Args:
            tx            -- the location of the transmitter
            initial_state -- 'simple' or 'optimal'
        '''
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 4   # in level 0, locating a block that is 4x4
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        min_distance = float('inf')
        mapping_set = 0
        num_set = len(self.sensordata['levels'][f'level-1'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level0, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx, block_len=1)
        print('level-1 tx', tx, level_1_correct)
        if level_0_correct is False and level_1_correct is True:
            raise Exception()
        return level_0_correct, level_1_correct

    def testing_twolevel_16x16grid_plus(self, tx_truth: tuple):
        '''two level plus a confirmation (level-1.5)
        Args:
            tx            -- the location of the transmitter
            initial_state -- 'simple' or 'optimal'
        '''
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 4   # in level 0, locating a block that is 4x4
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        min_distance = float('inf')
        mapping_set = 0
        num_set = len(self.sensordata['levels'][f'level-{level_i}'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level0, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level1 = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
        print('level-1 tx', tx_level1, level_1_correct)
        
        # level 1.5 for block edge
        grid_length = 16
        if self.is_blockedge(tx_level1, grid_length, block_length):
            # step 1: get the set in level 1.5 according to tx_level1
            level_i = 1.5
            mapping_set = 0
            min_distance = float('inf')
            num_set = len(self.sensordata['levels'][f'level-{level_i}'])
            for set_i in range(num_set):
                set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
                a, b = set_['area']
                center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                distance = Utility.distance(tx_level1, center, 1)
                if distance < min_distance:
                    min_distance = distance
                    mapping_set = set_i
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
            # step 2: get the evolving operator and the quantum state
            sensors = set_['sensors']
            qstate = self.get_sensor_data(tx_truth, sensors)
            # step 3: compute the probabilities
            povm = self.povms[f'level-{level_i}-set-{mapping_set}']
            max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
            tx_level1 = povm['tx_loc'][max_i]
            level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
            print('level-1.5 tx', tx_level1, level_1_correct)
        return level_0_correct, level_1_correct


    def is_blockedge(self, tx, grid_length, block_length):
        '''currently excluding the "grid edge", only "block edge"
        '''
        m = grid_length // block_length  # number of blocks horizontally / vertically
        for i in range(1, m):
            if abs(tx[0] - i * block_length) < 1 and 2 < tx[0] < grid_length - 2 and 2 < tx[1] < grid_length - 2:
                return True
            if abs(tx[1] - i * block_length) < 1 and 2 < tx[0] < grid_length - 2 and 2 < tx[1] < grid_length - 2:
                return True
        return False


    def training_twolevel_15x15grid(self):
        '''train the POVM for each set of sensors (similar to classifier) -- two levels
           level-0 is doing 25 state discrimination
           level-1 is doing 9 state discrimination
        '''
        def get_25txloc(a: list, b: list) -> list:
            '''
            Args:
                a -- top left location
                b -- bottom right location
            Return:
                a list of 25 tx locations, each location is a tuple
            '''
            tx_list = []
            for i in range(5):
                for j in range(5):
                    tx = (a[0] + (2*i+1)*(b[0] - a[0]) / 10, a[1] + (2*j+1)*(b[1] - a[1]) / 10)
                    tx_list.append(tx)
            return tx_list

        def get_9txloc(a: list, b: list) -> list:
            '''
            Args:
                a -- top left location
                b -- bottom right location
            Return:
                a list of 9 tx locations, each location is a tuple
            '''
            tx_list = []
            for i in range(3):
                for j in range(3):
                    tx = (a[0] + (2*i+1)*(b[0] - a[0]) / 6, a[1] + (2*j+1)*(b[1] - a[1]) / 6)
                    tx_list.append(tx)
            return tx_list

        povm = Povm()
        # 16 state discrimination, pretty good measurement
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            if level_ == 'level-0':
                priors = [1/25] * 25
            else:
                priors = [1/9] * 9
            for set_, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                info = f'level={level_}, set={set_}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                if level_ == 'level-0':
                    tx_list = get_25txloc(a, b)
                else:
                    tx_list = get_9txloc(a, b)
                evolve_operators = []
                tx_loc = {}
                qstates = []
                init_state = self.get_simple_initial_state(num=len(sensors))
                for i, tx in enumerate(tx_list):  # each tx leads to one evolve operator
                    tx_loc[i] = tx
                    evolve = 1
                    for rx_i in sensors:          # each evolve operator is a product state of some unitary operators
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        _, uo = self.unitary_operator.compute(distance)
                        evolve = np.kron(evolve, uo)
                    evolve_operators.append(evolve)
                    qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state)))
                povm.pretty_good_measurement(qstates, priors, debug=False)
                key = f'{level_}-{set_}'
                self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        print('training POVM done!')

    def testing_twolevel_15x15grid(self, tx_truth: tuple):
        '''currently only supports two level
        Args:
            tx            -- the location of the transmitter
            initial_state -- 'simple' or 'optimal'
        '''
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 3   # in level 0, locating a block that is 3x3
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        min_distance = float('inf')
        mapping_set = 0
        num_set = len(self.sensordata['levels'][f'level-1'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level0, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx, block_len=1)
        print('level-1 tx', tx, level_1_correct)
        if level_0_correct is False and level_1_correct is True:
            raise Exception()
        return level_0_correct, level_1_correct


    def training_onelevel_16state_level_0_set_0(self):
        '''4x4 grid, pretty good measurement, using a simple initial state
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
    
    def testing_onelevel_16state_level_0_set_0(self, tx_truth: tuple, grid_length: int):
        '''4x4 grid, single level 4 state discrimination
        '''
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level0 = povm['tx_loc'][max_i]
        Plot.prob_heatmap(probs, n=grid_length, filename=f'tmp-folder/truth={tx_truth}, pred={tx_level0}.png')
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct


    def training_onelevel_16state_level_0_set_0_initstate(self):
        '''4x4 grid, pretty good measurement, optimize the initial state
        '''
        optimize_initstate = OptimizeInitialState(num_sensor=4)
        priors = [1/16] * 16
        txs = []
        tx_loc = {}
        for i in range(4):
            for j in range(4):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*4 + j] = (x, y)
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        num_sensor = len(sensors)
        evolution_operators = []
        for tx in txs:
            evolve = 1
            for rx_i in sensors:  # rx_i is in str
                rx = self.sensordata['sensors'][f'{rx_i}']
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance)
                evolve = np.kron(evolve, uo)
            evolution_operators.append(Operator(evolve))
        init_step = Default.init_step
        max_stuck = Default.max_stuck
        cooling_rate = Default.cooling_rate
        stepsize_decreasing_rate = Default.stepsize_decreasing_rate
        epsilon = Default.EPSILON
        initstate, operators = optimize_initstate.simulated_annealing(num_sensor, evolution_operators, priors, init_step,
                                                                      stepsize_decreasing_rate, epsilon, max_stuck, cooling_rate)
        key = f'level-{level_i}-set-{set_i}'
        self.povms[key] = {'init_state': initstate, 'povm': operators, 'tx_loc': tx_loc}
        print('training POVM done!')

    def testing_onelevel_16state_level_0_set_0_initstate(self, tx_truth: tuple, grid_length: int):
        '''4x4 grid, single level 4 state discrimination
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
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        initial_state = povm['init_state']
        qstate = QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state.state_vector))
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
        Plot.prob_heatmap(probs, n=grid_length, filename=f'tmp-folder/truth={tx_truth}, pred={tx_level0}.png')
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct


    def training_onelevel_36state_level_0_set_0(self):
        '''6x6 grid, pretty good measurement, using a simple initial state
        '''
        povm = Povm()
        priors = [1/36] * 36
        txs = []
        tx_loc = {}
        for i in range(6):
            for j in range(6):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*6 + j] = (x, y)
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

    def training_onelevel_36state_level_0_set_0_initstate(self):
        '''6x6 grid, pretty good measurement, optimize initial state using simulated annealing
        '''
        optimize_initstate = OptimizeInitialState(num_sensor=4)
        priors = [1/36] * 36
        txs = []
        tx_loc = {}
        for i in range(6):
            for j in range(6):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*6 + j] = (x, y)
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        num_sensor = len(sensors)
        evolution_operators = []
        for tx in txs:
            evolve = 1
            for rx_i in sensors:  # rx_i is in str
                rx = self.sensordata['sensors'][f'{rx_i}']
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance)
                evolve = np.kron(evolve, uo)
            evolution_operators.append(Operator(evolve))
        init_step = Default.init_step
        max_stuck = Default.max_stuck
        cooling_rate = Default.cooling_rate
        stepsize_decreasing_rate = Default.stepsize_decreasing_rate
        epsilon = Default.EPSILON
        initstate, operators = optimize_initstate.simulated_annealing(num_sensor, evolution_operators, priors, init_step,
                                                                      stepsize_decreasing_rate, epsilon, max_stuck, cooling_rate)
        key = f'level-{level_i}-set-{set_i}'
        self.povms[key] = {'init_state': initstate, 'povm': operators, 'tx_loc': tx_loc}
        print('training POVM done!')

    def testing_onelevel_36state_level_0_set_0(self, tx_truth: tuple, grid_length: int, opt_init_state: bool = False):
        '''6x6 grid, single level 36 state discrimination
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
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        if opt_init_state:
            init_state = povm['init_state']
            qstate = QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state.state_vector))
        else:
            init_state = self.get_simple_initial_state(len(sensors))
            qstate = QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state))
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
        Plot.prob_heatmap(probs, n=grid_length, filename=f'tmp-folder/truth={tx_truth}, pred={tx_level0}.png')
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        print('level 0 tx', tx_level0, level_0_correct)
        return level_0_correct


    def get_sensor_data(self, tx: tuple, sensors: list) -> QuantumState:
        '''Given the Tx and sensors, return the sensing data of the sensors, i.e., a quantum state of sensors
           Assuming a simple initial state
        Args:
            tx -- tx location
            sensors -- a list of sensor index
        Return:
            the QuantumState of the sensors
        '''
        evolve = 1
        for rx_i in sensors:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance)
            evolve = np.kron(evolve, uo)
        init_state = self.get_simple_initial_state(num=len(sensors))
        return QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state))

    def measure_maxprob_index(self, qstate: QuantumState, povm: list) -> Tuple[int, list]:
        '''do measurement using POVM and get the max probability
        Args:
            qstate -- the quantum sensing data
            povm   -- a list of measurement operators
        Return:
            the index of the max probability, also the list of probabilities
        '''
        probs = []
        for operator in povm:
            prob = np.trace(np.dot(operator.data, qstate.density_matrix))
            probs.append(prob)
        max_i = 0
        maxx = 0
        for i, prob in enumerate(probs):
            if prob > maxx:
                max_i = i
                maxx = prob
        return max_i, probs


    def training_threelevel_16x16grid(self):
        '''train the POVM for each set of sensors (similar to classifier) -- two levels
           each POVM is doing a 16 state discrimination
        '''
        def get_16txloc(a: list, b: list) -> list:
            '''
            Args:
                a -- top left location
                b -- bottom right location
            Return:
                a list of 16 tx locations, each location is a tuple
            '''
            tx_list = []
            for i in range(4):
                for j in range(4):
                    tx = (a[0] + (2*i+1)*(b[0] - a[0])/8, a[1] + (2*j+1)*(b[1] - a[1])/8)
                    tx_list.append(tx)
            return tx_list

        def get_4txloc(a: list, b: list) -> list:
            '''
            Args:
                a -- top left location
                b -- bottom right location
            Return:
                a list of 4 tx locations, each location is a tuple
            '''
            tx_list = []
            for i in range(2):
                for j in range(2):
                    tx = (a[0] + (2*i+1)*(b[0] - a[0])/4, a[1] + (2*j+1)*(b[1] - a[1])/4)
                    tx_list.append(tx)
            return tx_list

        # level-0: 4  state discrimination
        # level-1: 4  state discrimination
        # level-2: 16 state discrimination

        povm = Povm()
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            for set_, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                info = f'level={level_}, set={set_}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                if level_ == 'level-0' or level_ == 'level-1':
                    tx_list = get_4txloc(a, b)
                    priors = [1/4] * 4
                else:
                    tx_list = get_16txloc(a, b)
                    priors = [1/16] * 16
                tx_loc = {}
                qstates = []
                init_state = self.get_simple_initial_state(num=len(sensors))
                for i, tx in enumerate(tx_list):  # each tx leads to one evolve operator
                    tx_loc[i] = tx
                    evolve = 1
                    for rx_i in sensors:          # each evolve operator is a product state of some unitary operators
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        _, uo = self.unitary_operator.compute(distance)
                        evolve = np.kron(evolve, uo)
                    qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state)))
                povm.pretty_good_measurement(qstates, priors, debug=False)
                # povm.semidefinite_programming_minerror(qstates, priors, debug=False)
                key = f'{level_}-{set_}'
                self.povms[key] = {'init_state': init_state, 'povm': povm.operators, 'tx_loc': tx_loc}
        print('training POVM done!')

    def testing_threelevel_16x16grid(self, tx_truth: tuple):
        '''three level
        Args:
            tx -- the location of the transmitter
        '''
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 8   # in level 0, locating a block that is 8x8
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        block_length = 4   # in level 1, locating a block that is 4x4
        min_distance = float('inf')
        mapping_set = 0
        num_set = len(self.sensordata['levels'][f'level-{level_i}'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level0, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        tx_level1 = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=block_length)
        print('level-1 tx', tx_level1, level_1_correct)
        
        # level 2
        # step 1: get the set in level 2 according to tx_level1
        level_i = 2
        block_length = 1   # in level 2, locating a block that is 1x1, i.e., a cell
        min_distance = float('inf')
        mapping_set = 0
        num_set = len(self.sensordata['levels'][f'level-{level_i}'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            center = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            distance = Utility.distance(tx_level1, center, 1)
            if distance < min_distance:
                min_distance = distance
                mapping_set = set_i
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])

        tx_level2 = povm['tx_loc'][max_i]
        level_2_correct = self.check_correct(tx_truth, tx_level2, block_len=block_length)
        print('level-2 tx', tx_level1, level_2_correct)

        return level_0_correct, level_1_correct, level_2_correct
