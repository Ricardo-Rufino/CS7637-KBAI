import numpy as np
from Frame3 import Frame3
from PIL import Image


class VisualSolver:
    problem_num = -1
    problem_debug = 0

    def __init__(self, problem):
        VisualSolver.problem_num += 1

        self.answer = -100
        self.problem = problem

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

        # Collection images from the potential answers.
        for i in self.answer_keys:

            # Collecting problem images.
            raven_figure = problem.figures[i]                       # RavenFigure object.
            image_path = raven_figure.visualFilename                # Filepath of figure.
            image = Image.open(image_path)                          # Image of the figure.
            image = image.convert("1")                              # Image converted into bi-level image.

            self.images_answers.append(image)

            if VisualSolver.problem_num == VisualSolver.problem_debug:
                print(image_path)
                print(image.size, image.width, image.height)
                print(image.mode)
                # image.show()

        self.get_answer()

    # Returns the number of white and dark pixels in the image.
    def __pixel_count(self, image: Image) -> tuple:
        histogram_array = image.histogram()
        white = histogram_array[-1]
        dark = histogram_array[0]

        return dark, white

    def __image_comparator(self, image1: Image, image2: Image) -> np.array:
        transformation = np.zeros((6, 1))

        # Difference in pixel count.-----------------------------------------
        dark1, white1 = self.__pixel_count(image1)
        dark2, white2 = self.__pixel_count(image2)

        transformation[0] = dark2-dark1

        return transformation

    def __row_col_transformation(self, image1: Image, image2: Image, image3: Image) -> list:
        transformation = []

        transformation.append(self.__image_comparator(image1, image2))
        transformation.append(self.__image_comparator(image2, image3))

        return transformation

    def __transformation_difference(self, transformation1: list, transformation2: list) -> int:
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

    def get_answer(self) -> int:
        a = self.images_problem[0]                                  # Location: (0,0)
        b = self.images_problem[1]                                  # Location: (0,1)
        c = self.images_problem[2]                                  # Location: (0,2)

        d = self.images_problem[3]                                  # Location: (1,0)
        f = self.images_problem[5]                                  # Location: (1,2)
        g = self.images_problem[6]                                  # Location: (2,0)
        h = self.images_problem[7]                                  # Location: (2,1)

        # Dictionary that contains the differences of all potential answers.
        diff = {}

        # Known transformation from the first row and column of the RPM.
        hor_tr1 = self.__row_col_transformation(a, b, c)
        ver_tr1 = self.__row_col_transformation(a, d, g)

        # Iterating through all the potential answers to find similar horizontal and vertical transformations.
        for i in range(0, len(self.images_answers)):
            ans = self.images_answers[i]
            hor_tr2 = self.__row_col_transformation(g, h, ans)
            ver_tr2 = self.__row_col_transformation(c, f, ans)

            # Differences between known and potential answers.
            hor_diff = self.__transformation_difference(hor_tr1, hor_tr2)
            ver_diff = self.__transformation_difference(ver_tr1, ver_tr2)

            if hor_diff == 0 and ver_diff == 0:
                self.answer = i+1
            else:
                difference = hor_diff + ver_diff
                diff[difference] = i+1

        sorted_answers = list(diff.keys())
        sorted_answers.sort()
        self.answer = diff[sorted_answers[0]]

        return self.answer


