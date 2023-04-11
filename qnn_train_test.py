import time
import numpy as np
import glob
import os
import json
import torch
import pickle
import torchquantum as tq
import torchquantum.functional as tqf
import torch.nn.functional as F
import torch.optim as optim
# import matplotlib.pyplot as plt
from torch import Tensor
from torchquantum.plugins.qiskit_plugin import tq2qiskit
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset
from qnn import QuantumSensing, QuantumMLclassification, QuantumMLregression
from utility import Utility
from default import Default


def compute_accuracy(output_all, target_all):
    _, indices = output_all.topk(1, dim=1)
    masks = indices.eq(target_all.view(-1, 1).expand_as(indices))
    size = target_all.shape[0]
    corrects = masks.sum().item()
    accuracy = corrects / size
    return accuracy


def compute_loc_error(output_all: Tensor, target_all: Tensor, dimension: int):
    errors = []
    for output, target in zip(output_all.cpu().detach().numpy(), target_all.cpu().detach().numpy()):
        error = Utility.distance(output, target, dimension)
        errors.append(error)
    return np.mean(errors)


def train_test(grid_length: int, num_sensor: int):
    print('-'*20)
    print(f'grid_length={grid_length}, num_sensor={num_sensor}\n')
    # data
    folder = f'{grid_length}x{grid_length}.{num_sensor}'

    root_dir = f'qml-data/{folder}/train'
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

    root_dir = f'qml-data/{folder}/test'
    test_dataset = QuantumSensingDataset(root_dir)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True, num_workers=4)

    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    n_qubits = num_sensor
    n_locations = grid_length ** 2
    model = QuantumMLclassification(n_wires=n_qubits, n_locations=n_locations).to(device)
    n_epochs = 100
    optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)

    train_loss = []
    train_acc  = []
    test_loss  = []
    test_acc   = []

    for e in range(n_epochs):
        start = time.time()
        model.train()
        loss_list = []
        target_all = []
        output_all = []
        for t, sample in enumerate(train_dataloader):
            thetas = sample['phase']
            targets = sample['label'].to(device)
            # preparing sensing data
            qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
            q_device = qsensing(thetas)
            # the model
            outputs = model(q_device)
            # compute loss, gradient, optimize, etc...
            loss = F.nll_loss(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        train_loss.append(np.mean(loss_list))
        target_all = torch.cat(target_all)
        output_all = torch.cat(output_all)
        accuracy = compute_accuracy(output_all, target_all)
        train_acc.append(accuracy)
        
        model.eval()
        loss_list = []
        target_all = []
        output_all = []
        with torch.no_grad():
            for t, sample in enumerate(test_dataloader):
                thetas = sample['phase']
                targets = sample['label'].to(device)
                qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
                q_device = qsensing(thetas)
                # the model
                outputs = model(q_device)
                loss = F.nll_loss(outputs, targets)
                loss_list.append(loss.item())
                target_all.append(targets)
                output_all.append(outputs)
            target_all = torch.cat(target_all)
            output_all = torch.cat(output_all)
        test_loss.append(np.mean(loss_list))
        accuracy = compute_accuracy(output_all, target_all)
        test_acc.append(accuracy)
        scheduler.step()
        epoch_time = time.time() - start
        print(f'epoch={e}, time = {epoch_time:.2f}, test loss={test_loss[-1]:.4f}, test accuracy={test_acc[-1]:.4f}')

    print('\nfinal test loss:\n', test_loss)
    print('final test accu:\n', test_acc)


def train_test_continuous(grid_length: int, num_sensor: int):
    print('-'*20)
    print(f'grid_length={grid_length}, num_sensor={num_sensor}\n')
    # data
    folder = f'{grid_length}x{grid_length}.{num_sensor}'

    root_dir = f'qml-data/{folder}/train'
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

    root_dir = f'qml-data/{folder}/test'
    test_dataset = QuantumSensingDataset(root_dir)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True, num_workers=4)

    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    n_qubits = num_sensor
    n_locations = grid_length ** 2
    model = QuantumMLregression(n_wires=n_qubits).to(device)
    n_epochs = 100
    optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)

    train_loss = []
    train_acc  = []
    test_loss  = []
    test_acc   = []

    for e in range(n_epochs):
        start = time.time()
        model.train()
        loss_list = []
        target_all = []
        output_all = []
        for t, sample in enumerate(train_dataloader):
            thetas = sample['phase']
            targets = sample['label'].to(device)
            # preparing sensing data
            qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
            q_device = qsensing(thetas)
            # the model
            outputs = model(q_device, qstate.states)
            # compute loss, gradient, optimize, etc...
            loss = F.mse_loss(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        train_loss.append(np.mean(loss_list))
        target_all = torch.cat(target_all)
        output_all = torch.cat(output_all)
        # accuracy = compute_accuracy(output_all, target_all)
        # train_acc.append(accuracy)
        
        model.eval()
        loss_list = []
        target_all = []
        output_all = []
        with torch.no_grad():
            for t, sample in enumerate(test_dataloader):
                thetas = sample['phase']
                targets = sample['label'].to(device)
                qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
                q_device = qsensing(thetas)
                # the model
                outputs = model(q_device)
                loss = F.mse_loss(outputs, targets)
                loss_list.append(loss.item())
                target_all.append(targets)
                output_all.append(outputs)
            target_all = torch.cat(target_all)
            output_all = torch.cat(output_all)
        test_loss.append(np.mean(loss_list))
        # accuracy = compute_accuracy(output_all, target_all)
        # test_acc.append(accuracy)
        scheduler.step()
        epoch_time = time.time() - start
        print(f'epoch={e}, time = {epoch_time:.2f}, test loss={test_loss[-1]:.4f}, test accuracy={test_acc[-1]:.4f}')

    print('\nfinal test loss:\n', test_loss)
    print('final test accu:\n', test_acc)


'''one level + discrete, save model'''
def train_save_onelevel(dataset_dir: str):
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    root_dir = os.path.join(dataset_dir, 'train')
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    # train_dataloader = DataLoader(train_dataset, batch_size=7, shuffle=True, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    n_qubits = info['sensor_num']
    area = info['area']
    block_cell_ratio = info['block_cell_ratio']
    grid_length = (area[1][0] - area[0][0]) // block_cell_ratio
    n_locations = grid_length ** 2
    model = QuantumMLclassification(n_wires=n_qubits, n_locations=n_locations).to(device)
    n_epochs = 80
    optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)

    model.train()
    train_loss = []
    train_acc = []
    for e in range(n_epochs):
        start = time.time()
        loss_list = []
        target_all = []
        output_all = []
        for _, sample in enumerate(train_dataloader):
            thetas = sample['phase']
            targets = sample['label'].to(device)
            # preparing sensing data
            qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
            q_device = qsensing(thetas)
            # the model
            outputs = model(q_device)
            # compute loss, gradient, optimize ...
            loss = F.nll_loss(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        train_loss.append(np.mean(loss_list))
        target_all = torch.cat(target_all)
        output_all = torch.cat(output_all)
        accuracy = compute_accuracy(output_all, target_all)
        train_acc.append(accuracy)
        scheduler.step()
        epoch_time = time.time() - start
        
        print(f'epoch={e}, time = {epoch_time:.2f}, train loss={train_loss[-1]:.4f}, train accuracy={train_acc[-1]:.4f}')

        if e % 5 == 4: # save a model every 5 epochs
            model_dir = dataset_dir.replace('qml-data', 'qml-model')
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            with open(os.path.join(model_dir, 'model.pt'), 'wb') as f:
                pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    print('\nfinal train loss:\n', train_loss)
    print('final train accu:\n', train_acc)


'''one level + continuous, save model'''
def train_save_onelevel_continuous(dataset_dir: str):
    info = json.load(open(os.path.join(dataset_dir, 'info')))
    print(info)
    root_dir = os.path.join(dataset_dir, 'train')
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    # train_dataloader = DataLoader(train_dataset, batch_size=7, shuffle=True, num_workers=4)
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    n_qubits = info['sensor_num']
    area = info['area']
    area_length = area[1][0] - area[0][0]
    model = QuantumMLregression(n_wires=n_qubits).to(device)
    n_epochs = 100
    optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)

    model.train()
    train_loss = []
    train_error = []
    for e in range(n_epochs):
        start = time.time()
        loss_list = []
        target_all = []
        output_all = []
        for _, sample in enumerate(train_dataloader):
            thetas = sample['phase']
            targets = sample['label'].to(device)
            # preparing sensing data
            qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
            q_device = qsensing(thetas)
            # the model
            outputs = model(q_device)
            # compute loss, gradient, optimize ...
            loss = F.mse_loss(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_list.append(loss.item())
            target_all.append(targets)
            output_all.append(outputs)
        train_loss.append(np.mean(loss_list))
        target_all = torch.cat(target_all)
        output_all = torch.cat(output_all)
        loc_error = compute_loc_error(output_all, target_all, area_length * Default.cell_length)
        train_error.append(loc_error)
        scheduler.step()
        epoch_time = time.time() - start
        
        print(f'epoch={e}, time = {epoch_time:.2f}, train loss={train_loss[-1]:.4f}, train accuracy={train_error[-1]:.4f}')

        if e % 10 == 9: # save a model every 5 epochs
            model_dir = dataset_dir.replace('qml-data', 'qml-model')
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            with open(os.path.join(model_dir, f'model.pt'), 'wb') as f:
                pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)


    print('\nfinal train loss:\n', train_loss)
    print('final train accu:\n', train_error)


'''two level + discrete, save model'''
def train_save_twolevel(folder: str):
    for i, dataset_dir in enumerate(sorted(glob.glob(folder + '/*'))):   # dataset_dir: ../40x40.two/level-0-set-0
        # if i > 0:
        #     continue
        info = json.load(open(os.path.join(dataset_dir, 'info')))
        print(info)
        root_dir = os.path.join(dataset_dir, 'train')
        train_dataset = QuantumSensingDataset(root_dir)
        train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
        # train_dataloader = DataLoader(train_dataset, batch_size=7, shuffle=True, num_workers=4)
        use_cuda = torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        n_qubits = info['sensor_num']
        area = info['area']
        block_cell_ratio = info['block_cell_ratio']
        grid_length = (area[1][0] - area[0][0]) // block_cell_ratio
        n_locations = grid_length ** 2
        model = QuantumMLclassification(n_wires=n_qubits, n_locations=n_locations).to(device)
        n_epochs = 80
        optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
        scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)
        
        model.train()
        train_loss = []
        train_acc = []
        for e in range(n_epochs):
            start = time.time()
            loss_list = []
            target_all = []
            output_all = []
            for _, sample in enumerate(train_dataloader):
                thetas = sample['phase']
                targets = sample['label'].to(device)
                # preparing sensing data
                qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
                q_device = qsensing(thetas)
                # the model
                outputs = model(q_device)
                # compute loss, gradient, optimize ...
                loss = F.nll_loss(outputs, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_list.append(loss.item())
                target_all.append(targets)
                output_all.append(outputs)
            train_loss.append(np.mean(loss_list))
            target_all = torch.cat(target_all)
            output_all = torch.cat(output_all)
            accuracy = compute_accuracy(output_all, target_all)
            train_acc.append(accuracy)
            scheduler.step()
            epoch_time = time.time() - start
        
            print(f'epoch={e}, time = {epoch_time:.2f}, test loss={train_loss[-1]:.4f}, test accuracy={train_acc[-1]:.4f}')

            if e % 5 == 4: # save a model every 5 epochs
                model_dir = dataset_dir.replace('qml-data', 'qml-model')
                if not os.path.exists(model_dir):
                    os.makedirs(model_dir)
                with open(os.path.join(model_dir, 'model.pt'), 'wb') as f:
                    pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    print('\nfinal train loss:\n', train_loss)
    print('final train accu:\n', train_acc)


'''two level + continuous, save model'''
def train_save_twolevel_continuous(folder: str):
    for i, dataset_dir in enumerate(sorted(glob.glob(folder + '/*'))):   # dataset_dir: ../40x40.two/level-0-set-0
        # if i > 0:
        #     continue
        info = json.load(open(os.path.join(dataset_dir, 'info')))
        print(info)
        root_dir = os.path.join(dataset_dir, 'train')
        train_dataset = QuantumSensingDataset(root_dir)
        train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
        # train_dataloader = DataLoader(train_dataset, batch_size=7, shuffle=True, num_workers=4)
        use_cuda = torch.cuda.is_available()
        device = torch.device('cuda' if use_cuda else 'cpu')
        n_qubits = info['sensor_num']
        area = info['area']
        area_length = area[1][0] - area[0][0]   # area is either the whole grid (level0) or a block (level1)
        model = QuantumMLregression(n_wires=n_qubits).to(device)
        n_epochs = 100
        optimizer = optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
        scheduler = CosineAnnealingLR(optimizer, T_max=n_epochs)
        
        model.train()
        train_loss = []
        train_error = []
        for e in range(n_epochs):
            start = time.time()
            loss_list = []
            target_all = []
            output_all = []
            for _, sample in enumerate(train_dataloader):
                thetas = sample['phase']
                targets = sample['label'].to(device)
                # preparing sensing data
                qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
                q_device = qsensing(thetas)
                # the model
                outputs = model(q_device)
                # compute loss, gradient, optimize ...
                loss = F.mse_loss(outputs, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_list.append(loss.item())
                target_all.append(targets)
                output_all.append(outputs)
            train_loss.append(np.mean(loss_list))
            target_all = torch.cat(target_all)
            output_all = torch.cat(output_all)
            loc_error = compute_loc_error(output_all, target_all, area_length * Default.cell_length)
            train_error.append(loc_error)
            scheduler.step()
            epoch_time = time.time() - start
        
            print(f'epoch={e}, time = {epoch_time:.2f}, train loss={train_loss[-1]:.4f}, train accuracy={train_error[-1]:.4f}')

            if e % 10 == 9: # save a model every 10 epochs
                model_dir = dataset_dir.replace('qml-data', 'qml-model')
                if not os.path.exists(model_dir):
                    os.makedirs(model_dir)
                with open(os.path.join(model_dir, 'model.pt'), 'wb') as f:
                    pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    print('\nfinal train loss:\n', train_loss)
    print('final train accu:\n', train_error)


def main():
    num_sensor = 16
    for grid_length in [8, 10, 12, 14, 16]:
        train_test(grid_length, num_sensor)


'''for training qml one level'''
def main1level(continuous: bool):
    if continuous:
        folder = os.path.join(os.getcwd(), 'qml-data', '4x4.4.H.cont')
        train_save_onelevel_continuous(folder)
        # folder = os.path.join(os.getcwd(), 'qml-data', '16x16.16.H.cont')
        # train_save_onelevel_continuous(folder)
    else:
        # time.sleep(2400)
        sen = 8
        for length in [2,4,6,8,10,12,14,16]:
            folder = os.path.join(os.getcwd(), 'qml-data', f'{length}x{length}.{sen}')
            train_save_onelevel(folder)
        
        # folder = os.path.join(os.getcwd(), 'qml-data', '10x10.16.H')
        # train_save_onelevel(folder)
        
        # folder = os.path.join(os.getcwd(), 'qml-data', '16x16.16.H')
        # train_save_onelevel(folder)


'''for training qml two level'''
def main2level(continuous: bool):
    if continuous:
        folder = os.path.join(os.getcwd(), 'qml-data', '16x16.two.H.cont')
        train_save_twolevel_continuous(folder)        
    else:
        folder = os.path.join(os.getcwd(), 'qml-data', '40x40.two')
        train_save_twolevel(folder)



if __name__ == '__main__':
    # main()
    main1level(continuous=False)
    # main2level(continuous=True)



# train on 3080ti, then copy to caitao-desktop
# scp -P 130 -r 40x40.two/ caitao@130.245.144.108:/home/caitao/Project/quantum-localization/qml-model
