import torch
import torch.nn as nn
import torch.nn.functional as F
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np
from torch.utils.data import DataLoader
from dataset import QuantumSensingDataset


class QuantumSensing(tq.QuantumModule):
    '''Model the quantum sensing process (state preparation).
       For a single quantum state
    '''
    def __init__(self, n_qubits: int, list_of_thetas: list, device: torch.device):
        '''
        Params:
            n_qubits       -- number of qubits
            list_of_thetas -- a list of (list of parameters) for the RZ gate
        '''
        super().__init__()
        if n_qubits != len(list_of_thetas[0]):
            raise Exception('n_qubit != len(thetas)')
        self.n_wires = n_qubits
        self.device = device
        self.bsz = len(list_of_thetas)
        self.rzs = []
        for thetas in list_of_thetas:
            self.rzs.append([tq.RZ(has_params=True, init_params=theta.item()) for theta in thetas])

    def forward(self, q_state: tq.QuantumState):
        q_state_list = []
        for i in range(self.bsz):
            q_state_tmp = tq.QuantumState(n_wires=self.n_wires, bsz=1)
            for j in range(self.n_wires):
                tqf.h(q_state_tmp, wires=j)       # hadamard gate --> super position
            for j, rz in enumerate(self.rzs[i]):
                rz(q_state_tmp, wires=j)          # quantum sensing model
            q_state_list.append(q_state_tmp.states)
        q_state_concat = torch.cat(q_state_list).to(self.device)
        q_state.clone_states(q_state_concat)


# quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
class QuantumML0(tq.QuantumModule):
    ''' the quantum layer part is tq.layers.U3CU3Layer0 (4 blocks)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
        self.quantum_layer = tq.layers.U3CU3Layer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
class QuantumML1(tq.QuantumModule):
    '''the quantum layer part is tq.layers.RXYZCXLayer0 (4 blocks)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
        self.quantum_layer = tq.layers.RXYZCXLayer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# quantum-classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
class QuantumML2(tq.QuantumModule):
    '''the quantum layer part is tq.layers.RXYZCXLayer0 (1 block)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 1, 'n_layers_per_block': 2}
        self.quantum_layer = tq.layers.RXYZCXLayer0(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# non-trainable version of RXYZCX
class MyRXYZCXLayer(tq.layers.LayerTemplate0):
    def build_layers(self):
        layers_all = tq.QuantumModuleList()
        for _ in range(self.arch['n_blocks']):
            layers_all.append(tq.Op1QAllLayer(op=tq.RX, n_wires=self.n_wires, has_params=True, trainable=False))
            layers_all.append(tq.Op1QAllLayer(op=tq.RY, n_wires=self.n_wires, has_params=True, trainable=False))
            layers_all.append(tq.Op1QAllLayer(op=tq.RZ, n_wires=self.n_wires, has_params=True, trainable=False))
            layers_all.append(tq.Op2QAllLayer(op=tq.CNOT, n_wires=self.n_wires, jump=1, circular=True))
        return layers_all


# quantum-classic hybrid that consists of both a (non-trainable) quantum convolutional layer and classical fully connected layer
class QuantumML3(tq.QuantumModule):
    '''the quantum layer part is MyRXYZCXLayer (4 block)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 4, 'n_layers_per_block': 2}
        self.quantum_layer = MyRXYZCXLayer(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# quantum-classic hybrid that consists of both a (non-trainable) quantum convolutional layer and classical fully connected layer
class QuantumML4(tq.QuantumModule):
    '''the quantum layer part is MyRXYZCXLayer (1 block)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.arch = {'n_wires': self.n_wires, 'n_blocks': 1, 'n_layers_per_block': 2}
        self.quantum_layer = MyRXYZCXLayer(self.arch)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        self.quantum_layer(q_device)
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


# no quantum convolutional layer, only classical fully connected layer
class NoQuantumML(tq.QuantumModule):
    '''the quantum layer part is MyRXYZCXLayer (1 block)
    '''
    def __init__(self, n_wires, n_locations):
        super().__init__()
        self.n_wires = n_wires
        self.q_device = tq.QuantumDevice(n_wires=self.n_wires)
        self.measure = tq.MeasureAll(tq.PauliZ)
        self.linear = nn.Linear(n_wires, n_locations)
    
    def forward(self, q_device: tq.QuantumDevice, input_states: torch.tensor):
        q_device.set_states(input_states)
        # quantum part
        x = self.measure(q_device)
        # classical part
        x = self.linear(x)
        return F.log_softmax(x, -1)


def test():
    n_qubits = 4
    n_locations = 4
    batch_size = 1
    list_of_thetas = [[np.pi/0.8, np.pi/1.2, np.pi/2.2, np.pi/3],
                      [np.pi/0.7, np.pi/1.7, np.pi/2.7, np.pi/3.5],
                      [np.pi/0.9, np.pi/2.1, np.pi/2.9, np.pi/3.9]]
    qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=list_of_thetas)
    qlocalize = QuantumML0(n_wires=n_qubits, n_locations=n_locations)
    q_device = tq.QuantumDevice(n_wires=n_qubits)
    q_device.reset_states(bsz=batch_size)
    state = tq.QuantumState(n_wires=n_qubits, bsz=2)
    qsensing(state)
    outputs = qlocalize(q_device, state.states)
    print(outputs)


def test2():
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    qlocalize = QuantumML0(n_wires=4, n_locations=4)
    root_dir = 'qml-data/toy/train'
    train_dataset = QuantumSensingDataset(root_dir)
    train_dataloader = DataLoader(train_dataset, batch_size=3, shuffle=False, num_workers=2)
    for t, sample in enumerate(train_dataloader):
        X = sample['phase']
        y = sample['label']
        bsz = X.shape[0]
        n_qubits = X.shape[1]
        qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=X, device=device)
        qstate = tq.QuantumState(n_wires=n_qubits, bsz=bsz)
        qsensing(qstate)
        print(qstate)
        q_device = tq.QuantumDevice(n_wires=n_qubits)
        q_device.reset_states(bsz=bsz)
        outputs = qlocalize(q_device, qstate.states)
        print(outputs)
        break


if __name__ == '__main__':
    # test()
    test2()
