'''
the main
'''

import argparse
import time
import numpy as np
from localization import QuantumLocalization
from default import Default
from my_logger import MyLogger
from unitary_operator import UnitaryOperator
from input_output import Input, Output
from utility import Utility



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parameters for POVM localization')
    parser.add_argument('-m', '--methods', type=str, nargs='+', default=[Default.method], help='POVM-Loc, POVM-Loc Pro, POVM-Loc Max, or POVM-Loc One')
    parser.add_argument('-l', '--grid_length', type=int, nargs=1, default=[Default.grid_length])
    parser.add_argument('-s', '--sensor_num', type=int, nargs=1, default=[Default.sensor_num])
    parser.add_argument('-c', '--continuous', action='store_true', default=False, help='whether the testing locations are continuous or discrete')
    parser.add_argument('-n', '--noise', type=float, nargs=1, default=[Default.std], help='the standard deviation of the zero mean shadowing')
    parser.add_argument('-od', '--output_dir', type=str, nargs=1, default=[Default.output_dir], help='the directory of the logged outputs')
    parser.add_argument('-of', '--output_file', type=str, nargs=1, default=[Default.output_file], help='the filename of the logged outputs')
    parser.add_argument('-rd', '--root_dir', type=str, nargs=1, default=[Default.root_dir], help='the root directory for training data in the quantum ml method')
    parser.add_argument('-gd', '--generate_data', action='store_true', default=False, help='generate new training data, for QML')

    args         = parser.parse_args()
    methods      = args.methods
    grid_length  = args.grid_length[0]
    sensor_num   = args.sensor_num[0]
    continuous   = args.continuous
    noise        = args.noise[0]
    output_dir   = args.output_dir[0]
    output_file  = args.output_file[0]
    
    unitary_operator = UnitaryOperator(Default.pathloss_expo, noise, Default.power_ref)
    ## training phase ##
    qls = {}
    if 'povmloc-one' in methods:
        sensordata = f'sensordata/onelevel.{grid_length}x{grid_length}.{sensor_num}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        ql.train_povmloc_one()
        qls['povmloc-one'] = ql
    if 'povmloc' in methods or 'povmloc-pro' in methods:
        sensordata = f'sensordata/twolevel.{grid_length}x{grid_length}.{sensor_num}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        ql.train_povmloc()
        qls['povmloc'] = ql
    if 'qml' in methods:
        sensordata = f'sensordata/onelevel.{grid_length}x{grid_length}.{sensor_num}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        root_dir = args.root_dir[0]
        generate_data = args.generate_data  # in POVM-Loc, the training and testing are all together
        if generate_data:                   # in QML, training and testing are separate (training takes too much time)
            if continuous:
                ql.train_quantum_ml_continuous(root_dir, generate_data)
            else:
                ql.train_quantum_ml(root_dir, generate_data)
        qls['qml'] = ql
    if 'qml-two' in methods:
        sensordata = f'sensordata/twolevel.{grid_length}x{grid_length}.{sensor_num}.json'
        ql = QuantumLocalization(grid_length=grid_length, cell_length=Default.cell_length, sensordata=sensordata, unitary_operator=unitary_operator)
        root_dir = args.root_dir[0]
        generate_data = args.generate_data  # in POVM-Loc, the training and testing are all together
        if generate_data:                   # in QML, training and testing are separate (training takes too much time)
            if continuous:
                ql.train_quantum_ml_two_continuous(root_dir)
            else:
                ql.train_quantum_ml_two(root_dir)
        qls['qml-two'] = ql


    ## testing phase ##
    mylogger = MyLogger(output_dir, output_file)
    if continuous == False:
        # testing discrete
        tx_list = [(x + 0.5, y + 0.5) for x in range(grid_length) for y in range(grid_length)]
        for i, tx in enumerate(tx_list):
            # if i <= 225:
            #     continue
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
                ql = qls['povmloc']
                start = time.time()
                correct, pred = ql.povmloc_pro(tx)
                elapse = round(time.time() - start, 2)
                outputs.append(Output('povmloc-pro', correct, localization_error=-1, pred=pred, elapse=elapse))
            if 'qml' in methods:
                if not args.generate_data:
                    ql = qls['qml']
                    root_dir = args.root_dir[0]
                    start = time.time()
                    correct, pred = ql.qml(tx, root_dir, continuous=False)
                    elapse = round(time.time() - start, 2)
                    outputs.append(Output('qml-c', correct, -1, pred, elapse))   
            if 'qml-two' in methods:
                generate_data = args.generate_data  # in POVM-Loc, the training and testing are all together
                if not generate_data:                   # in QML, training and testing are separate (training takes too much time)
                    ql = qls['qml-two']
                    root_dir = args.root_dir[0]
                    start = time.time()
                    correct, pred = ql.qml_two(tx, root_dir, continuous=False)
                    elapse = round(time.time() - start, 2)
                    outputs.append(Output('qml-c-two', correct, localization_error=-1, pred=pred, elapse=elapse))

            mylogger.log(myinput, outputs)
            # time.sleep(0.5)
    else:
        # testing: continuous
        np.random.seed(1)
        # tx_list = [(x + 0.5 + np.random.uniform(-0.5, 0.5), y + 0.5 + np.random.uniform(-0.5, 0.5)) for x in range(grid_length) for y in range(grid_length)]
        # tx_list = Utility.generate_tx_list('test-5meter', grid_length, sensordata)
        tx_list = []
        for _ in range(25):
            tx_list.extend(Utility.generate_tx_list('filter-5meter', grid_length, sensordata))
            if (grid_length <= 10 and len(tx_list) > 100) or grid_length > 10:
                break
        for i, tx in enumerate(tx_list):
            # if i > 3:
            #     continue
            myinput = Input((round(tx[0], 3), round(tx[1], 3)), grid_length, sensor_num, noise, continuous)
            outputs = []
            if 'povmloc-one' in methods:
                ql = qls['povmloc-one']
                start = time.time()
                correct, error, pred = ql.povmloc_one(tx, continuous=True)
                elapse = round(time.time() - start, 2)
                outputs.append(Output('povmloc-one', correct, localization_error=round(error, 3), pred=pred, elapse=elapse))
            if 'povmloc' in methods:
                ql = qls['povmloc']
                start = time.time()
                correct, error, pred = ql.povmloc(tx, continuous=True)
                elapse = round(time.time() - start, 2)
                outputs.append(Output('povmloc', correct, localization_error=round(error, 3), pred=pred, elapse=elapse))
            if 'povmloc-pro' in methods:
                ql = qls['povmloc']
                start = time.time()
                correct, error, pred = ql.povmloc_pro(tx, continuous=True)
                elapse = round(time.time() - start, 2)
                outputs.append(Output('povmloc-pro', correct, localization_error=round(error, 3), pred=pred, elapse=elapse))
            if 'qml' in methods:
                if not args.generate_data:
                    ql = qls['qml']
                    root_dir = args.root_dir[0]
                    start = time.time()
                    error, pred = ql.qml(tx, root_dir, continuous=True)
                    elapse = round(time.time() - start, 2)
                    outputs.append(Output('qml-r', False, error, pred, elapse))
            if 'qml-two' in methods:
                if not args.generate_data:
                    ql = qls['qml-two']
                    root_dir = args.root_dir[0]
                    start = time.time()
                    correct, error, pred = ql.qml_two(tx, root_dir, continuous=True)
                    elapse = round(time.time() - start, 2)
                    outputs.append(Output('qml-r-two', correct, error, pred, elapse))
            mylogger.log(myinput, outputs)
            # time.sleep(0.5)


# python main.py -m qml-two -l 40 -s 20 -n 1 -rd qml-data/40x40.two.H.cont -gd -c
