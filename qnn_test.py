import time
import numpy as np
import glob
import os
import json
import pickle
import torch
import torch.nn.functional as F
import torch.optim as optim
# import matplotlib.pyplot as plt
from typing import Tuple
from torch import Tensor
from torchquantum.plugins.qiskit_plugin import tq2qiskit
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset
from qnn import QuantumSensing, QuantumMLclassification, QuantumMLregression, QuantumMLregressionIBM, QuantumMLclassificationIBM
from utility import Utility
from default import Default
from torchquantum.plugins import QiskitProcessor
from my_logger import MyLogger
from input_output import Input, Output


def get_loc_error(output_all: list, target_all: list, dimension: int) -> list:
    '''return a list of error (float)
    '''
    errors = []
    for output, target in zip(output_all, target_all):
        error = Utility.distance(output, target, dimension)
        errors.append(error)
    return errors


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


def test_onelevel_continuous_ibm(length: int, sen: int, noise_in_training: bool, ibm_in_testing: bool, output_dir: str, output_file: str):
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
    backend_name = 'ibmq_quito'
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
            outputs.append(Output(f'qml-noise={noise_in_training}', False, round(error, 3), (round(pred[0]*area_length, 3), round(pred[1]*area_length, 3)), -1))
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
            outputs = model(thetas, use_qiskit=False)
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
            myinput = Input((round(tx[0]*area_length, 3), round(tx[1]*area_length, 3)), length, sen, noise=0, continuous=True, ibm=False)
            outputs = []
            outputs.append(Output(f'qml-r', False, round(error, 3), (round(pred[0]*area_length, 3), round(pred[1]*area_length, 3)), -1))
            mylogger.log(myinput, outputs)


def test_onelevel_discrete_ibm(length: int, sen: int, noise_in_training: bool, ibm_in_testing: bool, output_dir: str, output_file: str):
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
    backend_name = 'ibmq_quito'
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
            outputs.append(Output(f'qml-noise={noise_in_training}', correct, -1, pred, -1))
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


def onelevel_ibm(continuous: bool):
    if continuous:
        length = 4
        sen = 4
        noise_in_training = False
        ibm_in_testing = False
        output_dir = 'results'
        output_file = 'ibm.continuous.onelevel'
        test_onelevel_continuous_ibm(length, sen, noise_in_training, ibm_in_testing, output_dir, output_file)
    else:
        length = 4
        sen = 4
        noise_in_training = True
        ibm_in_testing = True
        output_dir = 'results'
        output_file = 'ibm.discrete.onelevel.epoch9'
        test_onelevel_discrete_ibm(length, sen, noise_in_training, ibm_in_testing, output_dir, output_file)


def onelevel(continuous: bool):
    if continuous:
        length = 4
        sen = 4
        output_dir = 'results'
        output_file = 'ibm.continuous.onelevel'
        test_onelevel_continuous(length, sen, output_dir, output_file)
    else:
        length = 4
        sen = 4
        output_dir = 'results'
        output_file = 'ibm.discrete.onelevel'
        test_onelevel_discrete(length, sen, output_dir, output_file)



if __name__ == '__main__':
    onelevel_ibm(continuous=False)
    # onelevel(continuous=False)
