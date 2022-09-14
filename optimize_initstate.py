import copy
import numpy as np
from typing import Tuple
from qiskit_textbook.tools import random_state
from qiskit.quantum_info.operators.operator import Operator
from quantum_state import QuantumState
from povm import Povm


class OptimizeInitialState:
    '''optimize the initial state
    '''
    def __init__(self, num_sensor: int):
        self.num_sensor = num_sensor


    def _normalize_state(self, state_vector: np.array) -> np.array:
        '''normalize a state vector
        '''
        magnitude_squared = sum([abs(a) ** 2 for a in state_vector])
        return state_vector / np.sqrt(magnitude_squared)

    def get_simple_initial_state(self, num: int) -> np.array:
        '''get an initial state that all amplitudes are equal real numbers
        '''
        amplitude = np.sqrt(1/(2**num))
        return np.array([amplitude + 0j]*2**num)
        # return np.array([amplitude]*2**num)

    def _evaluate(self, init_state: QuantumState, evolution_operators: list, priors: list, povm: Povm) -> Tuple[float, list]:
        '''evaluate a qstate using pretty good measurement and simulation
        Args:
            init_state -- the initial state to be evaluated
            evolution_operators -- a list of unitary operators
            priors -- a list of priors
            povm   -- positive operator valued measurement
        Return:
            (score, a list povm operator elements)
        '''
        quantum_states = []
        for operator in evolution_operators:
            init_state_copy = copy.deepcopy(init_state)
            init_state_copy.evolve(operator)
            quantum_states.append(init_state_copy)
        povm.pretty_good_measurement(quantum_states, priors, debug=False)
        # error = povm.simulate(quantum_states, priors, seed=0, repeat=1000)
        accuracy = povm.compute_theoretical_accuracy(quantum_states, priors)
        return accuracy.real, povm.operators


    def _find_neighbor(self, qstate: QuantumState, i: int, step_size: float) -> QuantumState:
        # return qstate
        real = 2 * np.random.random() - 1
        imag = 2 * np.random.random() - 1
        direction = real + 1j*imag
        direction /= abs(direction)
        state_vector = qstate.state_vector.copy()
        state_vector[i] += direction * step_size
        normalized_vector = self._normalize_state(state_vector)
        return QuantumState(self.num_sensor, normalized_vector)


    def _generate_init_temperature(self, qstate: QuantumState, init_step: float, init_temp_neighbors: int, evolution_operators: Operator, priors: list, povm: Povm):
        scores = []
        for i in range(init_temp_neighbors):
            neighbor = self._find_neighbor(qstate, i, init_step)
            score, _ = self._evaluate(neighbor, evolution_operators, priors, povm)
            scores.append(score)
        return np.std(scores)


    def simulated_annealing(self, max_time: float, num_sensor: int, evolution_operators: list, priors: list, init_step: float, stepsize_decreasing_rate: float,
                            epsilon: float, max_stuck: int, cooling_rate: float) -> Tuple[QuantumState, list]:
        '''optimize the initial state by simulated annealing
        Args:
            num_sensor -- number of sensors
            evolution_operators -- a list of unitary operators
        Return:
            (the initial state, list of povm operators)
        '''
        print('start simulated annealing')
        np.random.seed(num_sensor)
        povm = Povm()
        # qstate = QuantumState(num_sensor, random_state(nqubits=num_sensor))
        qstate = QuantumState(num_sensor, self.get_simple_initial_state(num=num_sensor))
        N = 2 ** num_sensor
        init_temp_neighbors = 10
        # init_temperature = self._generate_init_temperature(qstate, init_step, init_temp_neighbors, evolution_operators, priors, povm)
        init_temperature = 0.00000000001
        temperature = init_temperature
        score1, povm_operators1 = self._evaluate(qstate, evolution_operators, priors, povm)
        scores = [score1]
        terminate = False
        stuck_count = 0
        std_ratio = 1
        stepsize = init_step
        while terminate is False:
            previous_score = score1
            scores_iteration = []
            for i in range(N):
                for _ in range(4):
                    neighbor = self._find_neighbor(qstate, i, stepsize)
                    score2, povm_operators2 = self._evaluate(neighbor, evolution_operators, priors, povm)
                    scores_iteration.append(score2)
                    dS = score2 - score1   # score2 is the score of the neighbor state, score1 is for current state
                    if dS > 0:                     # qstate improves
                        qstate = neighbor
                        score1 =  score2
                        povm_operators1 = povm_operators2
                    else:
                        prob = np.exp(dS / temperature)
                        if np.random.uniform(0, 1) <  prob:
                            qstate = neighbor      # qstate becomes worse
                            score1 = score2
                            povm_operators1 = povm_operators2
                        else:
                            pass                   # qstate no change
            scores.append(score1)
            if previous_score >= score1 - epsilon:
                stuck_count += 1
            else:
                stuck_count = 0
                terminate = False
            if stuck_count == max_stuck:
                terminate = True

            std = np.std(scores_iteration[-10:])
            std_ratio *= cooling_rate
            temperature = min(temperature * cooling_rate, std * std_ratio)
            stepsize *= stepsize_decreasing_rate
        
        return qstate, povm_operators1
