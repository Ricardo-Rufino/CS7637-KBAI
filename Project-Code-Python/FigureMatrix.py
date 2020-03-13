import numpy as np


class FigureMatrix:
    def __init__(self):
        self.matrix = np.array([
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ])

    # Adds figure frame to the matrix.
    # @figure_frame     (Frame3)    frame of figure.
    def add(self, figure_frame):
        x = figure_frame.get_coordinate()[0]
        y = figure_frame.get_coordinate()[1]

        "**************************************************************************************************************"
        "           MAY HAVE TO TAKE INTO ACCOUNT INSIDE FIELD OF FIGURE'S FRAME TO DETERMINE LIST POSITION            "
        "**************************************************************************************************************"

        self.matrix[x][y].append(figure_frame)



