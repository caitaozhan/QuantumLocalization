'''
the main
'''

import argparse
import time
from localization import QuantumLocalization
from default import Default
from my_logger import MyLogger
from unitary_operator import UnitaryOperator
from input_output import Input, Output



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parameters for POVM localization')
    parser.add_argument('-m', '--methods', type=str, nargs='+', default=[Default.method], help='POVM-Loc, POVM-Loc Pro, POVM-Loc Max, or POVM-Loc One')
    parser.add_argument('-l', '--grid_length', type=int, nargs=1, default=[Default.grid_length])
    parser.add_argument('-s', '--sensor_num', type=int, nargs=1, default=[Default.sensor_num])
    parser.add_argument('-c', '--continuous', type=bool, nargs=1, default=[Default.continuous], help='whether the testing locations are continuous or discrete')
    parser.add_argument('-n', '--noise', type=float, nargs=1, default=[Default.std], help='the standard deviation of the zero mean shadowing')
    parser.add_argument('-od', '--output_dir', type=str, nargs=1, default=[Default.output_dir], help='the directory of the logged outputs')
    parser.add_argument('-of', '--output_file', type=str, nargs=1, default=[Default.output_file], help='the filename of the logged outputs')


    args = parser.parse_args()
    methods      = args.methods
    grid_length  = args.grid_length[0]
    sensor_num   = args.sensor_num[0]
    continuous   = args.continuous[0]
    noise        = args.noise[0]
    output_dir   = args.output_dir[0]
    output_file  = args.output_file[0]

    unitary_operator = UnitaryOperator(Default.alpha, noise, Default.power_ref)
    # training phase
    qls = {}
    if 'povmloc-one' in methods:
        sensordata = f'sensordata/onelevel.{grid_length}x{grid_length}.{sensor_num}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        ql.train_povmloc_one()
        qls['povmloc-one'] = ql
    if 'povmloc' in methods:
        sensordata = f'sensordata/twolevel.{grid_length}x{grid_length}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        ql.train_povmloc()
        qls['povmloc'] = ql
    if 'povmloc-pro' in methods:
        pass
    
    # testing phase
    mylogger = MyLogger(output_dir, output_file)
    tx_list = [(x + 0.5, y + 0.5) for x in range(grid_length) for y in range(grid_length)]
    for i, tx in enumerate(tx_list):
        if i not in [7, 11]:
            continue
        myinput = Input(tx, grid_length, sensor_num, noise, continuous)
        outputs = []
        if 'povmloc-one' in methods:
            ql = qls['povmloc-one']
            start = time.time()
            correct, pred = ql.povmloc_one(tx)
            elapse = round(time.time() - start, 2)
            outputs.append(Output('povmloc-one', correct, localization_error=-1, pred=pred, elapse=elapse))
        if 'povmloc' in methods:
            ql = qls['povmloc']
            start = time.time()
            correct, pred = ql.povmloc(tx)
            elapse = round(time.time() - start, 2)
            outputs.append(Output('povmloc', correct, localization_error=-1, pred=pred, elapse=elapse))
        if 'povmloc-pro' in methods:
            pass
        
        mylogger.log(myinput, outputs)
        time.sleep(0.5)
