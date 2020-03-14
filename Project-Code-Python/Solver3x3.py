import numpy as np

from Frame3 import Frame3
from FigureMatrix import FigureMatrix


class Solver3x3:
    def __init__(self, problem):
        self.problem = problem

        # Keys that will be used to access RavenFigure objects from RavensProblem objects.
        self.figure_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.answer_keys = ["1", "2", "3", "4", "5", "6", "7", "8"]

        # Lists that will be used to stored the RavenFigure objects.
        # Type: List<RavensFigure>
        # From: RavensProblem
        self.raven_fig_figures = []
        self.raven_fig_answers = []

        # Lists that will be used to store the RavenObject objects.
        # Type: Dictionary<Dictionary>
        # From: RavensFigure
        self.raven_obj_figures = {}
        self.raven_obj_answers = {}

        # Lists that contains the frames of the figures and potential answers.
        # Type: list<list>
        self.list_figure = []
        self.list_answers = []

        # ------------------------------------------------------------------------------------------------------------ #
        #                                 Collection RavenFigure and RavenObjects                                      #
        # ------------------------------------------------------------------------------------------------------------ #

        # Collecting RavenFigure and RavenObject objects for all figures in the problem set.
        for i in self.figure_keys:
            # Collecting RavenFigure objects.
            self.raven_fig_figures.append(problem.figures[i])

            # Collecting dictionary that contain RavenObjects.
            raven_objects = self.raven_fig_figures[-1].objects
            self.raven_obj_figures[i] = raven_objects

        # Collection RavenFigure and RavenObject objects for all possible answers.
        for i in self.answer_keys:
            # Collecting RavenFigure objects.
            self.raven_fig_answers.append(problem.figures[i])

            # Collecting dictionary that contain RavenObjects.
            raven_objects = self.raven_fig_answers[-1].objects
            self.raven_obj_answers[i] = raven_objects

        # ------------------------------------------------------------------------------------------------------------ #
        #                                Organizing RavenObjects into Frames (Frame3)                                  #
        # ------------------------------------------------------------------------------------------------------------ #

        print("")
        print("Figures:")
        # Organizing frames for all figures in the problem set from each object dictionary found in RavenFigure class.
        for figure in self.figure_keys:
            raven_object = self.raven_obj_figures[figure]           # RavenObject dictionary for a given figure.
            raven_object_keys = list(raven_object.keys())           # Keys for RavenFigure's Objects dictionary.
            list.sort(raven_object_keys)

            frames = []
            for key in raven_object_keys:
                frame = Frame3(figure, key, raven_object[key].attributes)
                frame.show()
                frames.append(frame)

            self.list_figure.append(frames)

        print("")
        print("Answers:")
        # Organizing frames for all potential answers from each object dictionary found in RavenFigure class.
        for figure in self.answer_keys:
            raven_object = self.raven_obj_answers[figure]           # RavenObject dictionary for a given figure.
            raven_object_keys = list(raven_object.keys())           # Keys for RavenFigure's Objects dictionary.
            list.sort(raven_object_keys)

            frames = []
            for key in raven_object_keys:
                frame = Frame3(figure, key, raven_object[key].attributes)
                frame.show()
                frames.append(frame)

            self.list_answers.append(frames)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                          Creating FigureMatrices                                             #
        # ------------------------------------------------------------------------------------------------------------ #

        for frames in self.list_figure:
            self.figure_matrix_creator(frames)



    # Creates figure matrix for a given figure in the raven's problem.
    # @frame_list       (list<Frame3>)      list containing the frames of the given figure.
    # @return           (FigureMatrix)      matrix representation of the figure.
    def figure_matrix_creator(self, frame_list):
        matrix = FigureMatrix()

        for figure in frame_list:
            matrix.add(figure)

        matrix.show()

        return matrix

    def raven_matrix_creator(self, figure_list):
        return -30

    def answer(self):
        return -30
