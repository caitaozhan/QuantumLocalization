'''
some utility tools
'''

import numpy as np
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
