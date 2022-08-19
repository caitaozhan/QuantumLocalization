'''
Model the unitary operator as a function of distance
From Xia Yi's PhD Thesis titled Distributed Quantum Sensing: Theoretical Foundation, Experimental Platform and Applications
Link: https://repository.arizona.edu/handle/10150/661283
'''

import numpy as np
import math
from scipy.linalg import expm
from typing import Tuple
from default import Default


class UnitaryOperator:
    def __init__(self, frequency: float, amplitude_reference: float):
        self._frequency = frequency                         # the RF signal's carrier frequency
        self._amplitude_reference = amplitude_reference     # the RF signal's amplitude at 1 meter
    
    @property
    def frequency(self):
        return self._frequency
    
    @property
    def amplitude_reference(self):
        return self._amplitude_reference
    
    @property
    def wave_length(self):
        return 3*10**8 / (self.frequency)
    
    # def compute(self, distance: float) -> Tuple[float, np.array]:
    def compute_arizona(self, distance: float) -> Tuple[float, np.array]:
        '''sticking to the Arizona RF Photonic sensing
        Args:
            distance -- the distance between the TX and RX
        Return:
            displacement     -- the displacement at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        TODO: 1) The amplitude model A = self.amplitude_reference / distance can be refined.
              2) rethink quadrature operator and Pauli z matrix
        '''
        c = 100
        delta_distance = math.fmod(distance, self.wave_length)
        displacement = c * self.amplitude_reference / distance * np.sin(2 * np.pi * delta_distance / self.wave_length)
        generator = np.array([[0, complex(0, 0.5)], [-complex(0, 0.5), 0]])   # quadrature operator
        exponent = -complex(0, 1) * generator * displacement
        unitary_operator = expm(exponent)
        return displacement, unitary_operator

    def compute(self, distance: float) -> Tuple[float, np.array]:
        '''making changes to work better, such as get rid of phase
        Args:
            distance -- the distance between the TX and RX
        Return:
            displacement     -- the displacement at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        TODO: 1) The amplitude model A = self.amplitude_reference / distance can be refined.
        '''
        def dist_modify(distance: float) -> float:
            # return max(distance, 0.5)
            return distance
        
        def amp2dbm(amp: float) -> float:
            '''amp (V) -> power (W) -> power (mW) -> power (dBm)
            '''
            power = 10*math.log10(amp**2 * 1000)
            return max(power, Default.noise_floor)
        
        def dbm_scaled(dbm: float) -> float:
            return dbm - Default.noise_floor

        c = 0.1
        amp = self.amplitude_reference / dist_modify(distance)
        displacement = c * dbm_scaled(amp2dbm(amp))
        generator = np.array([[0.5, 0], [0, -0.5]])            # half of Pauli z matrix
        exponent = -complex(0, 1) * generator * displacement
        unitary_operator = expm(exponent)
        return displacement, unitary_operator

def main1():
    from qiskit.quantum_info.operators.operator import Operator
    import matplotlib.pyplot as plt
    from utility import Utility
    plt.rcParams['font.size'] = 45
    plt.rcParams['lines.linewidth'] = 4

    frequency = 900 * 10**6        # Hz
    amplitude_reference = 0.1      # V/m
    uo = UnitaryOperator(frequency, amplitude_reference)
    X = []
    y = []
    for distance in np.linspace(0.1, 10, 901):
        # distance = i               # m
        # Utility.print_matrix('unitary operator', uo.compute(distance))
        displacement, operator = uo.compute(distance)
        op = Operator(operator)
        X.append(distance)
        y.append(displacement)
        print(f'distance={distance:.2f}, displacement={displacement}, is unitary={op.is_unitary()}')
        # operator_inv = np.linalg.inv(operator)
        # operator_ct = operator.conjugate().transpose()
        Utility.print_matrix('operator', operator)
        # Utility.print_matrix('inverse', operator_inv)
        # Utility.print_matrix('conjugate transpose', operator_ct)
        # break
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.9, bottom=0.15)
    ax.plot(X, y)
    ax.set_title('RF-Photonic Sensing')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Phase Quadrature Displacement')
    fig.savefig('tmp.png')


if __name__ == '__main__':
    main1()
