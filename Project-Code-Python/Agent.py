# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
# from PIL import Image
import numpy as np
from Frame import Frame


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):

        # Dictionary used to map location to coordinate.
        self.position = {
            "center": [0, 0],
            "bottom-right": [1, -1],
            "bottom-left": [-1, -1],
            "top-right": [1, 1],
            "top-left": [-1, 1]
        }

        self.value = {}
        self.counter = 1
        for i in np.arange(-2, 3):
            for j in np.arange(-2, 3):

                key = str(i) + " " + str(j)
                if i == 0 and j == 0:
                    self.value[key] = 0
                else:
                    self.value[key] = self.counter
                    self.counter += 1

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):

        # Creating frames for the problem

        if problem.hasVerbal:
            if problem.problemType == "2x2":
                return self.solve_2x2(problem)
            elif problem.problemType == "3x3":
                return self.solve_3x3(problem)
            else:
                return -10
        else:
            return -1

        return 2

    # Method used to solve 2x2 methods.---------------------------------------------------------------------------------
    def solve_2x2(self, problem):
        # Keys that will be used to access RavenFigure objects from RavensProblem objects.
        figure_keys = ["A", "B", "C"]
        answer_keys = ["1", "2", "3", "4", "5", "6"]

        # Lists that will be used to stored the RavenFigure objects.
        raven_fig_figures = []
        raven_fig_answers = []

        # Lists that will be used to store the RavenObject objects.
        raven_obj_figures = []
        raven_obj_answers = []

        # Lists that contains the frame of the figures and potential answers.
        list_figure = []
        list_answers = []

        # Collecting RavenFigure and RavenObject objects.---------------------------------------------------------------
        for i in range(0, len(figure_keys)):
            # Collecting RavenFigure objects.
            raven_fig_figures.append(problem.figures[figure_keys[i]])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = raven_fig_figures[i].objects
            raven_obj_figures.append(fig_dict)

        for i in range(0, len(answer_keys)):
            # Collecting RavenFigure objects.
            raven_fig_answers.append(problem.figures[answer_keys[i]])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = raven_fig_answers[i].objects
            raven_obj_answers.append(fig_dict)
        # ------------------------------------------------------------------------------------------------------------ #

        for i in range(0, len(raven_obj_figures)):
            dict = raven_obj_figures[i]
            keys = list(dict.keys())
            list.sort(keys)

            frame_ds = []
            for key in keys:
                frame_ds.append(self.frame_creator(key, dict[key].attributes))

            # Arranging frames into their respective spot on the matrix.
            list_figure.append(frame_ds)

        for i in range(0, len(raven_obj_answers)):
            dict = raven_obj_answers[i]
            keys = list(dict.keys())
            list.sort(keys)

            frame_ds = []
            for key in keys:
                frame_ds.append(self.frame_creator(key, dict[key].attributes))

            # Arranging frames into their respective spot on the matrix.
            list_answers.append(frame_ds)

        transform = self.frame_comparator(list_figure[0], list_figure[1])
        # print("Transformation: ")
        # print(transform)

        answer = self.answer_selector(list_figure[2], list_answers, transform)
        # print("Answer: ")
        # print(answer)

        # print("Figures:")
        # for i in list_figure:
        #     for j in i:
        #         j.show()
        #
        # print("Answers:")
        # for i in list_answers:
        #     for j in i:
        #         j.show()

        return answer

    def solve_3x3(self, problem):
        # Keys that will be used to access RavenFigure objects from RavensProblem objects.
        figure_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]
        answer_keys = ["1", "2", "3", "4", "5", "6", "7", "8"]

        # Lists that will be used to stored the RavenFigure objects.
        raven_fig_figures = []
        raven_fig_answers = []

        # Lists that will be used to store the RavenObject objects.
        raven_obj_figures = []
        raven_obj_answers = []

        # Lists that contains the frame of the figures and potential answers.
        list_figure = []
        list_answers = []

        # Collecting RavenFigure and RavenObject objects.---------------------------------------------------------------
        for i in range(0, len(figure_keys)):
            # Collecting RavenFigure objects.
            raven_fig_figures.append(problem.figures[figure_keys[i]])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = raven_fig_figures[i].objects
            raven_obj_figures.append(fig_dict)

        for i in range(0, len(answer_keys)):
            # Collecting RavenFigure objects.
            raven_fig_answers.append(problem.figures[answer_keys[i]])

            # Collecting dictionary that contain RavenObjects.
            fig_dict = raven_fig_answers[i].objects
            raven_obj_answers.append(fig_dict)

        return -30

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Helper Functions                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

    # Function that creates a frame for a given figure in the raven problem.
    # @id:          (character)     id of the frame (i.e. 'a').
    # @attributes:  (dictionary)    maps keys (such as size, filled) to their respective values.
    # @return:      (Frame)         Frame with the corresponding attributes of the figure.
    def frame_creator(self, id, attributes):

        values = list(attributes.values())  # Casting values to a list.

        # Potential attributes of figure.
        sizeType = ["huge", "very large", "large", "medium", "small"]
        fillType = ["yes", "no", "left-half", "right-half", "top-half", "bottom-half"]
        shapType = ["square", "circle", "cross", "plus", "right triangle",
                    "pac-man", "octagon", "diamond", "heart", "pentagon",
                    "triangle", "star"]
        aligType = ["bottom-right", "bottom-left", "top-right", "top-left"]

        # Default values of attributes.
        size, fill, shape = "", "", ""
        angle, inside, alignment = None, None, None

        for i in values:
            if i in sizeType:
                size = i
            elif i in fillType:
                fill = i
            elif i in shapType:
                shape = i
            elif i in aligType:
                alignment = i
            elif str.isdigit(i):
                angle = i
            elif str.isalpha(i) or len(i.split(",")) > 1:
                inside = i

        return Frame(id, shape, fill, size, angle=angle, inside=inside, alignment=alignment)

    # Function used to compare frames.
    # @a:       (matrix)    first matrix.
    # @b:       (matrix)    second matrix.
    # @return:  (matrix)    matrix that details the difference between a and b.
    def frame_comparator(self, a, b):

        transform = np.zeros((6, 1))

        if (len(a) < 3 and len(b) < 3) and (len(a) == len(b)):

            transform = np.zeros((6, len(a)))                       # Transformation array; used to compare frames.

            for j in range(0, len(a)):
                first = a[j].getValues()
                second = b[j].getValues()

                for i in range(0, 5):
                    if first[i] != second[i] and i != 3 and i != 4:
                        transform[i][j] = 1
                    elif i == 3 and first[0] == second[0]:          # Special case when dealing with angles.
                        first_angle = int(first[i])
                        second_angle = int(second[i])
                        transform[i][j] = np.absolute(first_angle-second_angle)
                    elif i == 4:
                        transform[i][j] = self.alignment_hash(first[i], second[i], self.position, self.value)

                transform[5][j] = 0

        else:
            if len(a) > len(b):
                transform = np.zeros((6, len(a)))
            else:
                transform = np.zeros((6, len(b)))

            row, col = transform.shape

            for j in range(0, col):
                transform[5, j] = len(b) - len(a)

        return transform

    def answer_selector(self, c, list_answers, transform):

        for i in range(0, len(list_answers)):
            if (len(list_answers[i]) < 3 and len(c) < 3) and len(list_answers[i]) == len(c):
                difference = self.frame_comparator(c, list_answers[i])
                # print(difference)
                if self.are_equal(difference, transform):
                    return i + 1

        return -1

    # Function used to compare matrices.
    # @first:       (matrix)    first matrix.
    # @second:      (matrix)    second matrix.
    # @return:      (boolean)   true if matrices are the same; false if they're not.
    def are_equal(self, first, second):

        counter = 0

        if (first.size == second.size):
            row, col = first.shape

            for i in range(0, row):
                for j in range(0, col):
                    if first[i][j] != second[i][j]:
                        counter += 1

        if counter == 0:
            return True
        else:
            return False

    # Function used for hashing alignment combinations.
    # @first:       (string)        string corresponding to the initial alignment of the figure.
    # @second:      (string)        string corresponding to the final alignment of the figure.
    # @position:    (dictionary)    maps alignment (string) to a list of two elements (x, y coordinates).
    # @value:       (dictionary)    maps directional vector (string) to a unique number.
    # @return:      (int)           unique number that corresponds to a unique directional vector.
    def alignment_hash(self, first, second, position, value):

        first_pos = position[first]
        second_pos = position[second]

        final_x = second_pos[0] - first_pos[0]
        final_y = second_pos[1] - first_pos[1]

        final_key = str(final_x) + " " + str(final_y)

        return value[final_key]

