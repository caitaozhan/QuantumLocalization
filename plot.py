import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class Plot:

    @staticmethod
    def prob_heatmap(probs: list, n: int, filename: str):
        '''
        Args:
            probs -- a list of probability
            n     -- the length of probs is n**2, it is flattening a square
        '''
        grid = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                grid[i][j] = probs[n*i + j].real
        plt.subplots(figsize=(16, 16))
        sns.heatmap(grid, linewidth=0.1, vmin=0, vmax=0.5, annot=True)
        plt.savefig(filename)


    @staticmethod
    def povmloc_one_vary_gridsize(data):
        pass



def povmloc_one_varygridsize():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/onelevel.4sen.varygrid', 'results/onelevel.8sen.varygrid']
    # data = 


if __name__ == '__main__':

    povmloc_one_varygridsize()
