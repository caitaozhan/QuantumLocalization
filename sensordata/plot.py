import matplotlib.pyplot as plt


class Plot:

    @staticmethod
    def visualize_sensors(grid_len: int, sensors: dict, level0_sensors: list, filename: str):
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
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.scatter(X, Y, c='red', s=40)
        ax.scatter(X0, Y0, c='black', s=60)
        ax.grid()
        ax.set_xticks(range(0, grid_len + 1))
        ax.set_yticks(range(0, grid_len + 1))
        ax.set_xlim(-0.1, grid_len + 0.1)
        ax.set_ylim(-0.1, grid_len + 0.1)
        ax.set_title('Scatter Plot for Sensors')
        print(filename)
        fig.savefig(filename)
