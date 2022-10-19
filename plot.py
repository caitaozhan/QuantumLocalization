from collections import defaultdict
from distutils.log import error
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tabulate
from utility import Utility


class Plot:

    plt.rcParams['font.size'] = 65
    plt.rcParams['lines.linewidth'] = 10
    plt.rcParams['lines.markersize'] = 35
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'

    METHOD  = ['povmloc-one',          'povmloc',  'povmloc-pro']
    _LEGEND = ['OneLevel', 'POVM-Loc', 'POVM-Loc Pro']
    LEGEND  = dict(zip(METHOD, _LEGEND))

    METHOD  = ['povmloc-one', 'povmloc', 'povmloc-pro']
    _COLOR  = ['tab:orange',  'blue',    'r']
    COLOR   = dict(zip(METHOD, _COLOR))

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
    def reduce_accuracy(vals: list) -> float:
        '''vals is a list of True/False bools
        '''
        vals = [val for val in vals if val is not None]
        if vals:
            return vals.count(True) / len(vals)
        else:
            return 0


    @staticmethod
    def reduce_average(vals: list) -> float:
        '''vals is a list of float
        '''
        vals = [val for val in vals if val is not None]
        return np.mean(vals)


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
        fig.subplots_adjust(left=0.14, right=0.98, top=0.9, bottom=0.14)
        ax.plot(X, y_8sen, linestyle='-',  marker='^', label="8 Quantum Sensors", mfc='black', mec='b', color=Plot.COLOR['povmloc-one'])
        ax.plot(X, y_4sen, linestyle='--', marker='^', label="4 Quantum Sensors", mfc='black', mec='b', color=Plot.COLOR['povmloc-one'])
        fig.legend(ncol=1, loc='lower left', bbox_to_anchor=(0.14, 0.14), fontsize=52, handlelength=3.5)
        ax.set_xlabel('Grid Size', labelpad=40)
        ax.grid(True)
        ax.set_xticks(X)
        ax.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=52)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax.set_ylabel('Localization Accuracy (%)', labelpad=20)
        ax.set_ylim([0, 102])
        method = Plot.LEGEND['povmloc-one']
        ax.set_title(f'Performance of {method}', pad=30, fontsize=65, fontweight='bold')
        fig.savefig(figname)


    @staticmethod
    def povmloc_vary_noise(data: list, figname: str):
        reduce = Plot.reduce_accuracy
        # step 1: prepare data
        table = defaultdict(list)
        for myinput, output_by_method in data:
            table[int(myinput.noise)].append({method: output.correct for method, output in output_by_method.items()})
        
        print_table = []
        methods = ['povmloc', 'povmloc-pro']
        for x, list_of_y_by_method in sorted(table.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Noise'] + methods))
        arr = np.array(print_table)
        X      = arr[:, 0]
        y_povmloc     = arr[:, 1] * 100  # percentage
        y_povmloc_pro = arr[:, 2] * 100

        # step 2: plotting
        fig, ax = plt.subplots(1, 1, figsize=(25, 18))
        fig.subplots_adjust(left=0.14, right=0.98, top=0.9, bottom=0.14)
        ax.plot(X, y_povmloc_pro, marker='^', label=Plot.LEGEND['povmloc-pro'], mfc='black', mec='b', color=Plot.COLOR['povmloc-pro'])
        ax.plot(X, y_povmloc,     marker='^', label=Plot.LEGEND['povmloc'],   mfc='black', mec='b', color=Plot.COLOR['povmloc'])
        fig.legend(ncol=1, loc='lower left', bbox_to_anchor=(0.14, 0.14), fontsize=55, handlelength=3.5)
        ax.set_xlabel('Noise (Std. of Shadowing)', labelpad=40)
        ax.grid(True)
        ax.set_xticks(X)
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.set_ylabel('Localization Accuracy (%)', labelpad=20)
        ax.set_ylim([87, 100.2])
        method1 = Plot.LEGEND['povmloc']
        ax.set_title(f'Performance of {method1} and Pro in 16x16 Grid', pad=30, fontsize=63, loc='right', fontweight='bold')
        fig.savefig(figname)


    @staticmethod
    def error_cdf(data: list, figname: str):
        table = defaultdict(list)
        for myinput, output_by_method in data:
            for method, output in output_by_method.items():
                table[method].append(output.localization_error)
                if output.localization_error > 50:
                    print(myinput)
        
        n_bins = 200
        method_n_bins = []
        for method, error_list in table.items():
            print(f'method={method}, avg. error = {np.average(error_list)}, error std. = {np.std(error_list)}')
            n, bins, _ = plt.hist(error_list, n_bins, density=True, histtype='step', cumulative=True, label=method)
            method_n_bins.append((method, n, bins))
        method_n_bins[0], method_n_bins[1] = method_n_bins[1], method_n_bins[0]  # switch ...
        plt.close()
        fig, ax = plt.subplots(figsize=(25, 18))
        fig.subplots_adjust(left=0.15, right=0.97, top=0.9, bottom=0.15)
        for method, n, bins in method_n_bins:
            ax.plot(bins[1:], n, label=Plot.LEGEND[method], color=Plot.COLOR[method])
        
        ax.grid(True)
        ax.legend(loc='lower right')
        ax.set_xlabel('Localization Error (m)', labelpad=40)
        ax.set_ylabel('Cumulative Distribution (CDF)', labelpad=40)
        ax.set_ylim([0, 1.003])
        ax.set_xlim([0, 30])
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.set_title('CDF of Localization Error in 16x16 Grid', pad=30, fontsize=63, fontweight='bold')
        fig.savefig(figname)
        

    @staticmethod
    def print_runtime(data: list):
        reduce = Plot.reduce_average
        methods = ['povmloc-one', 'povmloc', 'povmloc-pro']
        table = defaultdict(list)
        for myinput, output_by_method in data:
            # if myinput.sensor_num == 8:
            if myinput.sensor_num == 4:
                table[myinput.grid_length].append({method: output.elapse for method, output in output_by_method.items()})
        print_table = []
        for x, list_of_y_by_method in sorted(table.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + methods))


def povmloc_one_varygridsize():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/onelevel.4sen.varygrid', 'results/onelevel.8sen.varygrid']
    data = Utility.read_logs(logs)
    figname = 'results/onelevel-varygrid.png'
    Plot.povmloc_one_vary_gridsize(data, figname)


def povmloc_varynoise():
    '''evaluate the performance of povmloc and povmloc-pro against varying noise
    '''
    logs = ['results/twolevel.noise0', 'results/twolevel.noise1', 'results/twolevel.noise2', 'results/twolevel.noise3', 'results/twolevel.noise4']
    data = Utility.read_logs(logs)
    figname = 'results/twolevel-varynoise.png'
    Plot.povmloc_vary_noise(data, figname)


def localization_error_cdf():
    '''the classic error CDF plot
    '''
    logs = ['results/twolevel.errorcdf', 'results/onelevel.errorcdf']
    data = Utility.read_logs(logs)
    figname = 'results/error_cdf.png'
    Plot.error_cdf(data, figname)


def runtime():
    '''the runtime
    '''
    logs = ['results/runtime']
    data = Utility.read_logs(logs)
    Plot.print_runtime(data)



if __name__ == '__main__':

    povmloc_one_varygridsize()

    povmloc_varynoise()

    localization_error_cdf()

    runtime()


'''

POVM-Loc (one level)

  Grid Length         4         8
-------------  --------  --------
            2  1         1
            4  1         1
            6  0.861111  1
            8  0.5625    0.984375
           10  0.25      0.83
           12  0.236111  0.611111
           14  0.173469  0.433673
           16  0.117188  0.296875


POVM-Loc and POVM-Loc Pro

  Noise    povmloc    povmloc-pro
-------  ---------  -------------
      0   0.925781       0.996094
      1   0.925781       0.992188
      2   0.929688       0.996094
      3   0.921875       0.996094
      4   0.914062       0.992188


Runtime

Grid Length    povmloc-one    povmloc    povmloc-pro
-------------  -------------  ---------  -------------
            2        4.77333    nan            nan
            4        9.0775     nan            nan
            6       27.4        nan            nan
            8       53.06       nan            nan
           10       80.565      nan            nan
           12      113.365      nan            nan
           14      149.387      nan            nan
           16      193.818       10.256         11.252

Grid Length    povmloc-one    povmloc    povmloc-pro
-------------  -------------  ---------  -------------
            2         1.04          nan            nan
            4         1.0675        nan            nan
            6         1.222         nan            nan
            8         1.424         nan            nan
           10         1.626         nan            nan
           12         1.996         nan            nan
           14         2.314         nan            nan
           16         2.666         nan            nan

'''