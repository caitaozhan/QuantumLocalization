'''
logging the input and outputs
'''

import os
from io import TextIOWrapper
from input_output import Input, Output
from typing import List


class MyLogger:
    def __init__(self, output_dir: str, output_file: str):
        self.output = self.init_output(output_dir, output_file)
    
    def init_output(self, output_dir: str, output_file: str) -> 'TextIOWrapper':
        '''set up output file
        '''
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        return open(os.path.join(output_dir, output_file), 'a')
    
    def log(self, myinput: Input, outputs: List[Output]):
        '''log the results
        '''
        self.output.write(f'{myinput}\n')
        for output in outputs:
            self.output.write(f'{output}\n')
        self.output.write('\n')
        self.output.flush()

