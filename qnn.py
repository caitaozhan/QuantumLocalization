import torch
import torch.nn as nn
import torch.nn.functional as F
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np



class QuantumSensing(tq.QuantumModule):
    '''Model the quantum sensing process (state preparation).
       For a single quantum state
    '''
    def __init__(self, n_qubits: int, list_of_thetas: list):
        '''
        Params:
            n_qubits       -- number of qubits
            list_of_thetas -- a list of (list of parameters) for the RZ gate
        '''
        super().__init__()
        if n_qubits != len(list_of_thetas[0]):
            raise Exception('n_qubit != len(thetas)')
        self.bsz = len(list_of_thetas)
        self.n_wires = n_qubits
        self.q_state = tq.QuantumState(n_wires=self.n_wires)
        self.rzs = []
        for thetas in list_of_thetas:
            self.rzs.append([tq.RZ(has_params=True, init_params=theta) for theta in thetas])
    
    def forward(self, q_state: tq.QuantumState):
        q_state_list = []
        for i in range(self.bsz):
            q_state_tmp = tq.QuantumState(n_wires=self.n_wires, bsz=1)
            for j in range(self.n_wires):
                tqf.h(q_state_tmp, wires=j)       # hadamard gate --> super position
            for j, rz in enumerate(self.rzs[i]):
                rz(q_state_tmp, wires=j)          # quantum sensing model
            q_state_list.append(q_state_tmp.states)
        q_state_concat = torch.cat(q_state_list)
        q_state.set_states(q_state_concat)



class QuantumML(tq.QuantumModule):
    '''the localization part is quantum classic hybrid that consists of both a quantum convolutional layer and classical fully connected layer
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


def test():
    n_qubits = 4
    n_locations = 4
    batch_size = 1
    list_of_thetas = [[np.pi/0.8, np.pi/1.2, np.pi/2.2, np.pi/3],
                      [np.pi/0.7, np.pi/1.7, np.pi/2.7, np.pi/3.5],
                      [np.pi/0.9, np.pi/2.1, np.pi/2.9, np.pi/3.9]]
    qsensing = QuantumSensing(n_qubits=n_qubits, list_of_thetas=list_of_thetas)
    qlocalize = QuantumML(n_wires=n_qubits, n_locations=n_locations)
    q_device = tq.QuantumDevice(n_wires=n_qubits)
    q_device.reset_states(bsz=batch_size)
    state = tq.QuantumState(n_wires=n_qubits, bsz=2)
    qsensing(state)
    outputs = qlocalize(q_device, state.states)
    print(outputs)



if __name__ == '__main__':
    test()
