'''
Quantum enhanced localization
'''

import math
import numpy as np
import json
import torch
import os
import pickle
import torchquantum as tq
from typing import Tuple
from bisect import bisect_left
from itertools import accumulate
from collections import Counter
from torch.utils.data import DataLoader
from utility import Utility
from unitary_operator import UnitaryOperator
from povm import Povm
from quantum_state import QuantumState
from default import Default
from qnn import QuantumSensing, QuantumML0
from dataset import QuantumSensingDataset



class QuantumLocalization:
    ''' Assumption 1: dividing a N x N grid into sqrt(N) row sqrt(N) column of blocks, where each block is sqrt(N) x sqrt(N)
                    So the number of tx equals sqrt(N) x sqrt(N) = N = grid_length
    '''
    def __init__(self, grid_length: int, cell_length: int, sensordata: str, unitary_operator: UnitaryOperator):
        self.grid_length = grid_length               # assume the grid is a square, size is (grid_len, grid_len)
        self.cell_length = cell_length               # the length of grid cell
        self.unitary_operator = unitary_operator     # the model for unitary operator
        with open(sensordata, 'r') as f:
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


    def is_blockedge(self, tx, grid_length, block_length):
        '''currently excluding the "grid edge", only "block edge"
        '''
        m = grid_length // block_length  # number of blocks horizontally / vertically
        for i in range(1, m):
            if abs(tx[0] - i * block_length) < 1:
                return True
            if abs(tx[1] - i * block_length) < 1:
                return True
        return False


    def get_sensor_data(self, tx: tuple, sensors: list, noise: bool = False) -> QuantumState:
        '''Given the Tx and sensors, return the sensing data of the sensors, i.e., a quantum state of sensors
           Assuming a simple initial state
        Args:
            tx -- tx location
            sensors -- a list of sensor index
            noise -- noise or no noise
        Return:
            the QuantumState of the sensors
        '''
        evolve = 1
        for rx_i in sensors:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx, rx, self.cell_length)
            _, uo = self.unitary_operator.compute(distance, noise)
            evolve = np.kron(evolve, uo)
        init_state = self.get_simple_initial_state(num=len(sensors))
        return QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state))


    def get_sensor_data_qml(self, tx: tuple, sensors: list, noise: bool = False) -> Tuple:
        '''Given the Tx and sensors, return the sensing data of the sensors, i.e., a quantum state of sensors
           Assuming a simple initial state
        Args:
            tx -- tx location
            sensors -- a list of sensor index
            noise -- noise or no noise
        Return:
            tq.QuantumDevice, tq.QuantumState
        '''
        # step 1: get the phases
        thetas = []
        for rx_i in sensors:
            rx = self.sensordata['sensors'][f'{rx_i}']
            distance = Utility.distance(tx, rx, self.cell_length)
            phase_shift, _ = self.unitary_operator.compute(distance, noise=noise)
            thetas.append(phase_shift)
        bsz = 1
        thetas = torch.Tensor([thetas])  # add a batch dimension
        n_qubits = len(sensors)
        qstate = tq.QuantumState(n_wires=n_qubits, bsz=bsz)
        use_cuda = torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=thetas, device=device)
        qsensing(qstate)
        q_device = tq.QuantumDevice(n_wires=n_qubits)
        q_device.reset_states(bsz=bsz)
        return q_device, qstate


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


    def sense_early_stop(self, count: Counter):
        values = sorted(list(count.values()), reverse=True)
        summ = sum(values)
        if values[0] > summ / 2 or values[0] > values[1] * 1.5:
            return True
        return False


    def sense_measure_index(self, tx: tuple, sensors: list, povm: list, repeat: int, early_stop: bool) -> Tuple[int, list]:
        '''the quantum sensing protocol
        '''
        count = Counter()
        for it in range(repeat):
            qstate = self.get_sensor_data(tx, sensors, noise=True)
            probs = []
            for operator in povm:
                prob = np.trace(np.dot(operator.data, qstate.density_matrix))
                probs.append(prob.real if prob.real > 0 else 0)    # ignore the negative real numbers...
            cumulate = list(accumulate(probs))
            maxx = max(cumulate)
            pick = np.random.uniform(0, maxx)
            i = bisect_left(cumulate, pick)
            if Default.DEBUG and it % 100 == 0:
                print(f'{it}, probs = {[round(p, 3) for p in probs]}, max = {maxx:0.5f}, pick = {pick:0.5f}, i = {i}')
            count[i] += 1
            # early stop
            if early_stop and it % 100 == 99 and it >= 400 and self.sense_early_stop(count):
                break

        max_i = -1
        maxx  = -1
        for i, c in count.items():
            if c > maxx:
                maxx = c
                max_i = i
        return max_i, count


    def train_povmloc_one(self):
        '''train the one level POVM localization method
        '''
        povm = Povm()
        txs = []
        tx_loc = {}
        for i in range(self.grid_length):     # the transmitter locations
            for j in range(self.grid_length):
                x = i + 0.5
                y = j + 0.5
                txs.append((x, y))
                tx_loc[i*self.grid_length + j] = (x, y)
        qstates = []                          # the quantum states for discrimination
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        for tx in txs:
            evolve = 1
            for rx_i in sensors:  # rx_i is in str
                rx = self.sensordata['sensors'][f'{rx_i}']
                distance = Utility.distance(tx, rx, self.cell_length)
                _, uo = self.unitary_operator.compute(distance, noise=False)  # assume noise is zero during training
                evolve = np.kron(evolve, uo)
            initial_state = self.get_simple_initial_state(len(sensors))
            qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, initial_state)))
        priors = [1/len(qstates)] * len(qstates)
        povm.pretty_good_measurement(qstates, priors, debug=False)
        key = f'level-{level_i}-set-{set_i}'
        self.povms[key] = {'povm': povm.operators, 'tx_loc': tx_loc}
        print('training POVM done!')


    def povmloc_one(self, tx_truth: tuple, continuous: bool = False) -> tuple:
        '''Localization using a single level POVM
           If discrete,   return (bool, (x, y))
           If continuous, return (bool, float, (x, y)) -- (correct/wrong, localization error, predicted location)
        '''
        seed = int(tx_truth[0]) * self.grid_length + int(tx_truth[1])
        np.random.seed(seed)
        level_i = 0
        set_i   = 0
        set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_data['sensors']
        key = f'level-{level_i}-set-{set_i}'
        povm = self.povms[key]
        early_stop = True if len(sensors) >= 8 else False
        max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], repeat=Default.repeat, early_stop=early_stop)
        print(f'({round(tx_truth[0], 3)}, {round(tx_truth[1], 3)})', sorted(list(freqs.items()), key=lambda x: -x[1])[:4], end='; ')
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=1)
        if not continuous:
            print('level-0 tx', tx_level0, level_0_correct)
            return level_0_correct, tx_level0
        else:
            print('level-0 tx', tx_level0, level_0_correct, end='; ')
            level_0_locerror = Utility.distance(tx_truth, tx_level0, Default.cell_length)
            print('level-0 tx', tx_level0, round(level_0_locerror, 3))
            return level_0_correct, level_0_locerror, tx_level0


    def get_txloc(self, a: tuple, b: tuple, block_cell_ratio: float) -> list:
        '''get the tx locations during the training phase
        Args:
            a           -- top left corner
            b           -- bottom right corner
            block_cell_ratio -- the ratio of block to cell in length
        Return:
            a list of 2D location tuples
        '''
        row = int((b[0] - a[0]) / block_cell_ratio + 10**-6)
        col = int((b[1] - a[1]) / block_cell_ratio + 10**-6)
        tx_list = []
        for i in range(row):
            for j in range(col):
                tx = (a[0] + (2*i+1)*(b[0] - a[0])/(2*row), a[1] + (2*j+1)*(b[1] - a[1])/(2*col))
                tx_list.append(tx)
        return tx_list


    def filter_tx(self, a: tuple, b: tuple, tx_list: tuple):
        '''filter the tx_list if (a, b) is a block at the edge of the grid
        '''
        epsilon = 10**-6
        if abs(a[0]) < epsilon:
            c = (a[1] + b[1]) / 2
            return [tx for tx in tx_list if tx[0] < 2 and (c-1 < tx[1] < c+1)]
        if abs(b[0] - self.grid_length) < epsilon:
            c = (a[1] + b[1]) / 2
            return [tx for tx in tx_list if tx[0] > self.grid_length - 2 and (c-1 < tx[1] < c+1)]
        if abs(a[1]) < epsilon:
            c = (a[0] + b[0]) / 2
            return [tx for tx in tx_list if tx[1] < 2 and (c-1 < tx[0] < c+1)]
        if abs(b[1] - self.grid_length) < epsilon:
            c = (a[0] + b[0]) / 2
            return [tx for tx in tx_list if tx[1] > self.grid_length - 2 and (c-1 < tx[0] < c+1)]
        return tx_list


    def train_povmloc(self):
        '''training the POVMs for two level POVMLoc, including POVMLoc and POVMLoc Pro
        '''
        povm = Povm()
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            for set_, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                block_cell_ratio = set_data['block_cell_ratio']
                info = f'level={level_}, set={set_}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                tx_list = self.get_txloc(a, b, block_cell_ratio)
                if level_ == 'level-1.5':
                    tx_list = self.filter_tx(a, b, tx_list)
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
                        disp, uo = self.unitary_operator.compute(distance, noise=False)  # training has no noise
                        evolve = np.kron(evolve, uo)
                    evolve_operators.append(evolve)
                    qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state)))
                priors = [1 / len(qstates)] * len(qstates)    # equal prior
                povm.pretty_good_measurement(qstates, priors, debug=False)
                key = f'{level_}-{set_}'
                self.povms[key] = {'povm': povm.operators, 'tx_loc':tx_loc}
        print('training POVM done!')


    def povmloc(self, tx_truth: tuple, continuous: bool = False) -> tuple:
        '''the two level POVM-Loc
        Args:
            tx         -- the location of the transmitter
            continuous -- during the testing phase, whether the TX is continuous or not. The difference is in the output only
        Return:
           If discrete,   return (bool, (x, y))
           If continuous, return (bool, float, (x, y)) -- (correct/wrong, localization error, predicted location)
        '''
        seed = int(tx_truth[0]) * self.grid_length + int(tx_truth[1])
        np.random.seed(seed)
        # level 0, only has one set of sensors
        block_length = int(math.sqrt(self.grid_length) + 10**-6)  # based on Assumption 1
        level_i = 0
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        # the sensing protocol
        max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=True)
        print(f'({round(tx_truth[0], 3)}, {round(tx_truth[1], 3)})', sorted(list(freqs.items()), key=lambda x: -x[1])[:4], end='; ')
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct, end='; ')
        
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
        # step 2: the sensing protocol
        sensors = set_['sensors']
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)
        tx_level1 = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
        if not continuous:
            print('level-1 tx', tx_level1, level_1_correct)
            return level_1_correct, tx_level1
        else:
            print('level-1 tx', tx_level1, level_1_correct, end='; ')
            level_1_locerror = Utility.distance(tx_truth, tx_level1, Default.cell_length)
            print('level-1 tx', tx_level1, round(level_1_locerror, 3))
            return level_1_correct, level_1_locerror, tx_level1


    def povmloc_pro(self, tx_truth: tuple, continuous: bool = False) -> tuple:
        '''the two level POVM-Loc Pro, it do another POVM for block edge cases
        Args:
            tx         -- the location of the transmitter
            continuous -- during the testing phase, whether the TX is continuous or not. The difference is in the output only
        Return:
           If discrete,   return (bool, (x, y))
           If continuous, return (bool, float, (x, y)) -- (correct/wrong, localization error, predicted location)
        '''
        seed = int(tx_truth[0]) * self.grid_length + int(tx_truth[1])
        np.random.seed(seed)
        # level 0, only has one set of sensors
        block_length = int(math.sqrt(self.grid_length) + 10**-6)   # based on Assumption 1
        level_i = 0
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        # the sensing protocol
        max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=True)
        print(f'({round(tx_truth[0], 3)}, {round(tx_truth[1], 3)})', sorted(list(freqs.items()), key=lambda x: -x[1])[:4], end='; ')
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct, end='; ')
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        mapping_set = -1
        num_set = len(self.sensordata['levels'][f'level-{level_i}'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            if a[0] <= tx_level0[0] <= b[0] and a[1] <= tx_level0[1] <= b[1]:
                    mapping_set = set_i
                    break
        else:
            raise Exception('Error in level 1!')
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: the sensing protocol
        sensors = set_['sensors']
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']
        max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)
        tx_level1 = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
        print('level-1 tx', tx_level1, level_1_correct, end='; ')
        
        # level 1.5 for block edge
        if self.is_blockedge(tx_level1, self.grid_length, block_length):
            # step 1: get the set in level 1.5 according to tx_level1
            level_i = 1.5
            mapping_set = -1
            num_set = len(self.sensordata['levels'][f'level-{level_i}'])
            for set_i in range(num_set):
                set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
                a, b = set_['area']
                if a[0] <= tx_level1[0] <= b[0] and a[1] <= tx_level1[1] <= b[1]:
                    mapping_set = set_i
                    break
            else:
                raise Exception('Error in level 1.5!')
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
            # step 2: the sensing protocol
            sensors = set_['sensors']
            povm = self.povms[f'level-{level_i}-set-{mapping_set}']
            max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)            
            tx_level1 = povm['tx_loc'][max_i]
            # print(tx_truth, sorted(list(freqs.items()), key=lambda x: -x[1])[:4], end='; ')
            level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
            if not continuous:
                print('level-1.5 tx', tx_level1, level_1_correct)
                return level_1_correct, tx_level1
            else:
                print('level-1.5 tx', tx_level1, level_1_correct, end='; ')
                level_1_locerror = Utility.distance(tx_truth, tx_level1, Default.cell_length)
                print('level-1.5 tx', tx_level1, round(level_1_locerror, 3))
                return level_1_correct, level_1_locerror, tx_level1
        if not continuous:
            print()
            return level_1_correct, tx_level1
        else:
            level_1_locerror = Utility.distance(tx_truth, tx_level1, Default.cell_length)
            print('error', round(level_1_locerror, 3))
            return level_1_correct, level_1_locerror, tx_level1


    def train_quantum_ml(self, root_dir: str, generate_data: bool):
        '''train the one level quantum machine learning model
        Args:
            root_dir -- the root directory of the training data
            generate -- True is generate new training data; False if use existing training data
        '''
        # step 1: generate simulated training data (also the testing data)
        if generate_data:
            Utility.remove_make(root_dir)
            train_phase_dir = os.path.join(root_dir, 'train', 'phase')
            train_label_dir = os.path.join(root_dir, 'train', 'label')
            test_phase_dir = os.path.join(root_dir, 'test', 'phase')
            test_label_dir = os.path.join(root_dir, 'test', 'label')
            os.makedirs(train_phase_dir)
            os.makedirs(train_label_dir)
            os.makedirs(test_phase_dir)
            os.makedirs(test_label_dir)
            txs = []
            tx_loc = {}
            for i in range(self.grid_length):     # the transmitter locations
                for j in range(self.grid_length):
                    x = i + 0.5
                    y = j + 0.5
                    txs.append((x, y))
                    tx_loc[i*self.grid_length + j] = (x, y)
            level_i = 0
            set_i   = 0
            set_data = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            sensors = set_data['sensors']
            repeat = 15
            counter = 0
            for i, tx in enumerate(txs):
                for _ in range(repeat):
                    thetas = []
                    for rx_i in sensors:  # rx_i is in str
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        phase_shift, _ = self.unitary_operator.compute(distance, noise=True)  # there is noise for quantum ml
                        thetas.append(phase_shift)
                    np.save(f'{train_phase_dir}/{counter}.npy', np.array(thetas).astype(np.float32))
                    np.save(f'{train_label_dir}/{counter}.npy', np.array(i).astype(np.int64))
                    counter += 1
            repeat = 5
            counter = 0
            for i, tx in enumerate(txs):
                for _ in range(repeat):
                    thetas = []
                    for rx_i in sensors:  # rx_i is in str
                        rx = self.sensordata['sensors'][f'{rx_i}']
                        distance = Utility.distance(tx, rx, self.cell_length)
                        phase_shift, _ = self.unitary_operator.compute(distance, noise=True)  # there is noise for quantum ml
                        thetas.append(phase_shift)
                    np.save(f'{test_phase_dir}/{counter}.npy', np.array(thetas).astype(np.float32))
                    np.save(f'{test_label_dir}/{counter}.npy', np.array(i).astype(np.int64))
                    counter += 1
        else:
            if os.path.exists(root_dir) is False:
                raise Exception(f'directory {root_dir} does not exist')
        
        # step 2: train the quantum ml model
        # training the quantum ml part is done on a jupyter notebook        
        print('training POVM done!')


    def train_quantum_ml_two(self, root_dir: str):
        '''train the two level quantum machine learning model
        Args:
            root_dir -- the root directory of the training data
        '''
        Utility.remove_make(root_dir)
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            for set_, set_data in sets.items():
                key = f'{level_}-{set_}'
                train_phase_dir = os.path.join(root_dir, key, 'train', 'phase')
                train_label_dir = os.path.join(root_dir, key, 'train', 'label')
                info_dir = os.path.join(root_dir, key)
                os.makedirs(train_phase_dir)
                os.makedirs(train_label_dir)
                sensors = set_data['sensors']
                area = set_data['area']
                block_cell_ratio = set_data['block_cell_ratio']
                info = {'level':level_, 'set': set_, 'sensors': sensors, 'sensor_num': len(sensors), 
                        'area': area, 'block_cell_ratio': block_cell_ratio}
                info_file = os.path.join(info_dir, 'info')
                with open(info_file, 'w') as f:
                    json.dump(info, f)
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                tx_list = self.get_txloc(a, b, block_cell_ratio)
                repeat = 75
                counter = 0
                for i, tx in enumerate(tx_list):
                    for _ in range(repeat):
                        thetas = []
                        for rx_i in sensors:
                            rx = self.sensordata['sensors'][f'{rx_i}']
                            distance = Utility.distance(tx, rx, self.cell_length)
                            phase_shift, _ = self.unitary_operator.compute(distance, noise=True)
                            thetas.append(phase_shift)
                        np.save(f'{train_phase_dir}/{counter}.npy', np.array(thetas).astype(np.float32))
                        np.save(f'{train_label_dir}/{counter}.npy', np.array(i).astype(np.int64))
                        counter += 1
        print('Generating data done!')


    def qml_two(self, tx_truth: tuple, root_dir: str, continuous: bool = False) -> tuple:
        '''
        Args:
            tx         -- the location of the transmitter
            root_dir   -- the root directory of the training data
            continuous -- during the testing phase, whether the TX is continuous or not. The difference is in the output only
        Return:
           If discrete,   return (bool, (x, y))
           If continuous, return (bool, float, (x, y)) -- (correct/wrong, localization error, predicted location)
        '''
        seed = int(tx_truth[0]) * self.grid_length + int(tx_truth[1])
        np.random.seed(seed)
        # block_length = int()
        level_i = 0
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        area = set_['area']
        block_cell_ratio = set_['block_cell_ratio']
        block_length = (area[1][0] - area[0][0]) // block_cell_ratio
        sensors = set_['sensors']
        # prepare model
        level_i = 0
        set_i = 0
        model_dir = os.path.join(os.getcwd(), root_dir.replace('data', 'model'), f'level-{level_i}-set-{set_i}')
        model_file = os.path.join(model_dir, 'model.pt')
        if os.path.exists(model_file) is False:
            raise Exception(f'model does not exist: {model_file}')
        with open(model_file, 'rb') as f:
            use_cuda = torch.cuda.is_available()
            device = torch.device('cuda' if use_cuda else 'cpu')
            model = pickle.load(f)
            model.to(device)
            model.eval()
        # prepare sensing data
        q_device, qstate = self.get_sensor_data_qml(tx_truth, sensors, noise=True)
        # feed the data into the model
        output = model(q_device, qstate.states)
        output = output.cpu().detach().numpy()
        print(output)
        print(np.argmax(output))


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
        levels = self.sensordata['levels']
        for level_, sets in levels.items():
            for set_, set_data in sets.items():
                sensors = set_data['sensors']
                area = set_data['area']
                info = f'level={level_}, set={set_}, sensors={sensors}, area={area}'
                print(info)
                a, b = area[0], area[1]  # a is top left, b is bottom right
                tx_list = get_16txloc(a, b)
                if level_ == 'level-1.5':
                    tx_list = self.filter_tx(a, b, tx_list)
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
                        disp, uo = self.unitary_operator.compute(distance, noise=False)  # training has no noise
                        evolve = np.kron(evolve, uo)
                    evolve_operators.append(evolve)
                    qstates.append(QuantumState(num_sensor=len(sensors), state_vector=np.dot(evolve, init_state)))
                priors = [1 / len(qstates)] * len(qstates)    # equal prior
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
        seed = int(tx_truth[0]) * 16 + int(tx_truth[1])
        np.random.seed(seed)
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 4   # in level 0, locating a block that is 4x4
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        
        # shortcut way
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        # the sensing protocol
        # max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=True)
        # print(tx_truth, sorted(list(freqs.items()), key=lambda x: -x[1])[:4], end='; ')
        # if max_i_theory != max_i:
        #     print(f'level_0 theory: {max_i_theory}, simulation: {max_i}')

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
        
        # shortcut way
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        # the sensing protocol
        # max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)
        # if max_i_theory != max_i:
        #     print(f'level_1 theory: {max_i_theory}, simulation: {max_i}')

        tx = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx, block_len=1)
        print('level-1 tx', tx, level_1_correct)
        if level_0_correct is False and level_1_correct is True:
            raise Exception()
        return level_0_correct, level_1_correct

    def testing_twolevel_16x16grid_pro(self, tx_truth: tuple):
        '''two level plus a confirmation (level-1.5)
        Args:
            tx            -- the location of the transmitter
            initial_state -- 'simple' or 'optimal'
        '''
        seed = int(tx_truth[0]) * 16 + int(tx_truth[1])
        np.random.seed(seed)
        # level 0, only has one set of sensors
        level_i = 0
        block_length = 4   # in level 0, locating a block that is 4x4
        set_i = 0
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
        sensors = set_['sensors']
        povm = self.povms[f'level-{level_i}-set-{set_i}']
        
        # shortcut way
        qstate = self.get_sensor_data(tx_truth, sensors)
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        # the sensing protocol
        # max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=True)
        # if max_i_theory != max_i:
        #     print(f'level_0 theory: {max_i_theory}, simulation: {max_i}')
       
        tx_level0 = povm['tx_loc'][max_i]
        level_0_correct = self.check_correct(tx_truth, tx_level0, block_len=block_length)
        print('level-0 tx', tx_level0, level_0_correct)
        
        # level 1
        # step 1: get the set in level 1 according to tx_level0
        level_i = 1
        mapping_set = -1
        num_set = len(self.sensordata['levels'][f'level-{level_i}'])
        for set_i in range(num_set):
            set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
            a, b = set_['area']
            if a[0] <= tx_level0[0] <= b[0] and a[1] <= tx_level0[1] <= b[1]:
                    mapping_set = set_i
                    break
        else:
            raise Exception('Error in level 1!')
        set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{mapping_set}']
        # step 2: get the evolving operator and the quantum state
        sensors = set_['sensors']
        qstate = self.get_sensor_data(tx_truth, sensors)
        # step 3: compute the probabilities
        povm = self.povms[f'level-{level_i}-set-{mapping_set}']

        # the shortcut way
        max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
        # the sensing protocol
        # max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)
        # if max_i_theory != max_i:
        #     print(f'level_1 theory: {max_i_theory}, simulation: {max_i}')

        tx_level1 = povm['tx_loc'][max_i]
        level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
        print('level-1 tx', tx_level1, level_1_correct)
        
        # level 1.5 for block edge
        grid_length = 16
        if self.is_blockedge(tx_level1, grid_length, block_length):
            # step 1: get the set in level 1.5 according to tx_level1
            level_i = 1.5
            mapping_set = -1
            num_set = len(self.sensordata['levels'][f'level-{level_i}'])
            for set_i in range(num_set):
                set_ = self.sensordata['levels'][f'level-{level_i}'][f'set-{set_i}']
                a, b = set_['area']
                if a[0] <= tx_level1[0] <= b[0] and a[1] <= tx_level1[1] <= b[1]:
                    mapping_set = set_i
                    break
            else:
                raise Exception('Error in level 1.5!')
            # step 2: get the evolving operator and the quantum state
            sensors = set_['sensors']
            qstate = self.get_sensor_data(tx_truth, sensors)
            # step 3: compute the probabilities
            povm = self.povms[f'level-{level_i}-set-{mapping_set}']
            
            # the shortcut way
            max_i, probs = self.measure_maxprob_index(qstate, povm['povm'])
            # the sensing protocol
            # max_i, freqs = self.sense_measure_index(tx_truth, sensors, povm['povm'], Default.repeat, early_stop=False)
            # if max_i_theory != max_i:
            #     print(f'level_1.5 theory: {max_i_theory}, simulation: {max_i}')
            
            tx_level1 = povm['tx_loc'][max_i]
            level_1_correct = self.check_correct(tx_truth, tx_level1, block_len=1)
            print('level-1.5 tx', tx_level1, level_1_correct)
        return level_0_correct, level_1_correct

