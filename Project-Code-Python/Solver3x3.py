import numpy as np

from Frame3 import Frame3

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
        # Type: List<Dictionary>
        # From: RavensFigure
        self.raven_obj_figures = []
        self.raven_obj_answers = []

        # Lists that contains the frame of the figures and potential answers.
        self.list_figure = []
        self.list_answers = []

        # ------------------------------------------------------------------------------------------------------------ #
        #                                 Collection RavenFigure and RavenObjects
        # ------------------------------------------------------------------------------------------------------------ #

        # Collecting RavenFigure and RavenObject objects for all figures in the problem set.
        for i in self.figure_keys:
            # Collecting RavenFigure objects.
            self.raven_fig_figures.append(problem.figures[i])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = self.raven_fig_figures[-1].objects
            self.raven_obj_figures.append(fig_dict)

        # Collection RavenFigure and RavenObject objects for all possible answers.
        for i in self.answer_keys:
            # Collecting RavenFigure objects.
            self.raven_fig_answers.append(problem.figures[i])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = self.raven_fig_answers[-1].objects
            self.raven_obj_answers.append(fig_dict)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                Organizing RavenObjects into Frames (Frame3)
        # ------------------------------------------------------------------------------------------------------------ #

        # Organizing frames for all figures in the problem set from each object dictionary found in RavenFigure class.
        for object_dict in self.raven_obj_figures:
            keys = list(object_dict.keys())
            list.sort(keys)

            frames = []
            for key in keys:
                frame = Frame3(key, object_dict[key].attributes)
                frame.show()
                frames.append(frame)

        # Organizing frames for all potential answers from each object dictionary found in RavenFigure class.
        for object_dict in self.raven_obj_figures:
            keys = list(object_dict.keys())
            list.sort(keys)

            frames = []
            for key in keys:
                frames.append(Frame3(key, object_dict[key].attributes))



        # for i in range(0, len(raven_obj_figures)):
        #     attributes = raven_obj_figures[i]
        #     keys = list(attributes.keys())
        #     list.sort(keys)
        #
        #     frame_ds = []
        #     for key in keys:
        #         frame_ds.append(self.frame_creator(key, attributes[key].attributes))
        #
        #     # Arranging frames into their respective spot on the matrix.
        #     list_figure.append(frame_ds)
        #
        # for i in range(0, len(raven_obj_answers)):
        #     attributes = raven_obj_answers[i]
        #     keys = list(attributes.keys())
        #     list.sort(keys)
        #
        #     frame_ds = []
        #     for key in keys:
        #         frame_ds.append(self.frame_creator(key, attributes[key].attributes))
        #
        #     # Arranging frames into their respective spot on the matrix.
        #     list_answers.append(frame_ds)

    def answer(self):
        return -30