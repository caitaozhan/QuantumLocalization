'''the dataset
'''

import os
import numpy as np
from torch.utils.data import Dataset


class QuantumSensingDataset(Dataset):
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.phase_dir = os.path.join(root_dir, 'phase')
        self.label_dir = os.path.join(root_dir, 'label')
        if len(os.listdir(self.phase_dir)) != os.listdir(self.label_dir):
            raise Exception('phase and label number are not equal')
        self.length = len(os.listdir(self.phase_dir))
    
    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        phase_path = os.path.join(self.phase_dir, f'{idx}.npy')
        label_path = os.path.join(self.label_dir, f'{idx}.npy')
        phase = np.load(phase_path)
        label = np.load(label_path)
        sample = {'phase': phase, 'label': label}
        return sample
