from collections import defaultdict
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tabulate
from utility import Utility


class Plot:

    plt.rcParams['font.size'] = 60
    plt.rcParams['lines.linewidth'] = 10
    plt.rcParams['lines.markersize'] = 35

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
    def reduce_accuracy(vals: list):
        '''vals is a list of True/False bools
        '''
        vals = [val for val in vals if val is not None]
        if vals:
            return vals.count(True) / len(vals)
        else:
            return 0

    @staticmethod
    def povmloc_one_vary_gridsize(data: list, figname: str):
        reduce = Plot.reduce_accuracy
        # step 1: prepare data
        table = defaultdict(list)
        for myinput, output_by_method in data:
            table[myinput.grid_length].append({myinput.sensor_num: output.correct for output in output_by_method.values()})
        
        print_table = []
        sensornum = [4, 8]
        for x, list_of_y_by_sensornum in sorted(table.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        X      = arr[:, 0]
        y_4sen = arr[:, 1] * 100  # percentage
        y_8sen = arr[:, 2] * 100

        # step 2: plotting
        fig, ax = plt.subplots(1, 1, figsize=(25, 18))
        fig.subplots_adjust(left=0.14, right=0.99, top=0.9, bottom=0.14)
        ax.plot(X, y_8sen, linestyle='--', marker='P', label="8 Quantum Sensors", mfc='r', mec='b')
        ax.plot(X, y_4sen, linestyle='-',  marker='^', label="4 Quantum Sensors", mfc='r', mec='b')
        fig.legend(ncol=1, loc='lower left', bbox_to_anchor=(0.14, 0.14), fontsize=52)
        ax.set_xlabel('Grid Size', labelpad=20)
        ax.set_xticks(X)
        ax.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=3, labelsize=50)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=3)
        ax.set_ylabel('Localization Accuracy (%)', fontsize=70, labelpad=20)
        ax.set_title('The Performance of POVM-Loc-OneLevel', pad=30)
        fig.savefig(figname)




def povmloc_one_varygridsize():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/onelevel.4sen.varygrid', 'results/onelevel.8sen.varygrid']
    data = Utility.read_logs(logs)
    figname = 'results/tmp.onelevel-varygrid.png'
    Plot.povmloc_one_vary_gridsize(data, figname)


if __name__ == '__main__':

    povmloc_one_varygridsize()
