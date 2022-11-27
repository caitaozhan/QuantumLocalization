import torch
import torch.nn as nn
import torch.nn.functional as F
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np



class QuantumSensing(tq.QuantumModule):
    '''Model the quantum sensing process (state preparation)
    '''
    def __init__(self, n_qubits: int, thetas: list):
        '''
        Params:
            thetas -- a list of parameters for the RZ gate
        '''
        super().__init__()
        if n_qubits != len(thetas):
            raise Exception('n_qubit != len(thetas)')
        self.n_wires = n_qubits
        self.q_state = tq.QuantumState(n_wires=self.n_wires)
        self.hs =  [tq.H() for _ in range(self.n_wires)]
        self.rzs = [tq.RZ(has_params=True, init_params=theta) for theta in thetas]
    
    def forward(self, q_state: tq.QuantumState):
        q_state.reset_states(1)
        for i, h in enumerate(self.hs):    # hadamard gate --> super position
            h(q_state, wires=i)
        for i, rz in enumerate(self.rzs):  # quantum sensing model
            rz(q_state, wires=i)



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
    thetas = [np.pi/0.8, np.pi/1.2, np.pi/2.2, np.pi/3]
    qsensing = QuantumSensing(n_qubits=n_qubits, thetas=thetas)
    qlocalize = QuantumML(n_wires=n_qubits, n_locations=n_locations)
    q_device = tq.QuantumDevice(n_wires=n_qubits)
    q_device.reset_states(bsz=batch_size)
    state = tq.QuantumState(n_wires=n_qubits, bsz=1)
    qsensing(state)
    outputs = qlocalize(q_device, state.states)
    print(outputs)



if __name__ == '__main__':
    test()
