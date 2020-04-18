import numpy as np
from Frame3 import Frame3
from PIL import Image, ImageChops, ImageOps


class VisualSolver:
    problem_num = 0  # Problem number.
    problem_inv = 9  # Problem to investigate.

    report = np.zeros((14, 24), dtype=int)

    def __init__(self, problem, correctness: dict):
        VisualSolver.problem_num += 1

        self.answer = -100
        self.problem = problem
        self.debug = VisualSolver.problem_num == VisualSolver.problem_inv

        # Dictionary that is used for answer tie-breakers.
        self.correctness = correctness

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

        # Collecting RavenFigure and RavenObject objects for all figures in the problem set.
        for i in self.figure_keys:

            # Collecting images from the RPM.
            raven_figure = self.problem.figures[i]  # RavenFigure object.
            image_path = raven_figure.visualFilename  # Filepath of figure.
            image = Image.open(image_path)  # Image of the figure.
            image = image.convert("1")  # Image converted into bi-level image.

            self.images_problem.append(image)

        # Collection images from the potential answers.
        for i in self.answer_keys:

            # Collecting problem images.
            raven_figure = self.problem.figures[i]  # RavenFigure object.
            image_path = raven_figure.visualFilename  # Filepath of figure.
            image = Image.open(image_path)  # Image of the figure.
            image = image.convert("1")  # Image converted into bi-level image.

            self.images_answers.append(image)

        tuple(self.images_problem)
        tuple(self.images_answers)

        if self.debug:
            print("All figure loaded properly, analysis will now start...")

        self.get_answer()

        if self.debug:
            print("\nAnalysis has concluded.---------------------------", end="\n\n")

        # if VisualSolver.problem_num == 24:
        #     print("Performance Review: ")
        #     self.__print_report()

    # ---------------------------------------------------------------------------------------------------------------- #
    # Main Solver Function
    # ---------------------------------------------------------------------------------------------------------------- #

    def get_answer(self) -> None:
        (a, b, c, d, e, f, g, h) = self.images_problem

        if self.debug:
            ans = self.images_answers[7]

            diff1 = self.__percent_pixel_difference(ans, b)
            diff2 = self.__percent_pixel_difference(ans, d)
            print(diff1)
            print(diff2)
            print(round(diff2/diff1))

        # List of all functions.
        func_list = [self.__horizontal_addition,
                     self.__same_diagonal,
                     self.__same_inner_outer,
                     self.__same_horizontal_outer,
                     self.__sameness_comparator,
                     self.__guess_by_uniqueness,
                     self.__problem_d8,
                     self.__problem_d9,
                     self.__problem_d12,
                     self.__reverse_addition,
                     self.__edge_addition,
                     self.__similarity_addition,
                     self.__similarity_retention,
                     self.__halves_addition]

        # List that contains all the answers calculated from the functions.
        answer_list = np.zeros((len(func_list), 1))

        report_j = VisualSolver.problem_num-1

        for i in range(len(func_list)):
            func = func_list[i]

            if func():
                answer_list[i] = self.answer
                # VisualSolver.report[i, report_j] = self.answer

        # Analysing answers.
        candidates = []
        for i in range(answer_list.size):
            if answer_list[i] != 0:
                attributes = [answer_list[i], self.correctness[i]]
                candidates.append(attributes)

        if len(candidates) > 1:
            correct_ans = candidates[0][0]
            confidence = candidates[0][1]
            for candidate in candidates:
                if candidate[0] != correct_ans:
                    if candidate[1] > confidence:
                        correct_ans = candidate[0]
                        confidence = candidate[1]

            self.answer = correct_ans

        # if VisualSolver.problem_num == 24:
        #     self.__print_report()

        # if self.debug:
        #     self.__print_report()

        # if self.debug:
        #     for i in self.images_problem:
        #         image1 = self.__remove_top(i)
        #         image1.show()
        # --------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------------------- #
    # Specific Case Functions for Problem Set D
    # ---------------------------------------------------------------------------------------------------------------- #

    # Function that checks if the horizontal images are the same.
    # Helps with the following problems:
    # D-01
    # E-01
    # E-02
    # E-03?
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
    # Helps with the following problems:
    # D-05
    # E-11
    def __sameness_comparator(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Comparing sameness of first two rows.
        ab_sim = ImageChops.logical_or(a, b)
        bc_sim = ImageChops.logical_or(b, c)

        de_sim = ImageChops.logical_or(d, e)
        ef_sim = ImageChops.logical_or(e, f)

        row1 = self.__are_equal(ab_sim, bc_sim)
        row2 = self.__are_equal(de_sim, ef_sim)

        # Comparing sameness of first column.
        ad_sim = ImageChops.logical_or(a, d)
        dg_sim = ImageChops.logical_or(d, g)

        be_sim = ImageChops.logical_or(b, e)
        eh_sim = ImageChops.logical_or(e, h)

        col1 = self.__are_equal(ad_sim, dg_sim)
        col2 = self.__are_equal(be_sim, eh_sim)

        # Checking for unique inner shapes in each column.
        unique_first_col = self.__unique_inner(a, d, g)
        unique_second_col = self.__unique_inner(b, e, h)

        # Check for solution.
        if row1 and col1 and unique_first_col:
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

    # Function created to solve problem D-08. Checks if fill type is shifting one unit to the right.
    def __problem_d8(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checking that right-shift fill type is present.
        a_change = self.__color_change(a)
        e_change = self.__color_change(e)

        b_change = self.__color_change(b)
        f_change = self.__color_change(f)
        g_change = self.__color_change(g)

        c_change = self.__color_change(c)
        d_change = self.__color_change(d)
        h_change = self.__color_change(h)

        ae_same_fill = a_change == e_change
        bfg_same_fill = b_change == f_change == g_change
        cdh_same_fill = c_change == d_change == h_change

        fill_right_shift = ae_same_fill and bfg_same_fill and cdh_same_fill

        # Checking that each shifting fill type is a different shape.
        ae_same = self.__are_equal(a, e)
        bfg_unique = self.__unique_images([b, f, g])
        cdh_unique = self.__unique_images([c, d, h])

        unique_right_shift = not ae_same and bfg_unique and cdh_unique

        if fill_right_shift and unique_right_shift:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]
                i_change = self.__color_change(ans)

                aei_change = a_change == e_change == i_change
                aei_unique = self.__unique_images([a, e, ans])

                if aei_change and aei_unique:
                    self.answer = i + 1
                    return True

        return False

    # Function designed to solve problem D-09. Checks that similarities are shifted to the right by one. Also checks
    # that images with equal similarities are unique.
    def __problem_d9(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # How many pixels to crop from the figures border.
        border = 40

        # Checking that similarities are shifted to the right by one unit.
        ae_sim = self.__remove_border(ImageChops.logical_or(a, e), border=border)

        bf_sim = self.__remove_border(ImageChops.logical_or(b, f), border=border)
        fg_sim = self.__remove_border(ImageChops.logical_or(f, g), border=border)
        second_sim = self.__are_equal(bf_sim, fg_sim)

        cd_sim = self.__remove_border(ImageChops.logical_or(c, d), border=border)
        dh_sim = self.__remove_border(ImageChops.logical_or(d, h), border=border)
        third_sim = self.__are_equal(cd_sim, dh_sim)

        # Checking for uniqueness among images that contain similarities.
        bfg_unique = self.__unique_images([b, f, g])
        cdh_unique = self.__unique_images([c, d, h])

        # Looking for potential answer.
        if second_sim and third_sim and bfg_unique and cdh_unique:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                ei_sim = self.__remove_border(ImageChops.logical_or(e, ans), border=border)

                first_sim = self.__are_equal(ae_sim, ei_sim)
                aei_unique = self.__unique_images([a, e, ans])

                if first_sim and aei_unique:
                    self.answer = i + 1
                    return True

        return False

    # Function created to solver problem D-12. Checks that figure incrementation occurs in as the figures shift 2 units
    # to the right.
    def __problem_d12(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checks that images are incrementing by one.
        af_increment = self.__percent_pixel_difference(a, f)
        eg_increment = self.__percent_pixel_difference(e, g)

        if not self.__similar_change(af_increment, eg_increment):
            return False

        # Checks that images are incrementing by two.
        ah_increment = self.__percent_pixel_difference(a, h)
        ec_increment = self.__percent_pixel_difference(e, c)

        if not self.__similar_change(ah_increment, ec_increment):
            return False

        for i in range(len(self.images_answers)):
            ans = self.images_answers[i]

            ib_increment = self.__percent_pixel_difference(ans, b)
            id_increment = self.__percent_pixel_difference(ans, d)

            if self.__similar_change(ib_increment, af_increment) and self.__similar_change(id_increment, ah_increment):
                self.answer = i + 1
                return True

        return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Specific Case Functions for Problem Set E
    # ---------------------------------------------------------------------------------------------------------------- #

    # Function that checks if right-left and bottom-up addition is present.
    # Helps with the following problems:
    # E-05
    def __reverse_addition(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checkin if right-left addition of the first two rows exists.
        bc = self.__add_images(b, c)
        ef = self.__add_images(e, f)

        row1 = self.__are_equal(bc, a)
        row2 = self.__are_equal(ef, d)

        # Checkin if bottom-up addition of the first two columns exists.
        dg = self.__add_images(d, g)
        eh = self.__add_images(e, h)

        col1 = self.__are_equal(dg, a)
        col2 = self.__are_equal(eh, b)

        # Looking for potential answer.
        if row1 and row2 and col1 and col2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                hi = self.__add_images(h, ans)
                fi = self.__add_images(f, ans)

                row3 = self.__are_equal(hi, g)
                col3 = self.__are_equal(fi, c)

                if row3 and col3:
                    self.answer = i + 1
                    return True

        return False

    # Function that checks if edge addition is present. That is, if the addition of the edges results in the center
    # image of the row/column.
    # Helps with the following problems:
    # E-06
    def __edge_addition(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checkin if edge addition of the first two rows exists.
        ac = self.__add_images(a, c)
        df = self.__add_images(d, f)

        row1 = self.__are_equal(ac, b)
        row2 = self.__are_equal(df, e)

        # Checkin if edge addition of the first two columns exists.
        ag = self.__add_images(a, g)
        bh = self.__add_images(b, h)

        col1 = self.__are_equal(ag, d)
        col2 = self.__are_equal(bh, e)

        # Looking for potential answer.
        if row1 and row2 and col1 and col2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                gi = self.__add_images(g, ans)
                ci = self.__add_images(c, ans)

                row3 = self.__are_equal(gi, h)
                col3 = self.__are_equal(ci, f)

                if row3 and col3:
                    self.answer = i + 1
                    return True

        return False

    # Function that adds the first two images in a row/column and finds the similarity between them as well. It adds
    # the similarity to the third image in the row/column and checks if its equal to the addition of the first two.
    # Helps with the following problems:
    # E-01
    # E-02
    # E-05
    # E-06
    # E-07
    # E-08
    # Rating = 10
    def __similarity_addition(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        drt = [0.90, 1.1]

        # Checkin if edge addition of the first two rows exists.
        ab = self.__add_images(a, b)
        de = self.__add_images(d, e)

        ab_sim = ImageChops.logical_or(a, b)
        de_sim = ImageChops.logical_or(d, e)

        c_plus_sim = self.__add_images(c, ab_sim)
        f_plus_sim = self.__add_images(f, de_sim)

        row1 = self.__are_equal(c_plus_sim, ab, dark_ratio_tolerance=drt)
        row2 = self.__are_equal(f_plus_sim, de, dark_ratio_tolerance=drt)

        # Checkin if edge addition of the first two columns exists.
        ad = self.__add_images(a, d)
        be = self.__add_images(b, e)

        ad_sim = ImageChops.logical_or(a, d)
        be_sim = ImageChops.logical_or(b, e)

        g_plus_sim = self.__add_images(g, ad_sim)
        h_plus_sim = self.__add_images(h, be_sim)

        col1 = self.__are_equal(g_plus_sim, ad, dark_ratio_tolerance=drt)
        col2 = self.__are_equal(h_plus_sim, be, dark_ratio_tolerance=drt)

        # Looking for potential answer.
        if row1 and row2 and col1 and col2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                gh = self.__add_images(g, h)
                cf = self.__add_images(c, f)

                gh_sim = ImageChops.logical_or(g, h)
                cf_sim = ImageChops.logical_or(c, f)

                ans_plus_sim1 = self.__add_images(ans, gh_sim)
                ans_plus_sim2 = self.__add_images(ans, cf_sim)

                row3 = self.__are_equal(ans_plus_sim1, gh, dark_ratio_tolerance=drt)
                col3 = self.__are_equal(ans_plus_sim2, cf, dark_ratio_tolerance=drt)

                if row3 and col3:
                    self.answer = i + 1
                    return True

        return False

    # Checks if the similarities between the first two images in the row/columns is the third image.
    # Helps with the following problems:
    # E-10
    # E-11
    # Rating = 1
    def __similarity_retention(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checking similarity in the first two rows.
        ab_sim = ImageChops.logical_or(a, b)
        de_sim = ImageChops.logical_or(d, e)

        row1 = self.__are_equal(ab_sim, c)
        row2 = self.__are_equal(de_sim, f)

        # Check similarity in the first two columns.
        ad_sim = ImageChops.logical_or(a, d)
        be_sim = ImageChops.logical_or(b, e)

        col1 = self.__are_equal(ad_sim, g)
        col2 = self.__are_equal(be_sim, h)

        # Looking for potential answer.
        if row1 and row2 and col1 and col2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                gh_sim = ImageChops.logical_or(g, h)
                cf_sim = ImageChops.logical_or(c, f)

                row3 = self.__are_equal(gh_sim, ans)
                col3 = self.__are_equal(cf_sim, ans)

                if row3 and col3:
                    self.answer = i + 1
                    return True

        return False

    def __halves_addition(self):
        (a, b, c, d, e, f, g, h) = self.images_problem

        # Checking first two row.
        a_top = self.__remove_bottom(a)
        b_bot = self.__remove_top(b)
        c_top = self.__remove_bottom(c)
        c_bot = self.__remove_top(c)

        d_top = self.__remove_bottom(d)
        e_bot = self.__remove_top(e)
        f_top = self.__remove_bottom(f)
        f_bot = self.__remove_top(f)

        row1 = self.__are_equal(a_top, c_top) and self.__are_equal(b_bot, c_bot)
        row2 = self.__are_equal(d_top, f_top) and self.__are_equal(e_bot, f_bot)

        # Checking first two columns.
        a_top = self.__remove_bottom(a)
        d_bot = self.__remove_top(d)
        g_top = self.__remove_bottom(g)
        g_bot = self.__remove_top(g)

        b_top = self.__remove_bottom(b)
        e_bot = self.__remove_top(e)
        h_top = self.__remove_bottom(h)
        h_bot = self.__remove_top(h)

        col1 = self.__are_equal(a_top, g_top) and self.__are_equal(d_bot, g_bot)
        col2 = self.__are_equal(b_top, h_top) and self.__are_equal(e_bot, h_bot)

        # Looking for potential answer.
        if row1 and row2 and col1 and col2:
            for i in range(len(self.images_answers)):
                ans = self.images_answers[i]

                # Analysis of third row.
                g_top = self.__remove_bottom(g)
                h_bot = self.__remove_top(h)
                i_top = self.__remove_bottom(ans)
                i_bot = self.__remove_top(ans)

                # Analysis of third columns.
                c_top = self.__remove_bottom(c)
                f_bot = self.__remove_top(f)

                row3 = self.__are_equal(g_top, i_top) and self.__are_equal(h_bot, i_bot)
                col3 = self.__are_equal(c_top, i_top) and self.__are_equal(f_bot, i_bot)

                if row3 and col3:
                    self.answer = i + 1
                    return True

        return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Functions that Compare Images
    # ---------------------------------------------------------------------------------------------------------------- #

    # Checks if images are the same.
    def __are_equal(self, image1: Image, image2: Image, show=None, dark_ratio_tolerance=None) -> bool:
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
            print("\tDark 2: " + str(dark2), end="\n\n")

        if dark_ratio_tolerance is None:
            dl = 0.95
            du = 1.05
        else:
            dl = dark_ratio_tolerance[0]
            du = dark_ratio_tolerance[1]

        # Equality will be defined if these two metrics are passed.
        if sameness > 0.95 and dl < dark_ratio < du:
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

    # Checks if the outer section of the image is the same.
    def __same_outer(self, image1: Image, image2: Image, show=None) -> bool:
        crop1 = self.__remove_center(image1)
        crop2 = self.__remove_center(image2)

        if self.__are_equal(crop1, crop2, show):
            return True

        return False

    # ---------------------------------------------------------------------------------------------------------------- #
    # Helper Functions
    # ---------------------------------------------------------------------------------------------------------------- #

    # Adds images together.
    def __add_images(self, image1: Image, image2: Image) -> Image:
        if self.__are_equal(image1, image2):
            return image1
        else:
            return ImageChops.logical_and(image1, image2)

    def __add_three_images(self, image1: Image, image2: Image, image3: Image) -> Image:
        first_addition = self.__add_images(image1, image2)
        second_addition = self.__add_images(first_addition, image3)

        return second_addition

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

    def __remove_bottom(self, image: Image) -> Image:

        # Makes a copy of the image to prevent changes to the original.
        copy = image.copy()

        # Map of all pixels.
        pixels = copy.load()

        # With and height.
        w = int(copy.size[0])
        h = int(copy.size[1])

        # Center off-set.
        off = 38

        # Change black center pixels to white.
        for i in range(0, w):
            for j in range(int(h/2), h):
                if pixels[i, j] == 0:
                    pixels[i, j] = 255

        return copy

    def __remove_top(self, image: Image) -> Image:

        # Makes a copy of the image to prevent changes to the original.
        copy = image.copy()

        # Map of all pixels.
        pixels = copy.load()

        # With and height.
        w = int(copy.size[0])
        h = int(copy.size[1])

        # Center off-set.
        off = 38

        # Change black center pixels to white.
        for i in range(0, w):
            for j in range(0, int(h/2)):
                if pixels[i, j] == 0:
                    pixels[i, j] = 255

        return copy

    # Returns an image with a whitened border.
    def __remove_border(self, image: Image, border=None) -> Image:
        if border is None:
            border = 55

        crop = ImageOps.crop(image, border=border)

        return crop

    # Returns true if inner images are the same between the images.
    def __equal_inner(self, image1: Image, image2: Image) -> bool:
        in1 = self.__remove_border(image1)
        in2 = self.__remove_border(image2)

        return self.__are_equal(in1, in2)

    # Returns true if the outer images are the same between the images.
    def __equal_outer(self, image1: Image, image2: Image, image3=None) -> bool:
        out1 = self.__remove_center(image1)
        out2 = self.__remove_center(image2)

        if image3 is not None:
            out3 = self.__remove_center(image3)
            return self.__are_equal(out1, out2) and self.__are_equal(out2, out3)
        else:
            return self.__are_equal(out1, out2)

    # Returns true if the figure is completely filled.
    def __is_filled(self, image: Image) -> bool:
        # Number of times white and black alternate.
        alternate = self.__color_change(image)

        if alternate == 2:
            return True

        return False

    # Return true if the figure is completely unfilled.
    def __is_unfilled(self, image: Image) -> bool:
        # Number of times white and black alternate.
        alternate = self.__color_change(image)

        if alternate == 4:
            return True

        return False

    # Returns true if the figure is partially filled.
    def __is_partially_filled(self, image: Image) -> bool:
        # Number of times white and black alternate.
        alternate = self.__color_change(image)

        if alternate == 6:
            return True

        return False

    def __color_change(self, image: Image) -> int:
        # Map of all pixels.
        pixels = image.load()

        # With and height.
        w = int(image.size[0])
        h = int(image.size[1])

        # Look through the middle of the image and check changes in color.
        i = int(h / 2)              # Middle of the figure (waist).
        color_change = 0            # Counter that checks the amount of color changes.
        for j in range(1, w):
            if pixels[i, j] != pixels[i, j - 1]:
                color_change += 1

        return color_change

    def _plane_exists(self, pixels, col, height) -> bool:
        for row in range(0, height):
            left = pixels[row, col-1]
            right = pixels[row, col+10]
            if pixels[row, col] == pixels[row, col - 1]:
                return False

        return True

    # Checks if the images in the list are all unique.
    def __unique_images(self, images: list) -> bool:
        comp1 = self.__are_equal(images[0], images[1])
        comp2 = self.__are_equal(images[0], images[2])
        comp3 = self.__are_equal(images[1], images[2])

        if not comp1 and not comp2 and not comp3:
            return True

        return False

    def __percent_pixel_difference(self, image1: Image, image2: Image) -> float:
        dark1, white1 = self.__pixel_count(image1)
        dark2, white2 = self.__pixel_count(image2)

        if dark1 == 0 and dark2 == 0:
            return 0

        if dark1 == 0:
            return 99999999
        else:
            return dark2/dark1 - 1

    def __similar_change(self, num1, num2):
        return np.abs(num2-num1) < 0.07

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

    # Prints the performance report of VisualSolver.
    def __print_report(self):
        row, col = VisualSolver.report.shape
        print("Performance Report:")
        for i in range(row):
            for j in range(col):
                if j == 0:
                    print("Solver {0}|".format(str(i+1)), end="\t")
                if j == 12:
                    print("|", end= "\t")
                print(str(VisualSolver.report[i, j]), end="\t\t")
            print()
        print()
