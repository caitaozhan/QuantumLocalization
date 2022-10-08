'''
Input and output parameters
'''

from dataclasses import dataclass
import json

@dataclass
class Input:
    continuous: bool  # whether the locations are continous during the testing phase
    level_length: int # by default, a level's length equals width, level one and level two has the same size
    noise: int        # the standard deviation of shadowing

    def __str__(self):
        return self.to_json_str()

    def to_json_str(self) -> str:
        '''return json formatting string
        '''
        inputdict = {
            'continuous': self.continuous,
            'level_length': self.level_length,
            'noise': self.noise
        }
        return json.dump(inputdict)

    @classmethod
    def from_json_str(cls, json_str: str) -> 'Input':
        '''init an Input object from json str
        '''
        indict = json.loads(json_str)
        return cls(indict['continuous'], indict['level_length'], indict['noise'])


@dataclass
class Output:
    method: str               # 'POVM-Loc One', 'POVM-Loc', 'POVM-Loc Pro', 'POVM_Loc Max'
    accuracy: float           # the metric when continuous == False, i.e., discrete case
    localization_error: float # the metric when continuous == True

    def __str__(self):
        return self.to_json_str()
    
    def to_json_str(self) -> str:
        outputdict = {
            'method': self.method,
            'accuracy': self.accuracy,
            'localization_error': self.localization_error
        }
        return json.dumps(outputdict)

    @classmethod
    def from_json_str(cls, json_str) -> 'Output':
        outdict = json.loads(json_str)
        return cls(outdict['method'], outdict['accuracy'], outdict['localization_error'])
