'''a runner
'''

from subprocess import Popen, PIPE

if  __name__ == '__main__':
    
    # plot 1: Y: accuracy, X: varying grid size
    
                                  # length, size, noise, continuous
    template = 'python main.py -m {} -l {} -s {} -n {} -of {}'
    # 4 sensors
    config = [
    #     ['POVM-Loc-One', 2, 4, 1,  'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 4, 4, 1,  'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 6, 4, 1,  'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 8, 4, 1,  'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 10, 4, 1, 'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 12, 4, 1, 'onelevel.4sen.varygrid'],
        # ['POVM-Loc-One', 14, 4, 1, 'onelevel.4sen.varygrid'],
    #     ['POVM-Loc-One', 16, 4, 1, 'onelevel.4sen.varygrid']
    ]
    # 8 sensors
    config = [
        # ['POVM-Loc-One', 2, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 4, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 6, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 8, 8, 1,  'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 10, 8, 1, 'onelevel.8sen.varygrid']
        # ['POVM-Loc-One', 12, 8, 1, 'onelevel.8sen.varygrid'],
        # ['POVM-Loc-One', 14, 8, 1, 'onelevel.8sen.varygrid'],
        ['POVM-Loc-One', 16, 8, 1, 'onelevel.8sen.varygrid']
    ]

    for i, c in enumerate(config):
        # if c[1] != 16:
        #     continue
        command = template.format(c[0], c[1], c[2], c[3], c[4])
        print(command)
        p = Popen(command, shell=True)
        p.wait()
