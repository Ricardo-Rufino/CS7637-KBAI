import numpy as np
from Frame3 import Frame3
from PIL import Image, ImageChops, ImageOps


class VisualSolver:
    problem_num = 0  # Problem number.
    problem_inv = 13  # Problem to investigate.

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
            raven_figure = self.problem.figures[i]  # RavenFigure object.
            image_path = raven_figure.visualFilename  # Filepath of figure.
            image = Image.open(image_path)  # Image of the figure.
            image = image.convert("1")  # Image converted into bi-level image.

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
            raven_figure = self.problem.figures[i]  # RavenFigure object.
            image_path = raven_figure.visualFilename  # Filepath of figure.
            image = Image.open(image_path)  # Image of the figure.
            image = image.convert("1")  # Image converted into bi-level image.

            self.images_answers.append(image)

            if self.debug:
                print(image_path)
                # print(image.size, image.width, image.height)
                # print(image.mode)
                # image.show()

        tuple(self.images_problem)
        tuple(self.images_answers)

        self.get_answer()

    # ---------------------------------------------------------------------------------------------------------------- #
    # Main Solver Function
    # ---------------------------------------------------------------------------------------------------------------- #

    def get_answer(self) -> None:
        (a, b, c, d, e, f, g, h) = self.images_problem

        if self.debug:
            ans = self.images_answers[0]
            image1 = ImageChops.logical_and(g, h)
            print(self.__are_equal(image1, ans))
            image1.show()




        # Special cases.------------------------------------------------------------------------------------------------

        # Checks if horizontal figures are the same.
        if self.__horizontal_addition():
            print("Used function: same_horizontal")
            return

        # Checks if diagonals are the same.
        if self.__same_diagonal():
            print("Used function: same_diagonal")
            return

        # Check if same difference is found in rows and columns.
        if self.__same_inner_outer():
            print("Used function: same_inner_outer")
            return

        if self.__same_horizontal_outer():
            print("Used function: same_horizontal_outer")
            return

        if self.__sameness_comparator():
            print("Used function: sameness_comparator")
            return

        if self.__guess_by_uniqueness():
            print("Used function: guess_by_uniqueness")
            return

        # --------------------------------------------------------------------------------------------------------------

        # # Dictionary that contains the differences of all potential answers.
        # diff = {}
        #
        # # Known transformation from the first row and column of the RPM.
        # hor_tr1 = self.__row_col_transformation(a, b, c)
        # ver_tr1 = self.__row_col_transformation(a, d, g)
        #
        # if self.debug:
        #     print("\nHorizontal and Vertical Lists: ")
        #     self.__print_transformation_list(hor_tr1, ver_tr1)
        #
        # # Iterating through all the potential answers to find similar horizontal and vertical transformations.
        # for i in range(0, len(self.images_answers)):
        #     ans = self.images_answers[i]
        #     hor_tr2 = self.__row_col_transformation(g, h, ans)
        #     ver_tr2 = self.__row_col_transformation(c, f, ans)
        #
        #     # Differences between known and potential answers.
        #     hor_diff = self.__transformation_difference(hor_tr1, hor_tr2)
        #     ver_diff = self.__transformation_difference(ver_tr1, ver_tr2)
        #
        #     if self.debug:
        #         print("\nAnswer " + str(i+1))
        #         self.__print_transformation_list(hor_tr2, ver_tr2)
        #
        #     if hor_diff == 0 and ver_diff == 0:
        #         self.answer = i+1
        #         return
        #     else:
        #         difference = hor_diff + ver_diff
        #         diff[difference] = i+1
        #
        # sorted_answers = list(diff.keys())
        # sorted_answers.sort()
        # self.answer = diff[sorted_answers[0]]

    # ---------------------------------------------------------------------------------------------------------------- #
    # Specific Case Functions
    # ---------------------------------------------------------------------------------------------------------------- #

    # Function that checks if the horizontal images are the same.
    # Helps with the following problems:
    # D-01
    def __horizontal_addition(self) -> bool:
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Addition of first row.
        ab = self.__add_images(a, b)
        row1 = self.__are_equal(ab, c)

        # Addition of second row.
        de = self.__add_images(d, e)
        row2 = self.__are_equal(de, f)

        # Partial addition of third row.
        gh = self.__add_images(g, h)

        # Finding potential answer.
        if row1 and row2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]
                if self.__are_equal(gh, ans):
                    self.answer = i + 1
                    return True

        return False

    # Function that checks if first two diagonal images are the same, if so, then it looks for a potential image from
    # the answer pool that keeps this trend.
    # Helps with the following problems:
    # D-02
    # D-03
    # D-11
    def __same_diagonal(self) -> bool:
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checking if diagonals are equal.
        ae_equal = self.__are_equal(a, e)
        dh_equal = self.__are_equal(d, h)
        bf_equal = self.__are_equal(b, f)

        # Looking for answer.
        if ae_equal and dh_equal and bf_equal:
            for i in range(0, len(self.images_answers)):
                ans = self.images_answers[i]
                if self.__are_equal(e, ans, show=True):
                    self.answer = i + 1
                    return True

        return False

    # Function that checks if the inner image remains the same (horizontally) and if the outer image remains the same
    # (vertically).
    # Helps with the following problems:
    # D-04
    def __same_inner_outer(self) -> bool:
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Images that display similarities.
        # Horizontal:
        ab = self.__same_inner(a, b)
        bc = self.__same_inner(b, c)
        gh = self.__same_inner(g, h)

        # Vertical:
        ad = self.__same_outer(a, d)
        dg = self.__same_outer(d, g)
        cf = self.__same_outer(c, f)

        if ab and bc and gh:
            if ad and dg and cf:
                for i in range(0, len(self.images_answers)):
                    # Potential horizontal and vertical piece.
                    hi = self.__same_inner(h, self.images_answers[i])
                    fi = self.__same_outer(f, self.images_answers[i])

                    if hi and fi:
                        self.answer = i + 1
                        return True
        return False

    # Function that checks if the horizontal images are the same and that the vertical outer images are the same.
    def __same_horizontal_outer(self):
        inner_images = []  # List of images with removed borders.
        outer_images = []  # List of images with removed centers.

        for i in self.images_problem:
            inner_images.append(self.__remove_border(i))
            outer_images.append(self.__remove_center(i))

        # Checking that the current problem contains this trend.
        for i in [0, 3]:

            row_inner = []
            for j in range(3):
                row_inner.append(inner_images[i + j])

                if not self.__are_equal(outer_images[i + j], outer_images[i + j]):
                    return False

            if not self.__unique_images(row_inner):
                return False

        # Trying to find a answer.
        if self.__are_equal(outer_images[-2], outer_images[-1]):
            row_inner = [inner_images[-2], inner_images[-1]]
            for i in range(len(self.images_answers)):

                ans_outer = self.__remove_center(self.images_answers[i])
                ans_inner = self.__remove_border(self.images_answers[i])

                row_inner.append(ans_inner)

                if self.__are_equal(outer_images[-1], ans_outer) and self.__unique_images(row_inner):
                    self.answer = i + 1
                    return True

                else:
                    row_inner.pop()

        return False

    # This function checks if the sameness across rows rows and columns is the same; and that columns contain unique
    # inner images.
    def __sameness_comparator(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Comparing sameness of first row.
        ab = ImageChops.logical_or(a, b)
        bc = ImageChops.logical_or(b, c)
        same_first_row = self.__are_equal(ab, bc)

        # Comparing sameness of first column.
        ad = ImageChops.logical_or(a, d)
        dg = ImageChops.logical_or(d, g)
        same_first_col = self.__are_equal(ad, dg)

        # Checking for unique inner shapes in each column.
        unique_first_col = self.__unique_inner(a, d, g)

        # Check for solution.
        if same_first_row and same_first_col and unique_first_col:
            gh = ImageChops.logical_or(g, h)  # Sameness of partial third row.
            cf = ImageChops.logical_or(c, f)  # Sameness of partial third column.
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                hi = ImageChops.logical_or(h, ans)
                fi = ImageChops.logical_or(f, ans)

                same_third_row = self.__are_equal(gh, hi)
                same_third_col = self.__are_equal(cf, fi)
                unique_third_col = self.__unique_inner(c, f, ans)

                if same_third_row and same_third_col and unique_third_col:
                    self.answer = i + 1
                    return True

        return False

    # Helps with the following problems:
    # D-05
    # D-07
    # D-09
    # D-10
    def __guess_by_uniqueness(self) -> bool:
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checking if images in the problem are unique.
        for i in range(len(self.images_problem)):
            for j in range(len(self.images_problem)):
                image1 = self.images_problem[i]
                image2 = self.images_problem[j]
                if i != j and self.__are_equal(image1, image2):
                    return False

        # Check for potential answer.
        ans = self.images_answers
        for i in range(len(ans)):
            counter = 0
            for j in self.images_problem:
                if self.__are_equal(ans[i], j):
                    continue
                counter += 1

            if counter == len(ans):
                self.answer = i + 1
                return True

        return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Functions that Compare Images
    # ---------------------------------------------------------------------------------------------------------------- #

    # Checks if images are the same.
    def __are_equal(self, image1: Image, image2: Image, show=None) -> bool:
        difference = ImageChops.difference(image1, image2)

        # Dark and white pixels of the first and second image.
        dark1, white1 = self.__pixel_count(image1)
        dark2, white2 = self.__pixel_count(image2)

        # Checking for ratio of sameness.
        dark3, white3 = self.__pixel_count(difference)
        total = dark3 + white3
        sameness = dark3 / total

        # Checking for dark ratio.
        if dark1 == 0 and dark2 == 0:
            dark_ratio = 1
        elif dark1 < dark2:
            dark_ratio = dark1 / dark2
        else:
            dark_ratio = dark2 / dark1

        if self.debug and show is True:
            print("\tEquality: " + str(sameness))
            print("\tDark Ratio: " + str(dark_ratio))
            print("\tDark 1: " + str(dark1))
            print("\tDark 1: " + str(dark2), end="\n\n")

        # Equality will be defined if these two metrics are passed.
        if sameness > 0.95 and 0.95 < dark_ratio < 1.05:
            return True
        else:
            return False

    # Checks if the inner section of the image is the same.
    def __same_inner(self, image1: Image, image2: Image, show=None) -> bool:
        # Cropping borders.
        crop1 = ImageOps.crop(image1, border=55)
        crop2 = ImageOps.crop(image2, border=55)

        if self.__are_equal(crop1, crop2, show):
            return True

        return False

    # Chekcs if the outer section of the image is the same.
    def __same_outer(self, image1: Image, image2: Image, show=None) -> bool:
        crop1 = self.__remove_center(image1)
        crop2 = self.__remove_center(image2)

        if self.__are_equal(crop1, crop2, show):
            return True

        return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Transformation Functions
    # ---------------------------------------------------------------------------------------------------------------- #

    def __row_col_transformation(self, image1: Image, image2: Image, image3: Image) -> list:
        transformation = []

        transformation.append(self.__image_transformation(image1, image2))
        transformation.append(self.__image_transformation(image2, image3))

        return transformation

    def __image_transformation(self, image1: Image, image2: Image) -> np.array:
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
        # Identifies if figure is increasing/decreasing.
        if dark2 > 1.2 * dark1 or dark2 < 0.8 * dark1:
            transformation[1] = 1

        return transformation

    def __image_comparator(self, image1: Image, image2: Image) -> list:
        transformation = []

        transformation.append(ImageChops.difference(image1, image2))  # Differences
        transformation.append(ImageChops.logical_or(image1, image2))  # Similarities

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
                    counter += float(np.abs(el1) + np.abs(el2))

        return counter

    def __print_transformation_list(self, tr1: list, tr2: list) -> None:
        array1 = tr1[0]
        array2 = tr1[1]
        array3 = tr2[0]
        array4 = tr2[1]

        for i in range(0, len(array1)):
            print("\t '{0}'  '{1}' \t|\t '{2}'  '{3}'".format(array1[i], array2[i], array3[i], array4[i], align='^',
                                                              width='10'))

    # ---------------------------------------------------------------------------------------------------------------- #
    # Helper Functions
    # ---------------------------------------------------------------------------------------------------------------- #

    # Adds images together.
    def __add_images(self, image1: Image, image2: Image) -> Image:
        if self.__are_equal(image1, image2):
            return image1
        else:
            return ImageChops.logical_and(image1, image2)

    # Returns the number of white and dark pixels in the image.
    def __pixel_count(self, image: Image) -> tuple:
        histogram_array = image.histogram()
        white = histogram_array[-1]
        dark = histogram_array[0]

        return float(dark), float(white)

    # Returns an image with a whitened center.
    def __remove_center(self, image: Image) -> Image:

        # Makes a copy of the image to prevent changes to the original.
        copy = image.copy()

        # Map of all pixels.
        pixels = copy.load()

        # Middle of image.
        w = int(copy.size[0] / 2)
        h = int(copy.size[1] / 2)

        # Center off-set.
        off = 38

        # Change black center pixels to white.
        for i in range(w - off, w + off):
            for j in range(h - off, h + off):
                if pixels[i, j] == 0:
                    pixels[i, j] = 255

        return copy

    # Returns an image with a whitened border.
    def __remove_border(self, image: Image) -> Image:
        crop = ImageOps.crop(image, border=55)

        return crop

    # Checks if the images in the list are all unique.
    def __unique_images(self, images: list) -> bool:
        comp1 = self.__are_equal(images[0], images[1])
        comp2 = self.__are_equal(images[0], images[2])
        comp3 = self.__are_equal(images[1], images[2])

        if not comp1 and not comp2 and not comp3:
            return True

        return False

    # Checks if images have the same inner image.
    def __unique_inner(self, image1: Image, image2: Image, image3: Image):
        in1 = self.__remove_border(image1)
        in2 = self.__remove_border(image2)
        in3 = self.__remove_border(image3)

        in_list = [in1, in2, in3]

        return self.__unique_images(in_list)

    # Checks if images have the same outer image.
    def __unique_outer(self, image1: Image, image2: Image, image3: Image):
        in1 = self.__remove_center(image1)
        in2 = self.__remove_center(image2)
        in3 = self.__remove_center(image3)

        in_list = [in1, in2, in3]

        return self.__unique_images(in_list)
