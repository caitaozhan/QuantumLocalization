'''
Some default numbers
'''

from dataclasses import dataclass

@dataclass
class Default:
    EPSILON: float       = 1e-8         # the epsilon for zero
    EPSILON_SEMIDEFINITE = 8e-4         # relaxed for semidefinate programming optimal condition checking......
    grid_length: int     = 4            # 4 x 4 grid
    cell_length: int     = 10           # in meters
    # frequency: int       = 20 * 10**6 # 915 * 10**5  # Hz
    frequency: int       = 915 * 10**6 # 915 * 10**5  # Hz
    amplitude_ref: float = 0.01         # V/m, amplitude reference, the amplitude at 1 meters away from the TX
    power_ref: float     = -10          # dBm, power reference, the power at 1 meters away from the TX
    tx_power: float      = 0.1          # the power of the TX is 0.1 watt (approximately a WiFi AP)
    noise_floor: int     = -90          # dBm
    noise_floor_q: int   = -110         # dBm
    pathloss_expo: float = 3.5          # the path loss exponent for propagation model
    alpha_nf_q: float    = 0.1 
    std: float           = 0            # the std of noise or shadowing for propagation model

    method: str          = 'POVM-Loc'   # the localization method
    continuous: bool     = False        # whether the testing locations are continuous or not
    grid_length: int     = 16           # the grid's size is grid_length x grid_length
    sensor_num: int      = 4            # the number of sensors for the one level case
    repeat: int          = 1000         # repeat how many shots during the sensing protocol

    output_dir: str      = 'results'    # the director of of the logged output file
    output_file: str     = 'tmp'        # the filename of the logged output file

    # below are for simulated annealing
    init_step = 0.2                 # initial step size
    max_stuck = 5                   # max stuck in a same temperature
    cooling_rate = 0.96             # the annealing cooling rate
    stepsize_decreasing_rate = 0.96 # the stepsize decreasing rate
    EPSILON = 1e-6

    # below are for quantum ml
    root_dir = 'qml-data/toy'

    DEBUG = False
