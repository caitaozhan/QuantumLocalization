'''a runner
'''

from subprocess import Popen, PIPE
import sys


def plot1():
    # plot 1: Discrete case. Methods: QSD-One and PQC-One-C. 
    #         Y: CC_accuracy, X: varying grid size
    
                                  # length, size, noise, continuous
    template = 'python main.py -m {} -l {} -s {} -of {}'
    # povmloc-one
    # config = [
        # ['povmloc-one', 2,  4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 4,  4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 6,  4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 8,  4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 10, 4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 12, 4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 14, 4, 'discrete.onelevel.varygrid'],
        # ['povmloc-one', 16, 8, 'discrete.onelevel.varygrid.8sen']
    # ]
    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()

    
    # qml

    template = 'python main.py -m {} -l {} -s {} -of {} -rd {}'
    config = [
        ['qml', 2,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 4,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 6,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 8,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 10, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 12, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 14, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        ['qml', 16, 16, 'discrete.onelevel.varygrid.qml.16sen']
    ]

    for i, c in enumerate(config):
        rood_dir = f'qml-data/{c[1]}x{c[1]}.{c[2]}'
        command = template.format(c[0], c[1], c[2], c[3], rood_dir)
        print(command)
        sys.stdout.flush()
        p = Popen(command, shell=True)
        p.wait()


def plot2():
    # plot 2: Continuous case. Methods: QSD-One and PQC-One-R. 
    #         Y: CC_accuracy,  X: varying grid size
    
                               # length, size, noise, continuous
    template = 'python main.py -m {} -l {} -s {} -of {} -c'
    # povmloc-one
    config = [
        # ['povmloc-one', 2,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 4,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 6,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 8,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 10, 8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 12, 8, 'continuous.onelevel.varygrid.8sen.2'],
        # ['povmloc-one', 14, 8, 'continuous.onelevel.varygrid.8sen.2'],
        ['povmloc-one', 16, 8, 'continuous.onelevel.varygrid.8sen.1']
    ]
    for i, c in enumerate(config):
        command = template.format(c[0], c[1], c[2], c[3])
        print(command)
        p = Popen(command, shell=True)
        p.wait()

    
    # qml

    # template = 'python main.py -m {} -l {} -s {} -of {} -rd {}'
    # config = [
    #     ['qml', 2,  16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 4,  16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 6,  16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 8,  16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 10, 16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 12, 16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 14, 16, 'discrete.onelevel.varygrid.qml.16sen'],
    #     ['qml', 16, 16, 'discrete.onelevel.varygrid.qml.16sen']
    # ]

    # for i, c in enumerate(config):
    #     rood_dir = f'qml-data/{c[1]}x{c[1]}.{c[2]}'
    #     command = template.format(c[0], c[1], c[2], c[3], rood_dir)
    #     print(command)
    #     sys.stdout.flush()
    #     p = Popen(command, shell=True)
    #     p.wait()




def plot3():
    # plot 3: POVMLoc (one level), POVMLoc and POVMLoc-Pro. The localization error CDF plot. Y: percentage, X: error
    
    template = 'python main.py -m {} {} -l {} -n {} -of {} -c'
    config = [
       ['povmloc', 'povmloc-pro', 16, 1, 'twolevel.errorcdf'],
    ]

    # template = 'python main.py -m {} -l {} -s {} -n {} -of {} -c'
    # config = [
    #     ['povmloc-one', 16, 8,  1, 'onelevel.errorcdf'],
    # ]

    for i, c in enumerate(config):
        command = template.format(c[0], c[1], c[2], c[3], c[4])
        print(command)
        p = Popen(command, shell=True)
        p.wait()


def table():
    '''a table for run time. the experiment data for plots 1,2,3 are collected on different machines
       to collect runtime, need to run experiments on the same machine
    '''
    # template = 'python main.py -m {} {} {} -l {} -s {} -n {} -of {}'
    # config = [
    #    ['povmloc', 'povmloc-pro', 'povmloc-one', 16, 8, 1, 'runtime'],
    # ]

    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3], c[4], c[5], c[6])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()

    template = 'python main.py -m {} -l {} -s {} -n {} -of {}'
    config = [
    #    ['povmloc-one', 2, 4, 1, 'runtime'],
    #    ['povmloc-one', 4, 4, 1, 'runtime'],
    #    ['povmloc-one', 6, 4, 1, 'runtime'],
    #    ['povmloc-one', 8, 4, 1, 'runtime'],
    #    ['povmloc-one', 10, 4, 1, 'runtime'],
    #    ['povmloc-one', 12, 4, 1, 'runtime'],
    #    ['povmloc-one', 14, 4, 1, 'runtime'],
    #    ['povmloc-one', 16, 4, 1, 'runtime'],
    #    ['povmloc-one', 2, 8, 1, 'runtime'],
       ['povmloc-one', 4, 8, 1, 'runtime'],
    #    ['povmloc-one', 6, 8, 1, 'runtime'],
    #    ['povmloc-one', 8, 8, 1, 'runtime'],
    #    ['povmloc-one', 10, 8, 1, 'runtime'],
    #    ['povmloc-one', 12, 8, 1, 'runtime'],
    #    ['povmloc-one', 14, 8, 1, 'runtime'],
    ]

    for i, c in enumerate(config):
        command = template.format(c[0], c[1], c[2], c[3], c[4])
        print(command)
        p = Popen(command, shell=True)
        p.wait()


def generate_data():
    sen = 4
    template = "python main.py -m qml -l {} -s {} -rd  qml-data/c.{}x{}.{} -gd -c"
    grid_length = [2,4,6,8,10,12,14,16]
    ps = []
    for gl in grid_length:
        command = template.format(gl, sen, gl, gl, sen)
        print(command)
        p = Popen(command, shell=True)
        p.wait()
        # ps.append(Popen(command, shell=True))

    # for p in ps:
    #     p.wait()




if  __name__ == '__main__':
    
    # plot1()
    plot2()
    # plot3()

    # table()

    # generate_data()
    
