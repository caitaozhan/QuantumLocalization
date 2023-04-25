'''
Input and output parameters
'''

from dataclasses import dataclass
import json
from typing import Tuple


@dataclass
class Input:
    ground_truth: Tuple  # the truth location of the transmitter
    grid_length: int     # by default, length equal width, i.e., a square
    sensor_num: int      # the number of sensors for the one level method (for two levels, the sensors are fixed)
    noise: int           # the standard deviation of shadowing
    continuous: bool     # whether the locations are continous during the testing phase
    ibm: bool = False    # whether testing on IBM quantum computer

    def __str__(self):
        return self.to_json_str()

    def to_json_str(self) -> str:
        '''return json formatting string
        '''
        inputdict = {
            'ground_truth': self.ground_truth,
            'grid_length': self.grid_length,
            'sensor_num': self.sensor_num,
            'noise': self.noise,
            'continuous': self.continuous,
            'ibm': self.ibm
        }
        return json.dumps(inputdict)

    @classmethod
    def from_json_str(cls, json_str: str) -> 'Input':
        '''init an Input object from json str
        '''
        indict = json.loads(json_str)
        ibm = indict['ibm'] if indict['ibm'] else False
        return cls(indict['ground_truth'], indict['grid_length'], indict['sensor_num'], indict['noise'], indict['continuous'], ibm)


@dataclass
class Output:
    method: str               # 'POVM-Loc One', 'POVM-Loc', 'POVM-Loc Pro', 'POVM_Loc Max'
    correct: float            # the metric when continuous == False, either correct or incorrect
    localization_error: float # the metric when continuous == True
    pred: Tuple               # the predicted location
    elapse: float             # the time

    def __str__(self):
        return self.to_json_str()
    
    def to_json_str(self) -> str:
        outputdict = {
            'method': self.method,
            'correct': self.correct,
            'localization_error': self.localization_error,
            'pred': self.pred,
            'elapse': self.elapse
        }
        return json.dumps(outputdict)

    @classmethod
    def from_json_str(cls, json_str) -> 'Output':
        outdict = json.loads(json_str)
        return cls(outdict['method'], outdict['correct'], outdict['localization_error'], outdict['pred'], outdict['elapse'])
