'''a runner
'''

from subprocess import Popen, PIPE


def plot1():
    # plot 1: POVMLoc (one level). Y: accuracy, X: varying grid size
    
                                  # length, size, noise, continuous
    template = 'python main.py -m {} -l {} -s {} -n {} -of {}'
    # 4 sensors
    config = [
        ['POVM-Loc-One', 2, 4, 1,  'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 4, 4, 1,  'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 6, 4, 1,  'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 8, 4, 1,  'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 10, 4, 1, 'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 12, 4, 1, 'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 14, 4, 1, 'onelevel.4sen.varygrid'],
        ['POVM-Loc-One', 16, 4, 1, 'onelevel.4sen.varygrid']
    ]
    # 8 sensors
    # config = [
        # ['POVM-Loc-One', 2, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 4, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 6, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 8, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 10, 8, 1, 'onelevel.8sen.varygrid']
        # ['POVM-Loc-One', 12, 8, 1, 'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 14, 8, 1, 'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 16, 8, 1, 'onelevel.8sen.varygrid']
    # ]

    for i, c in enumerate(config):
        # if c[1] != 16:
        #     continue
        command = template.format(c[0], c[1], c[2], c[3], c[4])
        print(command)
        p = Popen(command, shell=True)
        p.wait()



def plot2():
    # plot 2: POVMLoc and POVMLoc-Pro. Y: accuracy, X: varying noise
    
    template = 'python main.py -m {} {} -l {} -n {} -of {}'
    config = [
        ['', 'povmloc-pro', 16, 0, 'twolevel.noise0'],
        ['', 'povmloc-pro', 16, 1, 'twolevel.noise1'],
        ['povmloc', 'povmloc-pro', 16, 2, 'twolevel.noise2'],
        ['povmloc', 'povmloc-pro', 16, 3, 'twolevel.noise3'],
        ['povmloc', 'povmloc-pro', 16, 4, 'twolevel.noise4'],
    ]

    for i, c in enumerate(config):
        command = template.format(c[0], c[1], c[2], c[3], c[4])
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
    template = "python main.py -m qml -l {} -s 16 -rd  qml-data/{}x{}.16 -gd"
    grid_length = [4, 6, 8, 10, 12, 14, 16]
    ps = []
    for gl in grid_length:
        command = template.format(gl, gl, gl)
        print(command)
        ps.append(Popen(command, shell=True))
    for p in ps:
        p.wait()




if  __name__ == '__main__':
    
    # plot1()
    # plot2()
    # plot3()

    # table()

    generate_data()
    
