from collections import defaultdict
from distutils.log import error
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tabulate
from utility import Utility


class Plot:

    plt.rcParams['font.size'] = 45
    plt.rcParams['lines.linewidth'] = 10
    plt.rcParams['lines.markersize'] = 20
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'

    METHOD  = ['povmloc-one',  'povmloc',  'qml',       'qml-r']
    _LEGEND = ['QSD-One',      'TwoLevel', 'PQC-One-C', 'PQC-One-R']
    LEGEND  = dict(zip(METHOD, _LEGEND))

    _COLOR  = ['r',            'r',        'b',         'deepskyblue']
    COLOR   = dict(zip(METHOD, _COLOR))

    _LINE   = ['-',           '--',       '-']
    LINE    = dict(zip(METHOD, _LINE))


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
    def discrete_onelevel_varygrid(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_accuracy
        table_qsd_onelevel = defaultdict(list)
        table_pqc_onelevel = defaultdict(list)
        for myinput, output_by_method in data:
            for method, output in output_by_method.items():
                if method == 'povmloc-one':
                    table_qsd_onelevel[myinput.grid_length].append({myinput.sensor_num: output.correct})
                if method == 'qml':
                    table_pqc_onelevel[myinput.grid_length].append({myinput.sensor_num: output.correct})
        
        print('\nQSD-Onelevel')
        print_table = []
        sensornum = [4, 8]
        for x, list_of_y_by_sensornum in sorted(table_qsd_onelevel.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        povm_one_4sen = arr[:, 1] * 100  # percentage
        povm_one_8sen = arr[:, 2] * 100

        print('PQC-Onelevel-C')
        print_table = []
        sensornum = [4, 8, 16]
        for x, list_of_y_by_sensornum in sorted(table_pqc_onelevel.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        pqc_one_4sen  = arr[:, 1]  * 100
        pqc_one_8sen  = arr[:, 2]  * 100
        pqc_one_16sen = arr[:, 3] * 100
        X      = arr[:, 0]

        # step 2: plotting
        cc_acc = "$CC_{acc}$"
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, 14))
        fig.subplots_adjust(left=0.085, right=0.99, top=0.91, bottom=0.18, wspace=0.13)
        ax1.plot(X, povm_one_8sen, linestyle='--', marker='o', label="8 Sensors", mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X, povm_one_4sen, linestyle=':',  marker='o', label="4 Sensors", mec='black', color=Plot.COLOR['povmloc-one'])
        ax2.plot(X, pqc_one_16sen, linestyle='-',  marker='o', label="16 Sensors",  mec='black', color=Plot.COLOR['qml'])
        ax2.plot(X, pqc_one_8sen,  linestyle='--', marker='o', label="8 Sensors",  mec='black', color=Plot.COLOR['qml'])
        ax2.plot(X, pqc_one_4sen,  linestyle=':',  marker='o', label="4 Sensors",  mec='black', color=Plot.COLOR['qml'])
        # ax1
        ax1.legend(ncol=1, handlelength=4, loc='lower left')
        ax1.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax1.grid(True)
        ax1.set_xticks(X)
        ax1.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=35, rotation=14)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax1.set_ylabel(f'{cc_acc} (%)')
        ax1.set_ylim([0, 102])
        method = Plot.LEGEND['povmloc-one']
        ax1.set_title(f'Performance of {method}', pad=30, fontsize=45, fontweight='bold')
        # ax2
        ax2.legend(ncol=1, handlelength=4, loc='lower left')
        ax2.grid(True)
        ax2.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax2.set_xticks(X)
        ax2.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax2.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=35, rotation=14)
        ax2.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax2.set_ylim([0, 102])
        method = Plot.LEGEND['qml']
        ax2.set_title(f'Performance of {method}', pad=30, fontsize=45, fontweight='bold')
        plt.figtext(0.275, 0.01, '(a)', fontsize=40)
        plt.figtext(0.76,  0.01, '(b)', fontsize=40)
        fig.savefig(figname)


    @staticmethod
    def continuous_onelevel_varygrid(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_average
        table_qsd_onelevel = defaultdict(list)
        table_pqc_onelevel = defaultdict(list)
        for myinput, output_by_method in data:
            for method, output in output_by_method.items():
                if method == 'povmloc-one':
                    table_qsd_onelevel[myinput.grid_length].append({myinput.sensor_num: output.localization_error})
                if method == 'qml-r':
                    table_pqc_onelevel[myinput.grid_length].append({myinput.sensor_num: output.localization_error})
        
        print('\nQSD-Onelevel')
        print_table = []
        sensornum = [4, 8]
        for x, list_of_y_by_sensornum in sorted(table_qsd_onelevel.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        povm_one_4sen = arr[:, 1]
        povm_one_8sen = arr[:, 2]

        print('PQC-Onelevel-R')
        print_table = []
        sensornum = [4, 8, 16]
        for x, list_of_y_by_sensornum in sorted(table_pqc_onelevel.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        pqc_one_r_4sen  = arr[:, 1]
        pqc_one_r_8sen  = arr[:, 2]
        pqc_one_r_16sen = arr[:, 3]
        X               = arr[:, 0]

        # step 2: plotting
        l_err = "$L_{err}$"
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, 14))
        fig.subplots_adjust(left=0.085, right=0.99, top=0.91, bottom=0.18, wspace=0.13)
        ax1.plot(X, povm_one_4sen, linestyle=':',  marker='o', label="4 Sensors", mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X, povm_one_8sen, linestyle='--', marker='o', label="8 Sensors", mec='black', color=Plot.COLOR['povmloc-one'])
        ax2.plot(X, pqc_one_r_4sen,  linestyle=':',  marker='o', label="4 Sensors",   mec='black', color=Plot.COLOR['qml-r'])
        ax2.plot(X, pqc_one_r_8sen,  linestyle='--', marker='o', label="8 Sensors",   mec='black', color=Plot.COLOR['qml-r'])
        ax2.plot(X, pqc_one_r_16sen, linestyle='-',  marker='o', label="16 Sensors",  mec='black', color=Plot.COLOR['qml-r'])
        # ax1
        ax1.legend(ncol=1, handlelength=4, loc='upper left')
        ax1.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax1.grid(True)
        ax1.set_xticks(X)
        ax1.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=35, rotation=14)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax1.set_ylabel(f'{l_err} (m)')
        ax1.set_ylim([0, 40])
        method = Plot.LEGEND['povmloc-one']
        ax1.set_title(f'Performance of {method}', pad=30, fontsize=45, fontweight='bold')
        # ax2
        ax2.legend(ncol=1, handlelength=4, loc='upper left')
        ax2.grid(True)
        ax2.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax2.set_xticks(X)
        ax2.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax2.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=35, rotation=14)
        ax2.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax2.set_ylim([0, 40])
        method = Plot.LEGEND['qml-r']
        ax2.set_title(f'Performance of {method}', pad=30, fontsize=45, fontweight='bold')
        plt.figtext(0.275, 0.01, '(a)', fontsize=40)
        plt.figtext(0.76,  0.01, '(b)', fontsize=40)
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
            Y, bins, _ = plt.hist(error_list, n_bins, density=True, histtype='step', cumulative=True, label=method)
            method_n_bins.append((method, Y, bins))
        method_n_bins[0], method_n_bins[1] = method_n_bins[1], method_n_bins[0]  # switch ...
        plt.close()
        fig, ax = plt.subplots(figsize=(25, 18))
        fig.subplots_adjust(left=0.15, right=0.97, top=0.9, bottom=0.15)
        for method, Y, bins in method_n_bins:
            ax.plot(bins[1:], Y, label=Plot.LEGEND[method], color=Plot.COLOR[method], linestyle=Plot.LINE[method])
        
        ax.grid(True)
        ax.legend(loc='lower right')
        ax.set_xlabel('$L_{err}$ (m)', labelpad=40)
        ax.set_ylabel('Percentage (%)', labelpad=40)
        Y = np.linspace(0, 1, 6)
        ax.set_yticks(Y)
        ax.set_yticklabels([int(y*100) for y in Y])
        ax.set_ylim([0, 1.003])
        ax.set_xlim([0, 30])
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax.set_title('CDF of $L_{err}$', pad=30, fontsize=63, fontweight='bold')
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


def discrete_onelevel_varygrid():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/discrete.onelevel.varygrid.qsd', 'results/discrete.onelevel.varygrid.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/discrete.onelevel.varygrid.png'
    Plot.discrete_onelevel_varygrid(data, figname)


def continuous_onelevel_varygrid():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/continuous.onelevel.varygrid.qsd', 'results/continuous.onelevel.varygrid.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/continuous.onelevel.varygrid.png'
    Plot.continuous_onelevel_varygrid(data, figname)


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

    # discrete_onelevel_varygrid()

    continuous_onelevel_varygrid()

    # povmloc_varynoise()

    # localization_error_cdf()

    # runtime()


'''

Plot 1 -- discrete onelevel

QSD-Onelevel
  Grid Length          4         8
-------------  ---------  --------
            2  1          1
            4  1          1
            6  0.888889   1
            8  0.578125   0.9375
           10  0.33       0.68
           12  0.166667   0.451389
           14  0.0867347  0.244898
           16  0.078125   0.12549
PQC-Onelevel-C
  Grid Length         4         8        16
-------------  --------  --------  --------
            2  1         1         1
            4  1         1         1
            6  0.944444  1         1
            8  0.890625  1         1
           10  0.82      1         1
           12  0.75      0.993056  1
           14  0.607143  0.928571  1
           16  0.523438  0.800781  0.949219


Plot 2 -- continuous one level
           
QSD-Onelevel
  Grid Length         4         8
-------------  --------  --------
            2   4.48754   6.89975
            4   3.92177   4.08887
            6   5.52066   3.78698
            8   8.71404   4.36634
           10  12.6864    5.67271
           12  19.818     9.14297
           14  30.9472   12.279
           16  35.5007   18.3714
PQC-Onelevel-R
  Grid Length         4         8       16
-------------  --------  --------  -------
            2   1.28724  0.864072  0.64478
            4   3.60149  1.6246    1.0055
            6   7.43288  2.55323   1.7387
            8  12.5013   3.57102   2.15625
           10  15.5509   5.1482    3.00706
           12  20.6928   5.72974   4.06911
           14  24.6972   8.55924   5.05789
           16  28.8596   8.52706   6.25085

'''