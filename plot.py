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

    METHOD  = ['povmloc-one', 'povmloc',  'qml-r',   'qml-r-two',      'qml-c',   'qml-c-two']
    _LEGEND = ['QSD-One',     'QSD-Two',  'PQC-One', 'PQC-Two',        'PQC-One', 'PQC-Two']
    LEGEND  = dict(zip(METHOD, _LEGEND))

    _COLOR  = ['r',           'lightcoral', 'b',     'cornflowerblue', 'b',       'cornflowerblue']
    COLOR   = dict(zip(METHOD, _COLOR))

    _LINE   = ['-',           '--',       '-',        '--',        '-']
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
    def continuous_varygrid(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_average
        sensor_num = 8
        onelevel_methods = ['povmloc-one', 'qml-r']
        twolevel_methods = ['povmloc', 'qml-r-two']
        table_onelevel = defaultdict(list)
        table_twolevel = defaultdict(list)
        for myinput, output_by_method in data:
            if myinput.sensor_num != sensor_num:
                continue
            for method, output in output_by_method.items():
                if method in onelevel_methods:
                    table_onelevel[myinput.grid_length].append({output.method: output.localization_error})
                if method in twolevel_methods:
                    table_twolevel[myinput.grid_length].append({output.method: output.localization_error})
        
        print('\nOnelevel')
        print_table = []
        for x, list_of_y_by_method in sorted(table_onelevel.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in onelevel_methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + onelevel_methods))
        arr = np.array(print_table)
        povmloc_one = arr[:, 1]
        qml_r_one   = arr[:, 2]
        X_one       = arr[:, 0]

        print('\nTwolevel')
        print_table = []
        for x, list_of_y_by_method in sorted(table_twolevel.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in twolevel_methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + twolevel_methods))
        arr = np.array(print_table)
        povmloc   = arr[:, 1]
        qml_r_two = arr[:, 2]
        X_two     = arr[:, 0]

        # step 2: plotting
        l_err = "$L_{err}$"
        fig, ax1 = plt.subplots(1, 1, figsize=(18, 16))
        fig.subplots_adjust(left=0.15, right=0.98, top=0.91, bottom=0.12, wspace=0.13)
        ax1.plot(X_one, povmloc_one, linestyle=':', marker='o', label=Plot.LEGEND['povmloc-one'], mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X_two, povmloc,     linestyle='-', marker='o', label=Plot.LEGEND['povmloc'],     mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X_one, qml_r_one,   linestyle=':', marker='o', label=Plot.LEGEND['qml-r'],       mec='black', color=Plot.COLOR['qml-r'])
        ax1.plot(X_two, qml_r_two,   linestyle='-', marker='o', label=Plot.LEGEND['qml-r-two'],   mec='black', color=Plot.COLOR['qml-r'])
        # ax1
        ax1.legend(ncol=1, handlelength=4, loc='upper left')
        ax1.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax1.grid(True)
        X = list(X_one)
        X.remove(9)
        ax1.set_xticks(X)
        ax1.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=38, rotation=10)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax1.set_ylabel(f'{l_err} (m)')
        # ax1.set_ylim([0, 40])
        ax1.set_title(f'Performance of Localization Algorithms', pad=30, fontsize=45, fontweight='bold')
        fig.savefig(figname)


    @staticmethod
    def continuous_varysensornum(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_average
        grid_length = 16
        table = defaultdict(list)
        for myinput, output_by_method in data:
            if myinput.grid_length != grid_length:
                continue
            for method, output in output_by_method.items():
                table[myinput.sensor_num].append({method: output.localization_error})
        
        print('\nVarying Sensor #')
        print_table = []
        methods = ['povmloc-one', 'povmloc', 'qml-r', 'qml-r-two']
        for x, list_of_y_by_method in sorted(table.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Sensor Number'] + methods))
        arr = np.array(print_table)
        povmloc_one = arr[:, 1]
        povmloc_two = arr[:, 2]
        qml_r_one   = arr[:, 3]
        qml_r_two   = arr[:, 4]
        X_one       = arr[:, 0]

        # return

        # step 2: plotting
        l_err = "$L_{err}$"
        fig, ax1 = plt.subplots(1, 1, figsize=(18, 16))
        fig.subplots_adjust(left=0.14, right=0.98, top=0.91, bottom=0.11, wspace=0.13)
        ind = np.arange(len(X_one))
        width = 0.15
        pos1 = ind - 1.5*width
        pos2 = ind - 0.5*width
        pos3 = ind + 0.5*width
        pos4 = ind + 1.5*width
        ax1.bar(pos1, povmloc_one, width=width, edgecolor='black', label=Plot.LEGEND['povmloc-one'], color=Plot.COLOR['povmloc-one'])
        ax1.bar(pos2, povmloc_two, width=width, edgecolor='black', label=Plot.LEGEND['povmloc'],     color=Plot.COLOR['povmloc'])
        ax1.bar(pos3, qml_r_one,   width=width, edgecolor='black', label=Plot.LEGEND['qml-r'],       color=Plot.COLOR['qml-r'])
        ax1.bar(pos4, qml_r_two,   width=width, edgecolor='black', label=Plot.LEGEND['qml-r-two'],   color=Plot.COLOR['qml-r-two'])
        ax1.grid(True)
        ax1.legend(ncol=1, handlelength=4, loc='upper right', fontsize=40)
        ax1.set_xlabel('Sensor Number', labelpad=10, fontsize=40)
        X = list(X_one)
        ax1.set_xticks(ind)
        ax1.set_xticklabels([f'{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, length=10, width=5)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax1.set_ylabel(f'{l_err} (m)', labelpad=20)
        ax1.set_title(f'Localization Performance in a 16x16 Grid', pad=30, fontsize=45, fontweight='bold')
        fig.savefig(figname)


    @staticmethod
    def discrete_varysensornum(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_average
        grid_length = 16
        table = defaultdict(list)
        for myinput, output_by_method in data:
            if myinput.grid_length != grid_length:
                continue
            for method, output in output_by_method.items():
                table[myinput.sensor_num].append({method: output.correct})
        
        print('\nVarying Sensor #')
        print_table = []
        methods = ['povmloc-one', 'povmloc', 'qml-c', 'qml-c-two']
        for x, list_of_y_by_method in sorted(table.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Sensor Number'] + methods))
        arr = np.array(print_table)
        povmloc_one = arr[:, 1] * 100
        povmloc_two = arr[:, 2] * 100
        qml_r_one   = arr[:, 3] * 100
        qml_r_two   = arr[:, 4] * 100
        X_one       = arr[:, 0]

        # step 2: plotting
        fig, ax1 = plt.subplots(1, 1, figsize=(18, 18))
        fig.subplots_adjust(left=0.14, right=0.98, top=0.8, bottom=0.11, wspace=0.13)
        ind = np.arange(len(X_one))
        width = 0.15
        pos1 = ind - 1.5*width
        pos2 = ind - 0.5*width
        pos3 = ind + 0.5*width
        pos4 = ind + 1.5*width
        ax1.bar(pos1, povmloc_one, width=width, edgecolor='black', label=Plot.LEGEND['povmloc-one'], color=Plot.COLOR['povmloc-one'])
        ax1.bar(pos2, povmloc_two, width=width, edgecolor='black', label=Plot.LEGEND['povmloc'],     color=Plot.COLOR['povmloc'])
        ax1.bar(pos3, qml_r_one,   width=width, edgecolor='black', label=Plot.LEGEND['qml-c'],       color=Plot.COLOR['qml-c'])
        ax1.bar(pos4, qml_r_two,   width=width, edgecolor='black', label=Plot.LEGEND['qml-c-two'],   color=Plot.COLOR['qml-c-two'])
        ax1.grid(True)
        ax1.legend(ncol=2, handlelength=4, loc='upper center', fontsize=40, bbox_to_anchor=(0.5, 1.28))
        ax1.set_xlabel('Sensor Number', labelpad=10, fontsize=40)
        X = list(X_one)
        ax1.set_xticks(ind)
        ax1.set_xticklabels([f'{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, length=10, width=5)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        CC_acc = "$CC_{acc}$"
        ax1.set_ylim([0, 100])
        ax1.set_ylabel(f'{CC_acc} (%)', labelpad=10)
        ax1.set_title(f'Localization Performance in a 16x16 Grid', pad=30, fontsize=45, fontweight='bold')
        fig.savefig(figname)


    @staticmethod
    def error_cdf(data: list, figname: str):
        # fix grid length at 16 and sensor number at 8
        grid_length = 16
        sensor_num = 8
        table = defaultdict(list)
        for myinput, output_by_method in data:
            if myinput.grid_length != grid_length or myinput.sensor_num != sensor_num:
                continue
            for method, output in output_by_method.items():
                if output.localization_error > 90:
                    print(myinput, '\n', output, '\n')
                    continue
                table[method].append(output.localization_error)

        n_bins = 200
        method_n_bins = []
        for method, error_list in table.items():
            print(f'method={method}, avg. error = {np.average(error_list)}, error std. = {np.std(error_list)}')
            Y, bins, _ = plt.hist(error_list, n_bins, density=True, histtype='step', cumulative=True, label=method)
            method_n_bins.append((method, Y, bins))
        plt.close()
        fig, ax = plt.subplots(figsize=(18, 16))
        fig.subplots_adjust(left=0.15, right=0.96, top=0.9, bottom=0.12)
        for method, Y, bins in method_n_bins:
            ax.plot(bins[1:], Y, label=Plot.LEGEND[method], color=Plot.COLOR[method], linestyle=Plot.LINE[method])
        
        ax.grid(True)
        X = list(range(0, 41, 5))
        ax.set_xticks(X)
        ax.set_xticklabels([f'{int(x)}' for x in X])
        ax.legend(loc='lower right', fontsize=40)
        ax.set_xlabel('$L_{err}$ (m)', labelpad=20)
        ax.set_ylabel('Percentage (%)', labelpad=20)
        Y = np.linspace(0, 1, 6)
        ax.set_yticks(Y)
        ax.set_yticklabels([int(y*100) for y in Y])
        ax.set_ylim([0, 1.003])
        ax.set_xlim([0, 40])
        ax.tick_params(axis='x', pad=15, direction='in', length=10, width=5)
        ax.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        ax.set_title('Cumulative Distribution Function of $L_{err}$', pad=30, fontsize=45, fontweight='bold')
        fig.savefig(figname)
        

    @staticmethod
    def discrete_varygrid(data: list, figname: str):
        # step 1.1: prepare accuracy data for QSD-One and PQC-One
        reduce = Plot.reduce_average
        sensor_num = 8
        onelevel_methods = ['povmloc-one', 'qml-c']
        twolevel_methods = ['povmloc', 'qml-c-two']
        table_onelevel = defaultdict(list)
        table_twolevel = defaultdict(list)
        for myinput, output_by_method in data:
            if myinput.sensor_num != sensor_num:
                continue
            for method, output in output_by_method.items():
                if method in onelevel_methods:
                    table_onelevel[myinput.grid_length].append({output.method: output.correct})
                if method in twolevel_methods:
                    table_twolevel[myinput.grid_length].append({output.method: output.correct})
        
        print('\nOnelevel')
        print_table = []
        for x, list_of_y_by_method in sorted(table_onelevel.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in onelevel_methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + onelevel_methods))
        arr = np.array(print_table)
        povmloc_one = arr[:, 1]
        qml_c_one   = arr[:, 2]
        X_one       = arr[:, 0]

        print('\nTwolevel')
        print_table = []
        for x, list_of_y_by_method in sorted(table_twolevel.items()):
            tmp_list = [reduce([(y_by_method[method] if method in y_by_method else None) for y_by_method in list_of_y_by_method]) for method in twolevel_methods]
            print_table.append([x] + tmp_list)
        print(tabulate.tabulate(print_table, headers=['Grid Length'] + twolevel_methods))
        arr = np.array(print_table)
        povmloc   = arr[:, 1]
        qml_c_two = arr[:, 2]
        X_two     = arr[:, 0]


        # step 2: plotting
        fig, ax1 = plt.subplots(1, 1, figsize=(18, 16))
        fig.subplots_adjust(left=0.15, right=0.98, top=0.91, bottom=0.12, wspace=0.13)
        ax1.plot(X_one, povmloc_one, linestyle=':', marker='o', label=Plot.LEGEND['povmloc-one'], mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X_two, povmloc,     linestyle='-', marker='o', label=Plot.LEGEND['povmloc'],     mec='black', color=Plot.COLOR['povmloc-one'])
        ax1.plot(X_one, qml_c_one,   linestyle=':', marker='o', label=Plot.LEGEND['qml-c'],       mec='black', color=Plot.COLOR['qml-c'])
        ax1.plot(X_two, qml_c_two,   linestyle='-', marker='o', label=Plot.LEGEND['qml-c-two'],   mec='black', color=Plot.COLOR['qml-c'])
        # ax1
        ax1.legend(ncol=1, handlelength=4, loc='lower left')
        ax1.set_xlabel('Grid Size', labelpad=10, fontsize=40)
        ax1.grid(True)
        X = list(X_one)
        X.remove(9)
        ax1.set_xticks(X)
        ax1.set_xticklabels([f'{int(x)}x{int(x)}' for x in X])
        ax1.tick_params(axis='x', pad=15, direction='in', length=10, width=5, labelsize=38, rotation=10)
        ax1.tick_params(axis='y', pad=15, direction='in', length=10, width=5)
        CC_acc = "$CC_{acc}$"
        ax1.set_ylabel(f'{CC_acc} (%)')
        # ax1.set_ylim([0, 40])
        ax1.set_title(f'Performance of Localization Algorithms', pad=30, fontsize=45, fontweight='bold')
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
    logs = ['results/discrete.onelevel.qsd', 'results/discrete.onelevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/discrete.onelevel.varygrid.png'
    Plot.discrete_onelevel_varygrid(data, figname)


def continuous_onelevel_varygrid():
    '''evaluate the performance of the single level POVM-Loc One
    '''
    logs = ['results/continuous.onelevel.qsd', 'results/continuous.onelevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/continuous.onelevel.varygrid.png'
    Plot.continuous_onelevel_varygrid(data, figname)


def continuous_varygrid():
    logs = ['results/continuous.onelevel.qsd', 'results/continuous.onelevel.pqc',\
            'results/continuous.twolevel.qsd', 'results/continuous.twolevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/continuous.varygrid.png'
    Plot.continuous_varygrid(data, figname)


def continuous_varysensornum():
    logs = ['results/continuous.onelevel.qsd', 'results/continuous.onelevel.pqc',\
            'results/continuous.twolevel.qsd', 'results/continuous.twolevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/continuous.varysensornum.png'
    Plot.continuous_varysensornum(data, figname)


def discrete_varysensornum():
    logs = ['results/discrete.onelevel.qsd', 'results/discrete.onelevel.pqc',\
            'results/discrete.twolevel.qsd', 'results/discrete.twolevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/discrete.varysensornum.png'
    Plot.discrete_varysensornum(data, figname)


def localization_error_cdf():
    '''the classic error CDF plot
    '''
    logs = ['results/continuous.onelevel.qsd', 'results/continuous.onelevel.pqc',\
            'results/continuous.twolevel.qsd', 'results/continuous.twolevel.pqc']
    data = Utility.read_logs(logs)
    figname = f'results/error_cdf.png'
    Plot.error_cdf(data, figname)


def discrete_varygrid():
    logs = ['results/discrete.onelevel.qsd', 'results/discrete.onelevel.pqc',\
            'results/discrete.twolevel.qsd', 'results/discrete.twolevel.pqc']
    data = Utility.read_logs(logs)
    figname = 'results/discrete.varygrid.png'
    Plot.discrete_varygrid(data, figname)


def runtime():
    '''the runtime
    '''
    logs = ['results/runtime']
    data = Utility.read_logs(logs)
    Plot.print_runtime(data)



if __name__ == '__main__':

    # obsolete
    # discrete_onelevel_varygrid()
    # continuous_onelevel_varygrid()

    # continuous_varygrid()
    # continuous_varysensornum()
    # localization_error_cdf()

    discrete_varygrid()
    discrete_varysensornum()


    # runtime()


'''

Plot 1 -- continuous, fix sensors (8), all four methods, vary grid 

Onelevel
  Grid Length    povmloc-one     qml-r
-------------  -------------  --------
            2        6.89975  0.864072
            4        4.08887  1.6246
            6        3.78698  2.55323
            8        4.36634  3.57102
            9        5.97415  3.71973
           10        5.67271  5.1482
           12        9.14297  5.72974
           14       12.279    8.55924
           16       18.3714   8.52706

Twolevel
  Grid Length    povmloc    qml-r-two
-------------  ---------  -----------
            4   12.173        1.26742
            9   12.8727       3.03796
           12    9.39258      3.02974
           16    9.67841      4.86637


           
Plot 2 -- continuous, fix grid size (16x16), all four methods, vary sensor




Plot 4 -- discrete, sensor=8, vary grid length, all four methods

Onelevel
  Grid Length    povmloc-one     qml-c
-------------  -------------  --------
            2       1         1
            4       1         1
            6       1         1
            8       0.9375    1
            9       0.790123  1
           10       0.68      1
           12       0.451389  0.993056
           14       0.244898  0.928571
           16       0.12549   0.800781

Twolevel
  Grid Length    povmloc    qml-c-two
-------------  ---------  -----------
            4   0.5625       1
            9   0.654321     0.604938
           12   0.847222     0.805556
           16   0.765625     0.808594



Plot 5 -- discrete, grid length = 16, vary sensor, all four methods

Sensor Number    povmloc-one     povmloc     qml-c    qml-c-two
---------------  -------------  ----------  --------  -----------
              4       0.078125    0.582031  0.523438     0.648438
              8       0.12549     0.765625  0.800781     0.808594
             16     nan         nan         0.949219     0.789062


'''







'''

discrete onelevel

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

continuous one level
           
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