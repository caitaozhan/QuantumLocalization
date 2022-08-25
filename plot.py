import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class Plot:

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
                grid[i][j] = probs[4*i + j]
        plt.subplots(figsize=(16, 16))
        sns.heatmap(grid, linewidth=0.1, vmin=0, vmax=0.5, annot=True)
        plt.savefig(filename)

    @staticmethod
    def visualize_sensors(sensors: dict, level0_sensors: list, filename: str):
        '''
        Args:
            sensors -- a list of 2D locations
        '''
        X, Y = [], []
        for x, y in sensors.values():
            X.append(x)
            Y.append(y)
        X0, Y0 = [], []
        for sen_i in level0_sensors:
            X0.append(sensors[sen_i][0])
            Y0.append(sensors[sen_i][1])
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        ax.scatter(X, Y, c='red', s=40)
        ax.scatter(X0, Y0, c='black', s=60)
        ax.grid()
        ax.set_xticks(range(0, 17))
        ax.set_yticks(range(0, 17))
        ax.set_xlim(-0.1, 16.1)
        ax.set_ylim(-0.1, 16.1)
        ax.set_title('Scatter Plot for Sensors')
        print(filename)
        fig.savefig(filename)
