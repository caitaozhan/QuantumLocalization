'''
the main
'''

import argparse
import numpy as np
import random
import matplotlib.pyplot as plt
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parameters for POVM localization')
    parser.add_argument('-m', '--methods', type=str, nargs='+', default=[Default.method], help='POVM-Loc, POVM-Loc Pro, POVM-Loc Max, or POVM-Loc One')
    parser.add_argument('-l', '--grid_length', type=int, nargs=1, default=[Default.grid_length])
    parser.add_argument('-c', '--continuous', type=bool, nargs=1, default=[Default.continuous], help='whether the testing locations are continuous or discrete')
    parser.add_argument('-n', '--noise', type=float, nargs=1, default=[Default.std], help='the standard deviation of the zero mean shadowing')

    args = parser.parse_args()
    methods      = args.methods
    grid_length  = args.grid_length[0]
    continuous   = args.continuous[0]
    noise        = args.noise[0]

    unitary_operator = UnitaryOperator(Default.alpha, noise, Default.power_ref)

    if 'POVM-Loc One' in methods:
        pass
    if 'POVM-Loc' in methods:
        pass
    if 'POVM-Loc Pro' in methods:
        pass
    if 'POVM-Loc Max' in methods:
        pass
