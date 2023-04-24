import torch
import torch.nn as nn
import torch.nn.functional as F
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset
from torchquantum.plugins import (
    op_history2qiskit_expand_params_and_fixed,
    op_history2qiskit,
    tq2qiskit_measurement,
    qiskit_assemble_circs
)



class QuantumSensing(tq.QuantumModule):
    '''Model the quantum sensing process (state preparation).
       For a single quantum state
    '''
    def __init__(self, n_qubits: int, device: torch.device):
        '''
        Params:
            n_qubits       -- number of qubits
            device     -- which classical device to use, 'cpu' or 'gpu'
        '''
        super().__init__()
        self.n_wires = n_qubits
        self.device = device

    def forward(self, list_of_thetas: list):
        '''         
        Args:
            list_of_thetas -- a list of (list of parameters) for the RZ gate
        Return:
            tq.QuantumDevice
        '''
        if self.n_wires != len(list_of_thetas[0]):
            raise Exception('n_qubit != len(thetas)')

        bsz = len(list_of_thetas)
        q_device = tq.QuantumDevice(n_wires=self.n_wires, bsz=bsz, device=self.device)
        rzs = []    # rotation z basis 
        for thetas in list_of_thetas:
            rzs.append([tq.RZ(has_params=True, init_params=theta.item()) for theta in thetas])

        q_state_list = []
        for i in range(bsz):
            q_device_tmp = tq.QuantumDevice(n_wires=self.n_wires, bsz=1)
            for j in range(self.n_wires):
                tqf.h(q_device_tmp, wires=j)       # hadamard gate --> super position
            for j, rz in enumerate(rzs[i]):
                rz(q_device_tmp, wires=j)          # quantum sensing model
            q_state_list.append(q_device_tmp.states)
        q_device.set_states(torch.cat(q_state_list).to(self.device))
        return q_device


# quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
class QuantumMLclassification(tq.QuantumModule):
    ''' the quantum layer part is tq.layers.U3CU3Layer0 (4 blocks)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
        self.quantum_layer = tq.layers.U3CU3Layer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice):
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
class QuantumMLregression(tq.QuantumModule):
    ''' the quantum layer part is tq.layers.U3CU3Layer0 (4 blocks)
        the output is not a discrete cell, but a continuous location (x, y)
    '''
    def __init__(self, n_wires):
        super().__init__()
        self.n_wires = n_wires
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4}
        self.quantum_layer = tq.layers.U3CU3Layer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, 2)  # (x, y)
    
    def forward(self, q_device: tq.QuantumDevice):
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        loc = self.linear(x)
        return loc


class QuantumMLregressionIBM(tq.QuantumModule):
    '''the IBM implementation for class QuantumMLregression
       currently for 4 qubits only
    '''

    qsn_encoder = [
        {"input_idx": [],  "func": "h",  "wires": [0]},
        {"input_idx": [],  "func": "h",  "wires": [1]},
        {"input_idx": [],  "func": "h",  "wires": [2]},
        {"input_idx": [],  "func": "h",  "wires": [3]},
        {"input_idx": [0], "func": "rz", "wires": [0]},
        {"input_idx": [1], "func": "rz", "wires": [1]},
        {"input_idx": [2], "func": "rz", "wires": [2]},
        {"input_idx": [3], "func": "rz", "wires": [3]},
    ]

    def __init__(self, n_wires):
        super().__init__()
        self.n_wires = n_wires
        self.encoder = tq.GeneralEncoder(QuantumMLregressionIBM.qsn_encoder)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4}
        self.quantum_layer = tq.layers.U3CU3Layer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, 2)

    def forward(self, x, use_qiskit=False):
        '''x is the tensor of phase shifts in batches
        '''
        bsz = x.shape[0]
        device = x.device
        qdev = tq.QuantumDevice(n_wires=self.n_wires, bsz=bsz, device=device, record_op=True)
        if use_qiskit:
            self.encoder(qdev, x)
            op_history_parameterized = qdev.op_history
            qdev.reset_op_history()
            encoder_circ = op_history2qiskit_expand_params_and_fixed(self.n_wires, op_history_parameterized, bsz=bsz)
            self.quantum_layer(qdev)
            op_history_fixed = qdev.op_history
            qdev.reset_op_history()
            quantum_layer_circ = op_history2qiskit(self.n_wires, op_history_fixed)
            measurement_circ = tq2qiskit_measurement(qdev, self.measure)

            assembed_circs = qiskit_assemble_circs(encoder_circ, quantum_layer_circ, measurement_circ)
            x = self.qiskit_processor.process_ready_circs(qdev, assembed_circs).to(torch.float32).to(device)

        else:
            self.encoder(qdev, x)
            self.quantum_layer(qdev)
            x = self.measure(qdev)

        loc = self.linear(x)
        return loc
    




# # quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
# class QuantumML1(tq.QuantumModule):
#     '''the quantum layer part is tq.layers.RXYZCXLayer0 (4 blocks)
#     '''
#     def __init__(self, n_wires, n_locations):
#         super().__init__()
#         self.n_wires = n_wires
#         self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
#         self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
#         self.quantum_layer = tq.layers.RXYZCXLayer0(self.arch)
#         self.measure = tq.MeasureAll(tq.PauliZ)
#         self.linear = nn.Linear(n_wires, n_locations)
    
#     def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
#         q_device.set_states(input_states)
#         # quantum part
#         self.quantum_layer(q_device)
#         x = self.measure(q_device)
#         # classical part
#         x = self.linear(x)
#         return F.log_softmax(x, -1)


# # quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
# class QuantumML2(tq.QuantumModule):
#     '''the quantum layer part is tq.layers.RXYZCXLayer0 (1 block)
#     '''
#     def __init__(self, n_wires, n_locations):
#         super().__init__()
#         self.n_wires = n_wires
#         self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
#         self.arch = {'n_wires': self.n_wires, 'n_blocks': 1, 'n_layers_per_block': 2}
#         self.quantum_layer = tq.layers.RXYZCXLayer0(self.arch)
#         self.measure = tq.MeasureAll(tq.PauliZ)
#         self.linear = nn.Linear(n_wires, n_locations)
    
#     def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
#         q_device.set_states(input_states)
#         # quantum part
#         self.quantum_layer(q_device)
#         x = self.measure(q_device)
#         # classical part
#         x = self.linear(x)
#         return F.log_softmax(x, -1)


# # non-trainable version of RXYZCX
# class MyRXYZCXLayer(tq.layers.LayerTemplate0):
#     def build_layers(self):
#         layers_all = tq.QuantumModuleList()
#         for _ in range(self.arch['n_blocks']):
#             layers_all.append(tq.Op1QAllLayer(op=tq.RX, n_wires=self.n_wires, has_params=True, trainable=False))
#             layers_all.append(tq.Op1QAllLayer(op=tq.RY, n_wires=self.n_wires, has_params=True, trainable=False))
#             layers_all.append(tq.Op1QAllLayer(op=tq.RZ, n_wires=self.n_wires, has_params=True, trainable=False))
#             layers_all.append(tq.Op2QAllLayer(op=tq.CNOT, n_wires=self.n_wires, jump=1, circular=True))
#         return layers_all


# # quantum-classic hybrid that consists of both a (non-trainable) quantum convolutional layer and classical fully connected layer
# class QuantumML3(tq.QuantumModule):
#     '''the quantum layer part is MyRXYZCXLayer (4 block)
#     '''
#     def __init__(self, n_wires, n_locations):
#         super().__init__()
#         self.n_wires = n_wires
#         self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
#         self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
#         self.quantum_layer = MyRXYZCXLayer(self.arch)
#         self.measure = tq.MeasureAll(tq.PauliZ)
#         self.linear = nn.Linear(n_wires, n_locations)
    
#     def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
#         q_device.set_states(input_states)
#         # quantum part
#         self.quantum_layer(q_device)
#         x = self.measure(q_device)
#         # classical part
#         x = self.linear(x)
#         return F.log_softmax(x, -1)


# # quantum-classic hybrid that consists of both a (non-trainable) quantum convolutional layer and classical fully connected layer
# class QuantumML4(tq.QuantumModule):
#     '''the quantum layer part is MyRXYZCXLayer (1 block)
#     '''
#     def __init__(self, n_wires, n_locations):
#         super().__init__()
#         self.n_wires = n_wires
#         self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
#         self.arch = {'n_wires': self.n_wires, 'n_blocks': 1, 'n_layers_per_block': 2}
#         self.quantum_layer = MyRXYZCXLayer(self.arch)
#         self.measure = tq.MeasureAll(tq.PauliZ)
#         self.linear = nn.Linear(n_wires, n_locations)
    
#     def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
#         q_device.set_states(input_states)
#         # quantum part
#         self.quantum_layer(q_device)
#         x = self.measure(q_device)
#         # classical part
#         x = self.linear(x)
#         return F.log_softmax(x, -1)


# # no quantum convolutional layer, only classical fully connected layer
# class NoQuantumML(tq.QuantumModule):
#     '''the quantum layer part is MyRXYZCXLayer (1 block)
#     '''
#     def __init__(self, n_wires, n_locations):
#         super().__init__()
#         self.n_wires = n_wires
#         self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
#         self.measure = tq.MeasureAll(tq.PauliZ)
#         self.linear = nn.Linear(n_wires, n_locations)
    
#     def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
#         q_device.set_states(input_states)
#         # quantum part
#         x = self.measure(q_device)
#         # classical part
#         x = self.linear(x)
#         return F.log_softmax(x, -1)


def test():
    n_qubits = 4
    n_locations = 4
    list_of_thetas = [[np.pi/0.8, np.pi/1.2, np.pi/2.2, np.pi/3],
                      [np.pi/0.7, np.pi/1.7, np.pi/2.7, np.pi/3.5],
                      [np.pi/0.9, np.pi/2.1, np.pi/2.9, np.pi/3.9]]
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    qlocalize = QuantumMLclassification(n_wires=n_qubits, n_locations=n_locations)
    qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
    q_device = qsensing(list_of_thetas)
    outputs = qlocalize(q_device)
    print(outputs)


def test2():
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    qlocalize = QuantumMLclassification(n_wires=4, n_locations=4).to(device)
    root_dir = 'qml-data/toy/train'
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=3, shuffle=False, num_workers=2)
    for t, sample in enumerate(train_dataloader):
        X = sample['phase']
        y = sample['label']
        n_qubits = X.shape[1]
        qsensing = QuantumSensing(n_qubits=n_qubits, device=device)
        q_device = qsensing(X)
        outputs = qlocalize(q_device)
        print(outputs)
        break


if __name__ == '__main__':
    # test()
    test2()
