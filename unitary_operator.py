'''
Model the unitary operator as a function of distance
'''

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
    
