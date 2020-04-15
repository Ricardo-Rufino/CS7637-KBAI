import numpy as np
from Frame3 import Frame3
from PIL import Image, ImageChops


class VisualSolver:
    problem_num = 0                                             # Problem number.
    problem_inv = 3                                             # Problem to investigate.

    def __init__(self, problem):
        VisualSolver.problem_num += 1

        self.answer = -100
        self.problem = problem
        self.debug = VisualSolver.problem_num == VisualSolver.problem_inv

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

        if self.debug:
            print("\nAnalysis of " + problem.name + "--------------------", end='\n\n')
            print("Figures: ")

        # Collecting RavenFigure and RavenObject objects for all figures in the problem set.
        for i in self.figure_keys:

            # Collecting images from the RPM.
            raven_figure = self.problem.figures[i]                  # RavenFigure object.
            image_path = raven_figure.visualFilename                # Filepath of figure.
            image = Image.open(image_path)                          # Image of the figure.
            image = image.convert("1")                              # Image converted into bi-level image.

            self.images_problem.append(image)

            if self.debug:
                print(image_path)
                # print(image.size, image.width, image.height)
                # print(image.mode)
                # print(image.histogram())
                # print(type(image))

                # image.show()

        if self.debug:
            print("\nPotential answers: ")

        # Collection images from the potential answers.
        for i in self.answer_keys:

            # Collecting problem images.
            raven_figure = self.problem.figures[i]                  # RavenFigure object.
            image_path = raven_figure.visualFilename                # Filepath of figure.
            image = Image.open(image_path)                          # Image of the figure.
            image = image.convert("1")                              # Image converted into bi-level image.

            self.images_answers.append(image)

            if self.debug:
                print(image_path)
                # print(image.size, image.width, image.height)
                # print(image.mode)
                # image.show()

        self.get_answer()

    def __image_comparator(self, image1: Image, image2: Image) -> np.array:
        transformation = np.zeros((6, 1))

        # Difference in pixel count.-----------------------------------------
        dark1, white1 = self.__pixel_count(image1)
        dark2, white2 = self.__pixel_count(image2)

        # if self.debug:
        #     print("Dark 1: " + str(dark1))
        #     print("Dark 2: " + str(dark2))

        # Identifies if a change in image has occurred.
        if dark1 != dark2:
            transformation[0] = 1
        if dark2 > 1.2*dark1 or dark2 < 0.8*dark1:
            transformation[1] = 1

        return transformation

    def __row_col_transformation(self, image1: Image, image2: Image, image3: Image) -> list:
        transformation = []

        transformation.append(self.__image_comparator(image1, image2))
        transformation.append(self.__image_comparator(image2, image3))

        return transformation

    def __transformation_difference(self, transformation1: list, transformation2: list) -> None:
        counter = 0

        for i in range(0, len(transformation1)):
            array1 = transformation1[i]
            array2 = transformation2[i]

            for k in range(0, len(array1)):
                el1 = array1[k]
                el2 = array2[k]

                if el1 != el2:
                    counter += float(np.abs(el1) + np.abs(el2))

        return counter

    def __print_transformation_list(self, tr1: list, tr2: list) -> None:
        array1 = tr1[0]
        array2 = tr1[1]
        array3 = tr2[0]
        array4 = tr2[1]

        for i in range(0, len(array1)):
            print("\t '{0}'  '{1}' \t|\t '{2}'  '{3}'".format(array1[i], array2[i], array3[i], array4[i], align='^', width='10'))

    def __diagonal_analysis(self, image1: Image, image2: Image) -> int:
        pass

    def get_answer(self) -> None:
        a = self.images_problem[0]                                  # Location: (0,0)
        b = self.images_problem[1]                                  # Location: (0,1)
        c = self.images_problem[2]                                  # Location: (0,2)

        d = self.images_problem[3]                                  # Location: (1,0)
        e = self.images_problem[4]                                  # Location: (1,1)
        f = self.images_problem[5]                                  # Location: (1,2)

        g = self.images_problem[6]                                  # Location: (2,0)
        h = self.images_problem[7]                                  # Location: (2,1)

        # Checks if diagonals are the same.
        if self.__are_equal(a, e):
            if self.debug:
                print("\nDiagonal are equal!")

            ans = self.__diagonal_analysis(e, self.images_answers)
            if ans > 0:
                self.answer = ans
                return

        # Dictionary that contains the differences of all potential answers.
        diff = {}

        # Known transformation from the first row and column of the RPM.
        hor_tr1 = self.__row_col_transformation(a, b, c)
        ver_tr1 = self.__row_col_transformation(a, d, g)

        if self.debug:
            print("\nHorizontal and Vertical Lists: ")
            self.__print_transformation_list(hor_tr1, ver_tr1)

        # Iterating through all the potential answers to find similar horizontal and vertical transformations.
        for i in range(0, len(self.images_answers)):
            ans = self.images_answers[i]
            hor_tr2 = self.__row_col_transformation(g, h, ans)
            ver_tr2 = self.__row_col_transformation(c, f, ans)

            # Differences between known and potential answers.
            hor_diff = self.__transformation_difference(hor_tr1, hor_tr2)
            ver_diff = self.__transformation_difference(ver_tr1, ver_tr2)

            if self.debug:
                print("\nAnswer " + str(i+1))
                self.__print_transformation_list(hor_tr2, ver_tr2)

            if hor_diff == 0 and ver_diff == 0:
                self.answer = i+1
                return
            else:
                difference = hor_diff + ver_diff
                diff[difference] = i+1

        sorted_answers = list(diff.keys())
        sorted_answers.sort()
        self.answer = diff[sorted_answers[0]]

    # ---------------------------------------------------------------------------------------------------------------- #
    # Functions that Compare Images
    # ---------------------------------------------------------------------------------------------------------------- #

    def __are_equal(self, image1: Image, image2: Image) -> bool:
        difference = ImageChops.difference(image1, image2)

        # Dark and white pixels of the first and second image.
        dark1, white1 = self.__pixel_count(image1)
        dark2, white2 = self.__pixel_count(image2)

        # Checking for ratio of sameness.
        dark3, white3 = self.__pixel_count(difference)
        total = dark3 + white3
        sameness = dark3/total

        # Checking for dark ratio.
        dark_ratio = dark1/dark2

        if self.debug:
            print("\tEquality: " + str(sameness))
            print("\tDark Ratio: " + str(dark_ratio))
            print("\tDark 1: " + str(dark1))
            print("\tDark 1: " + str(dark2), end="\n\n")

        # Equality will be defined if these two metrics are passed.
        if sameness > 0.95 and 0.95 < dark_ratio < 1.05:
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Helper Functions
    # ---------------------------------------------------------------------------------------------------------------- #

    # Returns the number of white and dark pixels in the image.
    def __pixel_count(self, image: Image) -> tuple:
        histogram_array = image.histogram()
        white = histogram_array[-1]
        dark = histogram_array[0]

        return float(dark), float(white)

    def __diagonal_analysis(self, image: Image, ans: list) -> int:
        for i in range(0, len(ans)):
            if self.__are_equal(image, ans[i]):
                return i + 1
        return -1