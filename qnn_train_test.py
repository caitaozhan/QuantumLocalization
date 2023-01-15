import time
import numpy as np
import torch
import torchquantum as tq
import torchquantum.functional as tqf
import torch.nn.functional as F
import torch.optim as optim
from torchquantum.plugins.qiskit_plugin import tq2qiskit
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset
from qnn import QuantumSensing, QuantumML0


def compute_accuracy(output_all, target_all):
    _, indices = output_all.topk(1, dim=1)
    masks = indices.eq(target_all.view(-1, 1).expand_as(indices))
    size = target_all.shape[0]
    corrects = masks.sum().item()
    accuracy = corrects / size
    return accuracy

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
    model = QuantumML0(n_wires=n_qubits, n_locations=n_locations).to(device)
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
            bsz = thetas.shape[0]
            n_qubits = thetas.shape[1]
            qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=thetas, device=device)
            qstate = tq.QuantumState(n_wires=n_qubits, bsz=bsz)
            qsensing(qstate)
            q_device = tq.QuantumDevice(n_wires=n_qubits)
            q_device.reset_states(bsz=bsz)
            # the model
            outputs = model(q_device, qstate.states)
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
                bsz = thetas.shape[0]
                n_qubits = thetas.shape[1]
                qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=thetas, device=device)
                qstate = tq.QuantumState(n_wires=n_qubits, bsz=bsz)
                qsensing(qstate)
                q_device = tq.QuantumDevice(n_wires=n_qubits)
                q_device.reset_states(bsz=bsz)
                # the model
                outputs = model(q_device, qstate.states)
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



def main():
    num_sensor = 16
    for grid_length in [8, 10, 12, 14, 16]:
        train_test(grid_length, num_sensor)



if __name__ == '__main__':
    main()
