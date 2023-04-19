'''a runner
'''

from subprocess import Popen, PIPE
import sys


def discrete():
    # plot 1: Discrete case. Methods: QSD-One and PQC-One-C. 
    #         Y: CC_accuracy, X: varying grid size
    
                                  # length, size, noise, continuous
    # povmloc-one

    # template = 'python main.py -m {} -l {} -s {} -of {}'
    # config = [
    #     ['povmloc-one', 2,  4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 4,  4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 6,  4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 8,  4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 9,  8, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 10, 4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 12, 4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 14, 4, 'discrete.onelevel.varygrid'],
    #     ['povmloc-one', 16, 8, 'discrete.onelevel.varygrid.8sen']
    # ]
    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()


    # povmloc (twolevel)

    # template = 'python main.py -m {} -l {} -s {} -of {}'
    # config = [
        # ['povmloc', 4,  8, 'discrete.twolevel.varygrid'],
        # ['povmloc', 9,  8, 'discrete.twolevel.varygrid'],
        # ['povmloc', 12, 8, 'discrete.twolevel.varygrid'],
        # ['povmloc', 16, 8, 'discrete.twolevel.varygrid'],
    #     ['povmloc', 16, 4, 'discrete.twolevel.qsd'],
    # ]
    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()


    # qml onelevel

    # template = 'python main.py -m {} -l {} -s {} -of {} -rd {}'
    # config = [
        # ['qml', 2,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 4,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 6,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 8,  16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 9,  8, 'discrete.onelevel.pqc'],
        # ['qml', 10, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 12, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 14, 16, 'discrete.onelevel.varygrid.qml.16sen'],
        # ['qml', 16, 16, 'discrete.onelevel.varygrid.qml.16sen']
    # ]

    # for i, c in enumerate(config):
    #     rood_dir = f'qml-data/{c[1]}x{c[1]}.{c[2]}'
    #     command = template.format(c[0], c[1], c[2], c[3], rood_dir)
    #     print(command)
    #     sys.stdout.flush()
    #     p = Popen(command, shell=True)
    #     p.wait()


    # qml-two

    template = 'python main.py -m {} -l {} -s {} -of {} -rd {}'
    config = [
        ['qml-two', 4,  8, 'discrete.twolevel.pqc'],
        ['qml-two', 9,  8, 'discrete.twolevel.pqc'],
        ['qml-two', 12, 8, 'discrete.twolevel.pqc'],
        ['qml-two', 16, 8, 'discrete.twolevel.pqc'],
        ['qml-two', 16, 4, 'discrete.twolevel.pqc'],
        ['qml-two', 16, 16, 'discrete.twolevel.pqc'],
    ]

    for i, c in enumerate(config):
        rood_dir = f'qml-data/{c[1]}x{c[1]}.{c[2]}.two'
        command = template.format(c[0], c[1], c[2], c[3], rood_dir)
        print(command)
        sys.stdout.flush()
        p = Popen(command, shell=True)
        p.wait()


def plot1_part1():
    # onelevel  : Continuous case. Methods: QSD-One and PQC-One-R. 
    #          Y: CC_accuracy,  X: varying grid size
    
                               # length, size, noise, continuous
    # template = 'python main.py -m {} -l {} -s {} -of {} -c'
    # povmloc-one
    # config = [
        # ['povmloc-one', 2,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 4,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 6,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 8,  8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 9,  8, 'continuous.onelevel.varygrid.8sen'],
        # ['povmloc-one', 10, 8, 'continuous.onelevel.varygrid.8sen.1'],
        # ['povmloc-one', 12, 8, 'continuous.onelevel.varygrid.8sen.2'],
        # ['povmloc-one', 14, 8, 'continuous.onelevel.varygrid.8sen.2'],
    #     ['povmloc-one', 16, 8, 'continuous.onelevel.varygrid.8sen.1']
    # ]
    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()

    
    # qml

    template = 'python main.py -m {} -l {} -s {} -of {} -rd {} -c'
    config = [
        # ['qml', 2,  16, 'discrete.onelevel.varygrid.pqc.4sen'],
        # ['qml', 4,  16, 'discrete.onelevel.varygrid.pqc.16sen'],
        # ['qml', 6,  16, 'discrete.onelevel.varygrid.pqc.16sen'],
        # ['qml', 8,  16, 'discrete.onelevel.varygrid.pqc.16sen'],
        ['qml', 9, 8, 'discrete.onelevel.varygrid.pqc.8sen'],
        # ['qml', 10, 16, 'discrete.onelevel.varygrid.pqc.16sen'],
        # ['qml', 12, 16, 'discrete.onelevel.varygrid.pqc.16sen'],
        # ['qml', 14, 16, 'discrete.onelevel.varygrid.pqc.16sen'],
        # ['qml', 16, 16, 'discrete.onelevel.varygrid.pqc.16sen']
    ]

    for i, c in enumerate(config):
        root_dir = f'qml-data/c.{c[1]}x{c[1]}.{c[2]}'
        command = template.format(c[0], c[1], c[2], c[3], root_dir)
        print(command)
        sys.stdout.flush()
        p = Popen(command, shell=True)
        p.wait()

def plot1_part2():
    # twolevel : Continuous case. Methods: QSD-Two, and PQC-Two. 
    #         Y: CC_accuracy,  X: varying grid size
    
                               # length, size, noise, continuous
    # qml-two
    template = 'python main.py -m {} -l {} -s {} -of {} -rd {} -c'
    config = [
        # ['qml-two', 4,  8, 'continuous.twolevel.varygrid.pqc'],
        # ['qml-two', 9,  8, 'continuous.twolevel.varygrid.pqc'],
        # ['qml-two', 12, 8, 'continuous.twolevel.varygrid.pqc'],
        ['qml-two', 16, 16, 'continuous.twolevel.pqc']
    ]
    for i, c in enumerate(config):
        root_dir = f'qml-data/c.{c[1]}x{c[1]}.{c[2]}.two'
        command = template.format(c[0], c[1], c[2], c[3], root_dir)
        print(command)
        p = Popen(command, shell=True)
        p.wait()

    
    # povmloc
    # template = 'python main.py -m {} -l {} -s {} -of {} -c'
    # config = [
    #     ['povmloc', 16,  4, 'continuous.twolevel.varysen'],
    # ]
    # for i, c in enumerate(config):
    #     command = template.format(c[0], c[1], c[2], c[3])
    #     print(command)
    #     p = Popen(command, shell=True)
    #     p.wait()


def plot2():
    # part of the data needed for plot 2 is already done by plot 1
    # qml
    template = 'python main.py -m {} -l {} -s {} -of {} -rd {} -c'
    config = [
        ['qml-two', 16, 4,  'continuous.twolevel.pqc'],
        # ['qml-two', 16, 16, 'continuous.twolevel.pqc'],
    ]
    for i, c in enumerate(config):
        root_dir = f'qml-data/c.{c[1]}x{c[1]}.{c[2]}.two'
        command = template.format(c[0], c[1], c[2], c[3], root_dir)
        print(command)
        p = Popen(command, shell=True)
        p.wait()


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
    # template = "python main.py -m qml-two -l {} -s {} -rd  qml-data/c.{}x{}.{}.two -gd -c"
    template = "python main.py -m qml-two -l {} -s {} -rd  qml-data/{}x{}.{}.two -gd"
    # sen = 8
    # grid_length = [4,9,12,16]
    # for gl in grid_length:
    gl = 16
    sennum = [4, 16]
    for sen in sennum:
        command = template.format(gl, sen, gl, gl, sen)
        print(command)
        p = Popen(command, shell=True)
        p.wait()





if  __name__ == '__main__':
    
    discrete()
    
    # plot1_part1()
    # plot1_part2()
    
    # plot2()
    
    # plot3()

    # table()

    # generate_data()
    
