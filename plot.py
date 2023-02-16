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
    plt.rcParams['lines.markersize'] = 30
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'

    METHOD  = ['povmloc-one', 'povmloc',  'povmloc-pro']
    _LEGEND = ['OneLevel',    'TwoLevel', 'TwoLevel-Pro']
    LEGEND  = dict(zip(METHOD, _LEGEND))

    _COLOR  = ['b',  'r',        'r']
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
    def povmloc_one_vary_gridsize(data: list, figname: str):
        # step 1.1: prepare accuracy data
        reduce = Plot.reduce_accuracy
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

        # step 1.2: prepare error data
        reduce = Plot.reduce_average
        table = defaultdict(list)
        for myinput, output_by_method in data:
            table[myinput.grid_length].append({myinput.sensor_num: output.localization_error for output in output_by_method.values()})
        
        print_table = []
        sensornum = [4, 8]
        for x, list_of_y_by_sensornum in sorted(table.items()):
            tmp_list = [reduce([(y_by_sensornum[sensor] if sensor in y_by_sensornum else None) for y_by_sensornum in list_of_y_by_sensornum]) for sensor in sensornum]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + sensornum))
        arr = np.array(print_table)
        X      = arr[:, 0]
        y_4sen_error = arr[:, 1]     # error
        y_8sen_error = arr[:, 2]

        # step 2: plotting
        cc_acc = "$CC_{acc}$"
        l_err  = "$L_{err}$"
        povmloc_one_color2 = 'black'
        fig, ax1 = plt.subplots(1, 1, figsize=(23, 22))
        fig.subplots_adjust(left=0.13, right=0.895, top=0.81, bottom=0.16)
        ax2 = ax1.twinx()
        ax1.plot(X, y_8sen,       linestyle='-',  marker='^', label=f"{cc_acc} 8 Sensors", mfc='black',                   mec='b', color=povmloc_one_color2)
        ax1.plot(X, y_4sen,       linestyle='--', marker='^', label=f"{cc_acc} 4 Sensors", mfc='black',                   mec='b', color=povmloc_one_color2)
        # ax2.plot(X, y_8sen_error, linestyle='-',  marker='o', label=f"{l_err} 8 Sensors",  mfc=Plot.COLOR['povmloc-one'], mec='b', color=Plot.COLOR['povmloc-one'])
        # ax2.plot(X, y_4sen_error, linestyle='--', marker='o', label=f"{l_err} 4 Sensors",  mfc=Plot.COLOR['povmloc-one'], mec='b', color=Plot.COLOR['povmloc-one'])
        # ax1
        fig.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1), fontsize=52, handlelength=3.5)
        ax1.set_xlabel('Grid Size', labelpad=20)
        ax1.grid(True)
        ax1.set_xticks(X)
        ax1.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=50, rotation=12)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelcolor=povmloc_one_color2)
        ax1.set_ylabel(f'{cc_acc} (%)', fontsize=55, color=povmloc_one_color2)
        ax1.set_ylim([0, 102])
        method = Plot.LEGEND['povmloc-one']
        ax1.set_title(f'Performance of {method}', pad=30, fontsize=60, fontweight='bold')
        # ax2
        ax2.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelcolor=Plot.COLOR['povmloc-one'])
        ax2.set_ylabel(f'{l_err} (m)', labelpad=10, fontsize=55, color=Plot.COLOR['povmloc-one'])
        ax2.set_ylim([0, 20.4])
        ax2.set_yticks(range(0, 21, 4))
        plt.figtext(0.485, 0.01, '(a)')
        fig.savefig(figname)


    @staticmethod
    def povmloc_vary_noise(data: list, figname: str):
        # step 1.1: prepare accuracy
        reduce = Plot.reduce_accuracy
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
        X             = arr[:, 0]
        y_povmloc     = arr[:, 1] * 100  # percentage
        y_povmloc_pro = arr[:, 2] * 100

        # step 1.2: prepare localization error
        reduce = Plot.reduce_average
        table = defaultdict(list)
        for myinput, output_by_method in data:
            table[int(myinput.noise)].append({method: output.localization_error for method, output in output_by_method.items()})
        
        print_table = []
        methods = ['povmloc', 'povmloc-pro']
        for x, list_of_y_by_method in sorted(table.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Noise'] + methods))
        arr = np.array(print_table)
        X                   = arr[:, 0]
        y_povmloc_error     = arr[:, 1]  # error
        y_povmloc_pro_error = arr[:, 2]
        
        # step 2: plotting
        povmloc_one_color2 = 'black'
        fig, ax1 = plt.subplots(1, 1, figsize=(23, 22))
        fig.subplots_adjust(left=0.13, right=0.88, top=0.81, bottom=0.16)
        ax2 = ax1.twinx()
        cc_acc = "$CC_{acc}$"
        l_err  = "$L_{err}$"
        ourpro_label = Plot.LEGEND['povmloc-pro']
        our_label    = Plot.LEGEND['povmloc']
        ax1.plot(X, y_povmloc_pro,       linestyle=Plot.LINE['povmloc-pro'],  marker='^', label=f"{cc_acc} {ourpro_label}", mfc='black',                   mec='b', color=povmloc_one_color2)
        ax1.plot(X, y_povmloc,           linestyle=Plot.LINE['povmloc'],      marker='^', label=f"{cc_acc} {our_label}",    mfc='black',                   mec='b', color=povmloc_one_color2)
        ax2.plot(X, y_povmloc_pro_error, linestyle=Plot.LINE['povmloc-pro'],  marker='o', label=f"{l_err} {ourpro_label}",  mfc=Plot.COLOR['povmloc-pro'], mec='b', color=Plot.COLOR['povmloc-pro'])
        ax2.plot(X, y_povmloc_error,     linestyle=Plot.LINE['povmloc'],      marker='o', label=f"{l_err} {our_label}",     mfc=Plot.COLOR['povmloc-pro'], mec='b', color=Plot.COLOR['povmloc'])
        fig.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1), fontsize=52, handlelength=3.5)
        # ax1
        ax1.grid(True)
        ax1.set_xlabel('Noise', labelpad=50)
        ax1.set_xticks(X)
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelsize=60)
        ax1.set_ylabel(f'{cc_acc} (%)', fontsize=55)
        ax1.set_ylim([90, 100.2])
        ax1.set_title(f'Performance of TwoLevel, TwoLevel-Pro', pad=30, fontsize=60, fontweight='bold')
        # ax2
        ax2.tick_params(axis='y', pad=15, direction='in', length=10, width=5, labelcolor=Plot.COLOR['povmloc'])
        ax2.set_ylabel(f'{l_err} (m)', labelpad=10, fontsize=55, color=Plot.COLOR['povmloc'])
        ax2.set_ylim([0, 1.2])
        ax2.set_yticks(np.linspace(0, 1.2, 4))
        plt.figtext(0.475, 0.01, '(b)')
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


def povmloc_one_varygridsize():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    # logs = ['results/onelevel.4sen.varygrid', 'results/onelevel.8sen.varygrid']
    logs = ['results/onelevel.varygrid']
    data = Utility.read_logs(logs)
    # figname = 'results/onelevel-varygrid.2.png'
    figname = 'results2/onelevel-varygrid.2.png'
    Plot.povmloc_one_vary_gridsize(data, figname)


def povmloc_varynoise():
    '''evaluate the performance of povmloc and povmloc-pro against varying noise
    '''
    # logs = ['results/twolevel.noise0', 'results/twolevel.noise1', 'results/twolevel.noise2', 'results/twolevel.noise3', 'results/twolevel.noise4']
    logs = ['results/twolevel.noise']
    data = Utility.read_logs(logs)
    figname = 'results/twolevel-varynoise.2.png'
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

    # povmloc_varynoise()

    # localization_error_cdf()

    # runtime()


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