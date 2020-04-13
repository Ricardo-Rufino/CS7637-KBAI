import numpy
from Frame3 import Frame3
from PIL import Image



class VisualSolver:
    problem_num = -1

    def __init__(self, problem, size_dictionary):
        VisualSolver.problem_num += 1

        self.answer = -100
        self.problem = problem
        self.size_dictionary = size_dictionary

        # Keys that will be used to access RavenFigure objects from RavensProblem objects.
        self.figure_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.answer_keys = ["1", "2", "3", "4", "5", "6", "7", "8"]

        # Lists that will be used to stored the RavenFigure objects.
        # Type: List<RavensFigure>
        # From: RavensProblem
        self.raven_fig_figures = []
        self.raven_fig_answers = []

        #
        self.images_problem = []
        self.images_answers = []

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
            raven_figure = problem.figures[i]
            image_path = raven_figure.visualFilename
            image = Image.open(image_path)

            self.images_problem.append(image)

            if VisualSolver.problem_num == 1:
                print(image_path)
                print(image.size, image.width, image.height)
                print(image.mode)
                image.show()


        # Collection RavenFigure and RavenObject objects for all possible answers.
        for i in self.answer_keys:
            # Collecting RavenFigure objects.
            self.raven_fig_answers.append(problem.figures[i])

            # Collecting dictionary that contain RavenObjects.
            raven_objects = self.raven_fig_answers[-1].objects
            self.raven_obj_answers[i] = raven_objects