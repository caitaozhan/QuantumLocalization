'''
Some default numbers
'''

from dataclasses import dataclass

@dataclass
class Default:
    EPSILON: float         = 1e-8         # the epsilon for zero
    EPSILON_SEMIDEFINITE   = 8e-4         # relaxed for semidefinate programming optimal condition checking......
    grid_length_small: int = 4            # 4 x 4 grid
    cell_length: int       = 2            # in meters
    frequency: int         = 20 * 10**6 # 915 * 10**5  # Hz
    # frequency: int         = 900 * 10**6 # 915 * 10**5  # Hz
    amplitude_ref: float   = 0.1          # V/m, amplitude reference
    