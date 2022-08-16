'''for testing purpose
'''
from localization import QuantumLocalization
from default import Default
from unitary_operator import UnitaryOperator


def test_localization():
    sensordata = 'sensordata/4x4-twolevel.json'
    unitary_operator = UnitaryOperator(Default.frequency, Default.amplitude_ref)
    initial_state = 'simple'
    ql = QuantumLocalization(grid_length=Default.grid_length_small, cell_length=Default.cell_length,
                             sensordata_filename=sensordata, unitary_operator=unitary_operator)
    ql.training_fourstate_povm(initial_state)

if __name__ == '__main__':
    test_localization()
