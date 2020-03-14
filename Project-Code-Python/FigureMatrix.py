import numpy as np


class FigureMatrix:
    def __init__(self):
        self.matrix = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]

    # Adds figure frame to the matrix.
    # @figure_frame     (Frame3)    frame of figure.
    def add(self, figure_frame):
        x = figure_frame.get_coordinate()[0]
        y = figure_frame.get_coordinate()[1]

        "**************************************************************************************************************"
        "           MAY HAVE TO TAKE INTO ACCOUNT INSIDE FIELD OF FIGURE'S FRAME TO DETERMINE LIST POSITION            "
        "**************************************************************************************************************"

        self.matrix[x][y].append(figure_frame)

    def map(self):
        map = np.zeros((3, 3))
        row, col = map.shape

        for i in range(0, row):
            for j in range(0, col):
                if len(self.matrix[row][col]) != 0:
                    map[row][col] = 1

        print(map)

    def show(self):
        print(self.matrix)


