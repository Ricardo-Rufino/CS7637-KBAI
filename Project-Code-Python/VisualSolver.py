import numpy as np
from Frame3 import Frame3
from PIL import Image


class VisualSolver:
    problem_num = -1
    problem_debug = 0

    def __init__(self, problem, size_dictionary: dict):
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

        # List of Images for both problems and potential answers.
        # Type: List<Image>
        # From: RavensFigure (indirectly through filepath).
        self.images_problem = []
        self.images_answers = []

        # ------------------------------------------------------------------------------------------------------------ #
        #                                        Collection RavenFigures                                               #
        # ------------------------------------------------------------------------------------------------------------ #

        # Collecting RavenFigure and RavenObject objects for all figures in the problem set.
        for i in self.figure_keys:

            # Collecting images from the RPM.
            raven_figure = problem.figures[i]                       # RavenFigure object.
            image_path = raven_figure.visualFilename                # Filepath of figure.
            image = Image.open(image_path)                          # Image of the figure.
            image = image.convert("1")                              # Image converted into bi-level image.

            self.images_problem.append(image)

            if VisualSolver.problem_num == VisualSolver.problem_debug:
                print(image_path)
                print(image.size, image.width, image.height)
                print(image.mode)
                print(image.histogram())
                print(type(image))

                # image.show()

            print(type(image))

        # Collection images from the potential answers.
        for i in self.answer_keys:

            # Collecting problem images.
            raven_figure = problem.figures[i]                       # RavenFigure object.
            image_path = raven_figure.visualFilename                # Filepath of figure.
            image = Image.open(image_path)                          # Image of the figure.

            self.images_answers.append(image)

            if VisualSolver.problem_num == VisualSolver.problem_debug:
                print(image_path)
                print(image.size, image.width, image.height)
                print(image.mode)
                # image.show()

    # Returns the number of white and dark pixels in the image.
    def pixel_count(self, image: Image) -> tuple:
        histogram_array = image.histogram()
        white = histogram_array[-1]
        dark = histogram_array[0]

        return dark, white

    def image_comparator(self, image1: Image, image2: Image) -> np.array:
        transformation = np.zeros((6, 1))

        # Difference in pixel count.-----------------------------------------
        dark1, white1 = self.pixel_count(image1)
        dark2, white2 = self.pixel_count(image2)

        transformation[0] = dark2-dark1

        return transformation

    def row_col_transformation(self, image1: Image, image2: Image, image3: Image) -> list:
        transformation = []

        transformation.append(self.image_comparator(image1, image2))
        transformation.append(self.image_comparator(image2, image3))

        return transformation

    def transformation_difference(self, transformation1: list, transformation2: list) -> int:
        counter = 0

        for i in range(0, len(transformation1)):
            array1 = transformation1[i]
            array2 = transformation2[i]

            for k in range(0, len(array1)):
                el1 = array1[k]
                el2 = array2[k]

                if el1 != el2:
                    counter += 1

        return counter

    def answer_selector(self):
        a = self.images_problem[0]
        b = self.images_problem[1]
        c = self.images_problem[2]

        d = self.images_problem[3]
        h = self.images_problem[6]

        hor_transformation = self.row_col_transformation(a, b, c)
        ver_transformation = self.row_col_transformation(a, d, h)

        pass

