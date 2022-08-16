'''
some utility tools
'''

import numpy as np
from typing import Union
# from qiskit.quantum_info.operators.operator import Operator


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
    def distance(loc1: Union[list, tuple], loc2: Union[list, tuple], cell_length: float) -> float:
        '''return the distance between loc1 and loc2
        '''
        return cell_length * np.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)
