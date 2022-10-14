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
    
                                  # length, size, noise, continuous
    template = 'python main.py -m {} {} -l {} -n {} -of {}'
    config = [
        ['', 'povmloc-pro', 16, 0, 'twolevel.noise0'],
        ['', 'povmloc-pro', 16, 1, 'twolevel.noise1'],
        ['povmloc', 'povmloc-pro', 16, 2, 'twolevel.noise2'],
        ['povmloc', 'povmloc-pro', 16, 3, 'twolevel.noise3'],
        ['povmloc', 'povmloc-pro', 16, 4, 'twolevel.noise4'],
    ]

    for i, c in enumerate(config):
        # if c[1] != 16:
        #     continue
        command = template.format(c[0], c[1], c[2], c[3], c[4])
        print(command)
        p = Popen(command, shell=True)
        p.wait()



if  __name__ == '__main__':
    
    # plot1()
    plot2()
    