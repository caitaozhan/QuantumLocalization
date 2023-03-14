'''
Model the unitary operator as a function of distance
From Xia Yi's PhD Thesis titled Distributed Quantum Sensing: Theoretical Foundation, Experimental Platform and Applications
Link: https://repository.arizona.edu/handle/10150/661283
'''

import numpy as np
import math
from scipy.linalg import expm
from scipy import constants
from typing import Tuple
from default import Default


class UnitaryOperator:
    def __init__(self, alpha: float, std: float, power_reference: float):
        self._alpha = alpha                                 # the alpha in the propagation model
        self._std = std                                     # the std in the propagation model
        self._power_reference = power_reference             # the RF signal's power at 1 meters
        # self._frequency = frequency                         # the RF signal's carrier frequency
        # self._amplitude_reference = amplitude_reference     # the RF signal's amplitude at 1 meter

    @property
    def alpha(self):
        return self._alpha

    @property
    def std(self):
        return self._std

    @property
    def power_reference(self):
        return self._power_reference

    # @property
    # def frequency(self):
    #     return self._frequency
    
    # @property
    # def amplitude_reference(self):
    #     return self._amplitude_reference
    
    # @property
    # def wave_length(self):
    #     return 3*10**8 / (self.frequency)
    
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

    def compute_amp(self, distance: float) -> Tuple[float, np.array]:
        '''making changes to work better, such as get rid of phase
        Args:
            distance -- the distance between the TX and RX
        Return:
            displacement     -- the displacement at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        TODO: 1) The amplitude model A = self.amplitude_reference / distance can be refined.
        '''
        def dist_modify(distance: float) -> float:
            return max(distance, 1)
        
        def amp2dbm(amp: float) -> float:
            '''amp (V) -> power (W) -> power (mW) -> power (dBm)
            '''
            power = 10*math.log10(amp**2 * 1000)
            return max(power, Default.noise_floor)
        
        def dbm_scaled(dbm: float) -> float:
            return dbm - Default.noise_floor

        c = 2 * np.pi / 80
        amp = self.amplitude_reference / dist_modify(distance)**2
        displacement = c * dbm_scaled(amp2dbm(amp))
        generator = np.array([[0.5, 0], [0, -0.5]])            # half of Pauli z matrix
        exponent = -complex(0, 1) * generator * displacement
        unitary_operator = expm(exponent)
        return displacement, unitary_operator


    def compute(self, distance: float, noise: bool = False) -> Tuple[float, np.array]:
        '''making changes to work better, such as get rid of phase
        Args:
            distance -- the distance between the TX and RX
            noise    -- whether consider the shadowing effect
        Return:
            phase shift      -- the phase shift at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        '''
        def dist_modify(distance: float) -> float:
            return max(distance, 1)
        
        c = 2 * np.pi / (Default.power_ref - Default.noise_floor)
        freespace = 10 * self.alpha * math.log10(dist_modify(distance))
        if noise:
            shadowing = np.random.normal(0, self.std)
            power = self._power_reference - freespace + shadowing
        else:
            power = self._power_reference - freespace
        power_scaled = max(power - Default.noise_floor, 0)     # power cannot be lower than noise floor
        phase_shift = c * power_scaled
        generator = np.array([[0.5, 0], [0, -0.5]])            # half of Pauli z matrix
        exponent = -complex(0, 1) * generator * phase_shift
        unitary_operator = expm(exponent)
        return phase_shift, unitary_operator


    def compute_new(self, distance: float, noise: bool = False, qsensor: bool = True) -> Tuple[float, np.array]:
        '''making changes to work better, such as get rid of phase
        Args:
            distance -- the distance between the TX and RX
            noise    -- whether consider the shadowing effect
        Return:
            phase shift      -- the phase shift at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        '''
        def dist_modify(distance: float) -> float:
            return max(distance, 1)
        
        c = 2 * (np.pi - Default.alpha_nf_q) / (Default.power_ref - Default.noise_floor_q)
        freespace = 10 * self.alpha * math.log10(dist_modify(distance))
        if noise:
            shadowing = np.random.normal(0, self.std)
            power = min(self._power_reference - freespace + shadowing, self._power_reference)
        else:
            power = self._power_reference - freespace
        if qsensor:
            power_sensed = max(power - Default.noise_floor_q, 0)     # power cannot be lower than noise floor
        else:
            power_sensed = max(power - Default.noise_floor, 0) + (Default.noise_floor - Default.noise_floor_q)
        phase_shift = c * power_sensed + Default.alpha_nf_q
        generator = np.array([[0.5, 0], [0, -0.5]])            # half of Pauli z matrix
        exponent = -complex(0, 1) * generator * phase_shift
        unitary_operator = expm(exponent)
        return phase_shift, unitary_operator


    def compute_H(self, distance: float, noise: bool = False) -> Tuple[float, np.array]:
        '''this version is based on Hamiltonian
        Args:
            distance -- the distance between the TX and RX
            noise    -- whether consider the shadowing effect
        Return:
            phase shift      -- the phase shift at the RF-Photonic senser
            unitary_operator -- the effect of the RF wave on the qubit at of the RF-Phonotic sensor
        '''
        def dist_modify(distance: float) -> float:
            return max(distance, Default.cell_length / 2)
        
        f = 10**9  # the frequency is 1GHz
        T = 1 / f  # time period of a cycle
        E = np.sqrt(30 * Default.tx_power) / (dist_modify(distance))  # electric field
        sensing_time = 0.1  # seconds
        n = sensing_time / T
        # to make 5 meters distance have a phase shift of 2pi
        E_5 = np.sqrt(30 * Default.tx_power) / (dist_modify(5))
        gamma = (np.pi**2 * constants.h) / (E_5 * sensing_time)
        phi_T = 2 / (np.pi * constants.h) * gamma * E * T
        phase_shift = n * phi_T
        generator = np.array([[0.5, 0], [0, -0.5]])            # half of Pauli z matrix
        exponent = -complex(0, 1) * generator * phase_shift
        unitary_operator = expm(exponent)
        return phase_shift, unitary_operator



def main1():
    from qiskit.quantum_info.operators.operator import Operator
    import matplotlib.pyplot as plt
    from utility import Utility
    plt.rcParams['font.size'] = 45
    plt.rcParams['lines.linewidth'] = 4

    # frequency = 900 * 10**6        # Hz
    # amplitude_reference = Default.amplitude_ref      # V/m
    alpha = Default.pathloss_expo
    std   = Default.std
    power_reference = Default.power_ref
    uo = UnitaryOperator(alpha, std, power_reference)
    X = []
    y = []
    for distance in np.linspace(1, 400, 101):
        # distance = i               # m
        # Utility.print_matrix('unitary operator', uo.compute(distance))
        # displacement, operator = uo.compute(distance)
        displacement, operator = uo.compute_H(distance)
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
    ax.set_ylim([0, 7])
    ax.set_title('Quantum Sensing Model')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Phase Shift')
    fig.savefig(f'tmp-hamiltonian.png')


if __name__ == '__main__':
    main1()
