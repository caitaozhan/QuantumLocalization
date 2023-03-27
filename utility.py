'''
some utility tools
'''

import os
import shutil
import numpy as np
import json
from typing import Union
from default import Default
from typing import List
from input_output import Input, Output


class Utility:

    @staticmethod
    def norm_squared(alpha: complex) -> float:
        '''
        Args:
            alpha -- the amplitude for an element in the state vector
        Return:
            the norm squared of a complex number, i.e. alpha * alpha.complex_conjugate
        '''
        return abs(alpha)**2


    @staticmethod
    def print_matrix(describe: str, matrix: np.array):
        '''print a matrix with complex values elegantly
        '''
        print(describe)
        for row in matrix:
            for item in row:
                real = f'{item.real:.5f}'
                imag = f'{item.imag:.5f}'
                if imag[0] != '-':
                    imag = '+' + imag
                print(f'({real:>8}{imag:>8}i)', end=' ')
            print()


    @staticmethod
    def distance(loc1: Union[list, tuple], loc2: Union[list, tuple], length: float) -> float:
        '''return the distance between loc1 and loc2
        '''
        return length * np.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)


    @staticmethod
    def check_zero(matrix) -> bool:
        '''check if a matrix contains all zero entries
        Args:
            matrix -- np.array -- the matrix to be checked
        Return:
            bool -- True if all elements in the matrix are zero, False otherwise
        '''
        matrix = np.abs(matrix)
        maxx = np.max(matrix)
        if maxx < Default.EPSILON_SEMIDEFINITE:
            return True
        else:
            return False


    @staticmethod
    def check_optimal(quantum_states: list, priors: list, povms: list) -> bool:
        '''check the optimality for minimum error povm
        Args:
            quantum_states -- a list of QuantumState objects
            priors         -- a list of prior probabilities
            povms          -- a list of Operator objects
        Return:
            bool -- True if povms are, False otherwise
        '''
        if not (len(quantum_states) == len(priors) == len(povms)):
            raise Exception('error in input, the input parameters do not have equal length')
        
        length = len(quantum_states)
        for i in range(length):
            for j in range(i+1, length):
                Pii  = povms[i].data
                Pij  = povms[j].data
                pi   = priors[i]
                pj   = priors[j]
                rhoi = quantum_states[i].density_matrix
                rhoj = quantum_states[j].density_matrix
                product = np.dot(Pii, np.dot(pi*rhoi - pj*rhoj, Pij))
                if Utility.check_zero(product) == False:
                    return False
        return True


    @staticmethod
    def read_logs(logs: List[str]) -> List:
        '''
        Args:
            logs -- a list of filenames
        Return:
            data -- List[Tuple('Input', Dict[str, 'Output'])]
        '''
        data = []
        for log in logs:
            f = open(log, 'r')
            while True:
                line = f.readline()
                if line == '':
                    break
                myinput = Input.from_json_str(line)
                output_by_method = {}
                line = f.readline()
                while line != '' and line != '\n':
                    output = Output.from_json_str(line)
                    output_by_method[output.method] = output
                    line = f.readline()
                data.append((myinput, output_by_method))
        return data


    @staticmethod
    def remove_make(root_dir: str):
        '''if root_dir exists, remove all the content
           make directory
        '''
        if os.path.exists(root_dir):
            shutil.rmtree(root_dir)
        os.makedirs(root_dir)


    @staticmethod
    def generate_tx_list(description: str, grid_length: int, sensordata_file: str = None) -> list:
        '''generate some tx locations
        Args:
            description -- some pattern to generate the tx locations during the testing phase
            grid_length -- the grid length
            sensordata_file -- the sensor information filename
        Return:
            a list of tuple (x, y)
        '''
        def is_outside(tx: tuple, sensor_list: list, threshold: float = 5) -> bool:
            '''
            Args:
                tx -- transmitter location (x, y)
                sensor_list -- a list of sensor location (x, y)
                threshold -- the minimum distance between the tx and all sensors
            Return:
                if True the tx is threshold distance outside ALL sensors
            '''
            for sen in sensor_list:
                if Utility.distance(tx, sen, Default.cell_length) < threshold:
                    return False
            return True

        tx_list = []
        if description == 'test-5meter':
            # for a 4x4 grid, put some tx in the (0.5, 0.5) grid
            for x in np.linspace(0, grid_length, 401):
                y = 0
                tx_list.append((x, y))
        elif description == 'filter-5meter':
            with open(sensordata_file, 'r') as f:
                sensordata = json.load(f)
                sensor_list = list(sensordata['sensors'].values())
            for i in range(grid_length):
                for j in range(grid_length):
                    outside_5m = False
                    while outside_5m is False:                    
                        x = i + np.random.uniform(0, 1)
                        y = j + np.random.uniform(0, 1)
                        outside_5m = is_outside((x, y), sensor_list, threshold=5)
                    tx_list.append((x, y))
        elif description == 'filter-5meter-onelevel':
            with open(sensordata_file, 'r') as f:
                sensordata = json.load(f)
                sensor_list_all = list(sensordata['sensors'].values())
                sensor_list = sensor_list_all[0:5] + sensor_list_all[7:9] + sensor_list_all[11:16]
            for i in range(grid_length):
                for j in range(grid_length):
                    outside_5m = False
                    while outside_5m is False:                    
                        x = i + np.random.uniform(0, 1)
                        y = j + np.random.uniform(0, 1)
                        outside_5m = is_outside((x, y), sensor_list, threshold=5)
                    tx_list.append((x, y))
        else:
            raise Exception(f'{description} not implemented...')
        return tx_list


