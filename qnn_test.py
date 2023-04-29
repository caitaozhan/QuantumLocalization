import time
import numpy as np
import glob
import os
import json
import pickle
import torch
import torch.nn.functional as F
import torchquantum as tq
import threading
from qiskit import IBMQ
from typing import Tuple
from collections import Counter
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset
from utility import Utility
from default import Default
from torchquantum.plugins import QiskitProcessor
from my_logger import MyLogger
from input_output import Input, Output
from unitary_operator import UnitaryOperator
from qiskit import IBMQ


def get_loc_error(output_all: list, target_all: list, dimension: int) -> list:
    '''return a list of error (float)
    '''
    errors = []
    for output, target in zip(output_all, target_all):
        error = Utility.distance(output, target, dimension)
        errors.append(error)
    return errors


def get_loc_error_finelevel(output_all: list, target_all: list, area_length: int, grid_length: int, base: Tuple) -> Tuple:
    '''the fine level version of getting the errors, need to add the relative output to the block_origin
    Args:
        output_all  -- the relative locations in a block
        target_all  -- the global locations ground truth
        area_length -- the length of the area (block)
        base        -- the bottom left cornor of the block
    Return:
        errors -- a list of errors
        preds  -- a list of predict locations
    '''
    errors = []
    preds = []
    for output, target in zip(output_all, target_all):
        tx_relative = (output[0] * area_length, output[1] * area_length)
        pred = (base[0] + tx_relative[0], base[1] + tx_relative[1])
        target = (target[0] * grid_length, target[1] * grid_length)
        error = Utility.distance(pred, target, Default.cell_length)
        errors.append(error)
        preds.append(pred)
    return errors, preds


def get_pred_correct(output_all: list, target_all: list, grid_length: int) -> Tuple[list, list]:
    '''return a list of predicted loc and whether its correctness
    '''
    def idx2pred(idx: int, grid_length: int) -> Tuple[float, float]:
        x = idx // grid_length
        y = idx % grid_length
        return (x + 0.5, y + 0.5)

    pred_list    = []
    correct_list = []
    for output, target in zip(output_all, target_all):
        idx = np.argmax(output)
        correct = True if idx == target else False
        pred = idx2pred(idx, grid_length)
        pred_list.append(pred)
        correct_list.append(correct)
    return pred_list, correct_list


def test_onelevel_continuous_ibm(length: int, sen: int, noise_in_training: bool, ibm_in_testing: bool, \
                                 output_dir: str, output_file: str, backend_name: str):
    print(f'ibm_in_testing = {ibm_in_testing}, noise_in_training = {noise_in_training}, backend_name = {backend_name}')
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{length}x{length}.{sen}')
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    area = info['area']
    area_length = area[1][0] - area[0][0]
    root_dir = os.path.join(dataset_dir, 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    model_dir = dataset_dir.replace('data', 'model')
    model_name = 'model-ibm.pt' if noise_in_training else 'model.pt'
    with open(os.path.join(model_dir, model_name), 'rb') as f:
        model = pickle.load(f)
    from qiskit import IBMQ
    IBMQ.load_account()
    if ibm_in_testing:
        processor = QiskitProcessor(use_real_qc=True, backend_name=backend_name)
    else:
        processor = QiskitProcessor(use_real_qc=False, noise_model_name=backend_name, max_jobs=8)
    model.set_qiskit_processor(processor)
    model.to(device=device)
    model.eval()
    
    loss_list = []
    target_all = []
    output_all = []
    start = time.time()
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas = sample['phase'].to(device)
            targets = sample['label'].to(device)
            outputs = model(thetas, use_qiskit=True)
            # the model
            loss = F.mse_loss(outputs, targets)
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
        output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
        errors = get_loc_error(output_all, target_all, area_length * Default.cell_length)
        avg_error = np.mean(errors)
        print(f'time = {time.time() - start}, test loss = {np.mean(loss_list)}, test localization error = {avg_error}')
        print(errors)
        mylogger = MyLogger(output_dir, output_file)
        for tx, pred, error in zip(target_all, output_all, errors):
            myinput = Input((round(tx[0]*area_length, 3), round(tx[1]*area_length, 3)), length, sen, noise=0, continuous=True, ibm=True)
            outputs = []
            outputs.append(Output(f'qml-{backend_name}', False, round(error, 3), (round(pred[0]*area_length, 3), round(pred[1]*area_length, 3)), -1))
            mylogger.log(myinput, outputs)


def test_onelevel_continuous(length: int, sen: int, output_dir: str, output_file: str):
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{length}x{length}.{sen}')
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    area = info['area']
    area_length = area[1][0] - area[0][0]
    root_dir = os.path.join(dataset_dir, 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    model_dir = dataset_dir.replace('data', 'model')
    model_name = 'model.pt'
    with open(os.path.join(model_dir, model_name), 'rb') as f:
        model = pickle.load(f)
    model.eval()
    
    loss_list = []
    target_all = []
    output_all = []
    start = time.time()
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas = sample['phase'].to(device)
            targets = sample['label'].to(device)
            # the model
            outputs = model(thetas, use_qiskit=False)
            loss = F.mse_loss(outputs, targets)
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
        output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
        errors = get_loc_error(output_all, target_all, area_length * Default.cell_length)
        avg_error = np.mean(errors)
        print(f'time = {time.time() - start}, test loss = {np.mean(loss_list)}, test localization error = {avg_error}')
        print(errors)
        mylogger = MyLogger(output_dir, output_file)
        for tx, pred, error in zip(target_all, output_all, errors):
            myinput = Input((round(tx[0]*area_length, 3), round(tx[1]*area_length, 3)), length, sen, noise=0, continuous=True, ibm=False)
            outputs = []
            outputs.append(Output(f'qml-r', False, round(error, 3), (round(pred[0]*area_length, 3), round(pred[1]*area_length, 3)), -1))
            mylogger.log(myinput, outputs)


def test_onelevel_discrete_ibm(length: int, sen: int, noise_in_training: bool, ibm_in_testing: bool, \
                               output_dir: str, output_file: str, backend_name: str):
    print(f'noise in training = {noise_in_training}, backend_name = {backend_name}')
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'{length}x{length}.{sen}')
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    area = info['area']
    block_cell_ratio = info['block_cell_ratio']
    area_length = area[1][0] - area[0][0]
    grid_length = area_length // block_cell_ratio
    root_dir = os.path.join(dataset_dir, 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    model_dir = dataset_dir.replace('data', 'model')
    model_name = 'model-ibm.pt' if noise_in_training else 'model.pt'
    with open(os.path.join(model_dir, model_name), 'rb') as f:
        model = pickle.load(f)
    from qiskit import IBMQ
    IBMQ.load_account()
    if ibm_in_testing:
        processor = QiskitProcessor(use_real_qc=True, backend_name=backend_name)
    else:
        processor = QiskitProcessor(use_real_qc=False, noise_model_name=backend_name, max_jobs=8)
    model.set_qiskit_processor(processor)
    model.to(device=device)
    model.eval()
    
    loss_list  = []
    target_all = []
    output_all = []
    loc_all    = []
    start = time.time()
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas  = sample['phase'].to(device)
            targets = sample['label'].to(device)
            loc_all.append(sample['loc'])
            # the model
            outputs = model(thetas, use_qiskit=True)
            loss = F.nll_loss(outputs, targets)
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
        output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
        loc_all    = torch.cat(loc_all).numpy().tolist()
        pred_list, correct_list = get_pred_correct(output_all, target_all, grid_length)
        accuracy = sum(correct_list) / len(correct_list)
        print(f'time = {time.time() - start}, test loss = {np.mean(loss_list)}, test localization error = {accuracy}')
        print(correct_list)
        mylogger = MyLogger(output_dir, output_file)
        for tx, pred, correct in zip(loc_all, pred_list, correct_list):
            myinput = Input(tx, length, sen, noise=0, continuous=True, ibm=True)
            outputs = []
            outputs.append(Output(f'qml-{backend_name}', correct, -1, pred, -1))
            mylogger.log(myinput, outputs)


def test_onelevel_discrete(length: int, sen: int, output_dir: str, output_file: str):
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'{length}x{length}.{sen}')
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    area = info['area']
    block_cell_ratio = info['block_cell_ratio']
    area_length = area[1][0] - area[0][0]
    grid_length = area_length // block_cell_ratio
    root_dir = os.path.join(dataset_dir, 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    model_dir = dataset_dir.replace('data', 'model')
    model_name = 'model.pt'
    with open(os.path.join(model_dir, model_name), 'rb') as f:
        model = pickle.load(f)
    model.eval()
    
    loss_list  = []
    target_all = []
    output_all = []
    loc_all    = []
    start = time.time()
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas  = sample['phase'].to(device)
            targets = sample['label'].to(device)
            loc_all.append(sample['loc'])
            # the model
            outputs = model(thetas, use_qiskit=False)
            loss = F.nll_loss(outputs, targets)
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
        output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
        loc_all    = torch.cat(loc_all).numpy().tolist()
        pred_list, correct_list = get_pred_correct(output_all, target_all, grid_length)
        accuracy = sum(correct_list) / len(correct_list)
        print(f'time = {time.time() - start}, test loss = {np.mean(loss_list)}, test accuracy = {accuracy}')
        mylogger = MyLogger(output_dir, output_file)
        for tx, pred, correct in zip(loc_all, pred_list, correct_list):
            myinput = Input(tx, length, sen, noise=0, continuous=False, ibm=False)
            outputs = []
            outputs.append(Output(f'qml-c', correct, -1, pred, -1))
            mylogger.log(myinput, outputs)


def test_twolevel_continuous(length: int, sen: int, output_dir: str, output_file: str):
    '''this coarse level will generate some the datasets for the fine level
    '''
    def limit_output(output: list) -> None:
        output[0] = 0 if output[0] < 0 else output[0]
        output[0] = 0.9999 if output[0] > 0.9999 else output[0]
        output[1] = 0 if output[1] < 0 else output[1]
        output[1] = 0.9999 if output[1] > 0.9999 else output[1]

    # a thread
    def fine_level_thread(block_id: int, grid_length: int, sen: int, output_dir: str, output_file: str):
        '''the second fine level localization.
        Args:
            block_id    -- or the set_i, this thread is associated with
            grid_length -- the length of the whole grid
            sen         -- the sensor number in the coarse level
        '''
        # 0. preparing variables
        level_i = 1
        set_i   = block_id
        dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{grid_length}x{grid_length}.{sen}.two')
        info = json.load(open(os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'info')))
        print(info)
        area = info['area']
        area_length = area[1][0] - area[0][0]
        block_base = area[0]
        
        # 1. the level-1-set-block_id testing dataset
        root_dir = os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'test')
        test_dataset = QuantumSensingDataset(root_dir)
        bsz = len(test_dataset)
        if bsz > 500:
            raise Exception('testing dataset too large!')
        test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 2. fine level model:
        model_path = os.path.join(dataset_dir.replace('data', 'model'), f'level-{level_i}-set-{set_i}', 'model.pt')
        if os.path.exists(model_path) is False:
            raise Exception(f'model does not exist: {model_path}')
        with open(model_path, 'rb') as f:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = pickle.load(f)
            model.to(device=device)
            model.eval()

        target_all = []
        output_all = []
        with torch.no_grad():
            for _, sample in enumerate(test_dataloader):
                thetas = sample['phase'].to(device)
                targets = sample['label'].to(device)
                # the model
                outputs = model(thetas, use_qiskit=False)
                target_all.append(targets)
                output_all.append(outputs)
            target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
            output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
            # compute the errors
            errors, preds = get_loc_error_finelevel(output_all, target_all, area_length, grid_length, block_base)
            avg_error = np.mean(errors)
            print(f'block = {block_id}, # of cases = {len(errors)}, test localization error = {avg_error}')
            mylogger = MyLogger(output_dir, output_file)
            for tx, pred, error in zip(target_all, preds, errors):
                myinput = Input((round(tx[0]*grid_length, 3), round(tx[1]*grid_length, 3)), grid_length, sen, noise=0, continuous=True, ibm=False)
                outputs = []
                outputs.append(Output(f'qml-r-two', False, round(error, 3), (round(pred[0], 3), round(pred[1], 3)), -1))
                mylogger.log(myinput, outputs)
            

    # 0. preparing variables
    level_i = 0
    set_i   = 0
    sensordata_file = f'sensordata/twolevel.{length}x{length}.{sen}.json'
    with open(sensordata_file, 'r') as f:
        sensordata = json.load(f)
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{length}x{length}.{sen}.two')
    info = json.load(open(os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'info')))
    unitary_operator = UnitaryOperator(Default.pathloss_expo, 0, Default.power_ref)

    print(info)
    # 1. prepare directories for the level 1 testing datasets
    area = info['area']
    area_length = area[1][0] - area[0][0]
    block_cell_ratio = info['block_cell_ratio']
    grid_length_block = area_length // block_cell_ratio
    total_blocks = grid_length_block ** 2
    block_sample_counter = Counter()
    testing_folder_template = os.path.join(dataset_dir, 'level-1-set-{}', 'test')
    for i in range(total_blocks):
        Utility.remove_make(testing_folder_template.format(i))
        test_phase_dir = os.path.join(testing_folder_template.format(i), 'phase')
        test_label_dir = os.path.join(testing_folder_template.format(i), 'label')
        os.makedirs(test_phase_dir)
        os.makedirs(test_label_dir)
    
    # 2. the level 0 testing dataset
    root_dir = os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 3. first coarse level model
    model_path = os.path.join(dataset_dir.replace('data', 'model'), f'level-{level_i}-set-{set_i}', 'model.pt')
    if os.path.exists(model_path) is False:
        raise Exception(f'model does not exist: {model_path}')
    with open(model_path, 'rb') as f:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = pickle.load(f)
        model.to(device=device)
        model.eval()
    
    # 4. run the coarse level model
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas = sample['phase'].to(device)
            targets = sample['label'].to(device)
            # the model
            outputs = model(thetas, use_qiskit=False)
            loss = F.mse_loss(outputs, targets)
            # print(loss.item())
            targets = targets.cpu().detach().numpy().tolist()
            outputs = outputs.cpu().detach().numpy().tolist()
            errors = []
            for output, target in zip(outputs, targets):
                limit_output(output)
                tx_level0 = (output[0] * area_length, output[1] * area_length)
                tx_truth = (target[0] * area_length, target[1] * area_length)
                error = Utility.distance(tx_level0, tx_truth, Default.cell_length)
                errors.append(error)
                # determine the block
                block = (int(tx_level0[0] / block_cell_ratio), int(tx_level0[1] / block_cell_ratio))
                block_i = block[0] * grid_length_block + block[1]
                # generate new thetas, and save to the new testing dataset
                sensors = sensordata['levels'][f'level-1'][f'set-{block_i}']['sensors']  # set_i == block_i
                thetas = []
                for rx_i in sensors:
                    rx = sensordata['sensors'][f'{rx_i}']
                    distance = Utility.distance(tx_truth, rx, Default.cell_length)
                    phase_shift, _ = unitary_operator.compute_H(distance, noise=True)
                    thetas.append(phase_shift)
                counter = block_sample_counter[block_i]
                np.save(os.path.join(testing_folder_template.format(block_i), 'phase', f'{counter}.npy'), np.array(thetas).astype(np.float32))
                np.save(os.path.join(testing_folder_template.format(block_i), 'label', f'{counter}.npy'), np.array(target).astype(np.float32))
                block_sample_counter[block_i] += 1
            print(f'one level error = {np.mean(errors)}')

    # 5. start the second fine level threads
    threads = []
    for block_id in range(total_blocks):
        t = threading.Thread(target=fine_level_thread, args=(block_id, length, sen, output_dir, output_file))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def test_twolevel_continuous_ibm(length: int, sen: int, output_dir: str, output_file: str, ibm_in_testing: bool, backend_name: bool):
    '''this coarse level will generate some the datasets for the fine level
    '''
    def limit_output(output: list) -> None:
        output[0] = 0 if output[0] < 0 else output[0]
        output[0] = 0.9999 if output[0] > 0.9999 else output[0]
        output[1] = 0 if output[1] < 0 else output[1]
        output[1] = 0.9999 if output[1] > 0.9999 else output[1]

    # a thread
    def fine_level_thread(block_id: int, grid_length: int, sen: int, output_dir: str, output_file: str, ibm_in_testing: bool, backend_name: bool):
        '''the second fine level localization.
        Args:
            block_id    -- or the set_i, this thread is associated with
            grid_length -- the length of the whole grid
            sen         -- the sensor number in the coarse level
        '''
        # 0. preparing variables
        level_i = 1
        set_i   = block_id
        dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{grid_length}x{grid_length}.{sen}.two')
        info = json.load(open(os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'info')))
        print(info)
        area = info['area']
        area_length = area[1][0] - area[0][0]
        block_base = area[0]
        
        # 1. the level-1-set-block_id testing dataset
        root_dir = os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'test')
        test_dataset = QuantumSensingDataset(root_dir)
        bsz = len(test_dataset)
        if bsz > 500:
            raise Exception('testing dataset too large!')
        elif bsz == 0:
            raise Exception(f'block_id = {block_id}, testing dataset is zero...')
        test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 2. fine level model:
        model_path = os.path.join(dataset_dir.replace('data', 'model'), f'level-{level_i}-set-{set_i}', 'model.pt')
        if os.path.exists(model_path) is False:
            raise Exception(f'model does not exist: {model_path}')
        with open(model_path, 'rb') as f:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = pickle.load(f)

        if ibm_in_testing:
            processor = QiskitProcessor(use_real_qc=True, backend_name=backend_name)
        else:
            processor = QiskitProcessor(use_real_qc=False, noise_model_name=backend_name, max_jobs=8)
        model.set_qiskit_processor(processor)
        model.to(device=device)
        model.eval()

        target_all = []
        output_all = []
        with torch.no_grad():
            for _, sample in enumerate(test_dataloader):
                thetas = sample['phase'].to(device)
                targets = sample['label'].to(device)
                # the model
                outputs = model(thetas, use_qiskit=True)
                target_all.append(targets)
                output_all.append(outputs)
            target_all = torch.cat(target_all).cpu().detach().numpy().tolist()
            output_all = torch.cat(output_all).cpu().detach().numpy().tolist()
            # compute the errors
            errors, preds = get_loc_error_finelevel(output_all, target_all, area_length, grid_length, block_base)
            avg_error = np.mean(errors)
            print(f'block = {block_id}, # of cases = {len(errors)}, test localization error = {avg_error}')
            mylogger = MyLogger(output_dir, output_file)
            for tx, pred, error in zip(target_all, preds, errors):
                myinput = Input((round(tx[0]*grid_length, 3), round(tx[1]*grid_length, 3)), grid_length, sen, noise=0, continuous=True, ibm=False)
                outputs = []
                outputs.append(Output(f'qml-two-{backend_name}', False, round(error, 3), (round(pred[0], 3), round(pred[1], 3)), -1))
                mylogger.log(myinput, outputs)


    print(f'ibm_in_testing={ibm_in_testing}, backend_name={backend_name}')
    # 0. preparing variables
    level_i = 0
    set_i   = 0
    sensordata_file = f'sensordata/twolevel.{length}x{length}.{sen}.json'
    with open(sensordata_file, 'r') as f:
        sensordata = json.load(f)
    dataset_dir = os.path.join(os.getcwd(), 'qml-data', f'c.{length}x{length}.{sen}.two')
    info = json.load(open(os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'info')))
    unitary_operator = UnitaryOperator(Default.pathloss_expo, 0, Default.power_ref)

    print(info)
    # 1. prepare directories for the level 1 testing datasets
    area = info['area']
    area_length = area[1][0] - area[0][0]
    block_cell_ratio = info['block_cell_ratio']
    grid_length_block = area_length // block_cell_ratio
    total_blocks = grid_length_block ** 2
    block_sample_counter = Counter()
    testing_folder_template = os.path.join(dataset_dir, 'level-1-set-{}', 'test')
    for i in range(total_blocks):
        Utility.remove_make(testing_folder_template.format(i))
        test_phase_dir = os.path.join(testing_folder_template.format(i), 'phase')
        test_label_dir = os.path.join(testing_folder_template.format(i), 'label')
        os.makedirs(test_phase_dir)
        os.makedirs(test_label_dir)
    
    # 2. the level 0 testing dataset
    root_dir = os.path.join(dataset_dir, f'level-{level_i}-set-{set_i}', 'test')
    test_dataset = QuantumSensingDataset(root_dir)
    bsz = len(test_dataset)
    if bsz > 500:
        raise Exception('testing dataset too large!')
    test_dataloader = DataLoader(test_dataset, batch_size=bsz, shuffle=False, num_workers=4)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 3. first coarse level model
    model_path = os.path.join(dataset_dir.replace('data', 'model'), f'level-{level_i}-set-{set_i}', 'model.pt')
    if os.path.exists(model_path) is False:
        raise Exception(f'model does not exist: {model_path}')
    with open(model_path, 'rb') as f:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = pickle.load(f)
    
    IBMQ.load_account()
    if ibm_in_testing:
        processor = QiskitProcessor(use_real_qc=True, backend_name=backend_name)
    else:
        processor = QiskitProcessor(use_real_qc=False, noise_model_name=backend_name, max_jobs=8)
    model.set_qiskit_processor(processor)
    model.to(device=device)
    model.eval()
    
    # 4. run the coarse level model
    with torch.no_grad():
        for _, sample in enumerate(test_dataloader):
            thetas = sample['phase'].to(device)
            targets = sample['label'].to(device)
            # the model
            outputs = model(thetas, use_qiskit=True)
            targets = targets.cpu().detach().numpy().tolist()
            outputs = outputs.cpu().detach().numpy().tolist()
            errors = []
            for output, target in zip(outputs, targets):
                limit_output(output)
                tx_level0 = (output[0] * area_length, output[1] * area_length)
                tx_truth = (target[0] * area_length, target[1] * area_length)
                error = Utility.distance(tx_level0, tx_truth, Default.cell_length)
                errors.append(error)
                # determine the block
                block = (int(tx_level0[0] / block_cell_ratio), int(tx_level0[1] / block_cell_ratio))
                block_i = block[0] * grid_length_block + block[1]
                # generate new thetas, and save to the new testing dataset
                sensors = sensordata['levels'][f'level-1'][f'set-{block_i}']['sensors']  # set_i == block_i
                thetas = []
                for rx_i in sensors:
                    rx = sensordata['sensors'][f'{rx_i}']
                    distance = Utility.distance(tx_truth, rx, Default.cell_length)
                    phase_shift, _ = unitary_operator.compute_H(distance, noise=True)
                    thetas.append(phase_shift)
                counter = block_sample_counter[block_i]
                np.save(os.path.join(testing_folder_template.format(block_i), 'phase', f'{counter}.npy'), np.array(thetas).astype(np.float32))
                np.save(os.path.join(testing_folder_template.format(block_i), 'label', f'{counter}.npy'), np.array(target).astype(np.float32))
                block_sample_counter[block_i] += 1
            print(f'one level error = {np.mean(errors)}')
            print(f'block_sample_counter = {block_sample_counter}')

    # 5. start the second fine level threads
    threads = []
    for block_id in range(total_blocks):
        t = threading.Thread(target=fine_level_thread, args=(block_id, length, sen, output_dir, output_file, ibm_in_testing, backend_name))
        t.start()
        threads.append(t)
        time.sleep(10)

    for t in threads:
        t.join()


def onelevel_ibm(continuous: bool):
    if continuous:
        length = 4
        sen = 4
        noise_in_training = False
        ibm_in_testing = True
        # backend_name = 'ibm_oslo'
        # backend_name = 'ibmq_quito'
        backend_name = 'ibmq_manila'
        output_dir = 'results'
        output_file = f'ibm.continuous.onelevel.{length}x{length}'
        test_onelevel_continuous_ibm(length, sen, noise_in_training, ibm_in_testing, output_dir, output_file, backend_name)
    else:
        length = 4
        sen = 4
        noise_in_training = False
        ibm_in_testing = True
        # backend_name = 'ibmq_quito'
        backend_name = 'ibmq_manila'
        output_dir = 'results'
        output_file = 'ibm.discrete.onelevel'
        test_onelevel_discrete_ibm(length, sen, noise_in_training, ibm_in_testing, output_dir, output_file, backend_name)


def onelevel(continuous: bool):
    if continuous:
        length = 3
        sen = 4
        output_dir = 'results'
        output_file = 'ibm.continuous.onelevel.2x2'
        test_onelevel_continuous(length, sen, output_dir, output_file)
    else:
        length = 3
        sen = 4
        output_dir = 'results'
        output_file = 'ibm.discrete.onelevel.3x3'
        test_onelevel_discrete(length, sen, output_dir, output_file)


def twolevel_ibm(continuous: bool):
    if continuous:
        length = 4
        sen = 4
        ibm_in_testing = True
        backend_name = 'ibmq_manila'
        output_dir = 'results'
        output_file = 'ibm.continuous.twolevel.manila'
        test_twolevel_continuous_ibm(length, sen, output_dir, output_file, ibm_in_testing, backend_name)
    else:
        pass


def twolevel(continuous: bool):
    if continuous:
        length = 4
        sen = 4
        output_dir = 'results'
        output_file = 'ibm.continuous.twolevel'
        test_twolevel_continuous(length, sen, output_dir, output_file)
    else:
        pass


if __name__ == '__main__':
    onelevel_ibm(continuous=True)
    # onelevel(continuous=True)

    # twolevel(continuous=True)
    # twolevel_ibm(continuous=True)
