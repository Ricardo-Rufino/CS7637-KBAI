import numpy as np

from Frame3 import Frame3
from FigureMatrix import FigureMatrix


class Solver3x3:
    def __init__(self, problem, size_dictionary):
        self.answer = -30
        self.problem = problem
        self.size_dictionary = size_dictionary
        self.guess = np.ones(8)*1000000

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

        print("\n" + problem.name, end="\n")
        print("")
        print("Figures:")
        # Organizing frames for all figures in the problem set from each object dictionary found in RavenFigure class.
        for figure in self.figure_keys:
            raven_object = self.raven_obj_figures[figure]           # RavenObject dictionary for a given figure.
            raven_object_keys = list(raven_object.keys())           # Keys for RavenFigure's Objects dictionary.
            list.sort(raven_object_keys)
            raven_object_keys.reverse()

            frames = []
            number = 1
            for key in raven_object_keys:
                frame = Frame3(number, figure, key, raven_object[key].attributes)
                frame.show()
                frames.append(frame)
                number += 1

            Frame3.reset_coordinate()

            # Reversing list so it displays frames from inside out.
            # frames.reverse()
            self.list_figure.append(frames)

        print("")
        print("Answers:")
        # Organizing frames for all potential answers from each object dictionary found in RavenFigure class.
        for figure in self.answer_keys:
            raven_object = self.raven_obj_answers[figure]           # RavenObject dictionary for a given figure.
            raven_object_keys = list(raven_object.keys())           # Keys for RavenFigure's Objects dictionary.
            list.sort(raven_object_keys)
            raven_object_keys.reverse()

            frames = []
            number = 1
            for key in raven_object_keys:
                frame = Frame3(number, figure, key, raven_object[key].attributes)
                frame.show()
                frames.append(frame)
                number += 1

            Frame3.reset_coordinate()

            # Reversing list so it displays frames from inside out.
            # frames.reverse()
            self.list_answers.append(frames)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                          Creating FigureMatrices                                             #
        # ------------------------------------------------------------------------------------------------------------ #
        figure_matrix_fig = []
        figure_matrix_ans = []
        for frames in self.list_figure:
            figure_matrix_fig.append(self.figure_matrix_creator(frames))
        for frames in self.list_answers:
            figure_matrix_ans.append(self.figure_matrix_creator(frames))

        # ------------------------------------------------------------------------------------------------------------ #
        #                            Creating Transformation Matrices and Selecting Answer                             #
        # ------------------------------------------------------------------------------------------------------------ #

        # Used to gathered known data.
        figure11 = figure_matrix_fig[0]                             # Row 1: 1st figure.
        figure12 = figure_matrix_fig[1]                             # Row 1: 2nd horizontal figure.
        figure13 = figure_matrix_fig[2]                             # Row 1: 3rd horizontal figure.
        figure21 = figure_matrix_fig[3]                             # Col 1: 2nd vertical figure.
        figure31 = figure_matrix_fig[6]                             # Col 1: 3rd vertical figure.

        # Partial information needed to find the answer.
        figure32 = figure_matrix_fig[7]                             # Row 3: 2nd horizontal figure.
        figure23 = figure_matrix_fig[5]                             # Col 3: 2nd vertical figure.

        # Transformation Matrices of known figures.
        tr_h1 = self.transformation(figure11, figure12)             # 1st horizontal transformation matrix.
        tr_h2 = self.transformation(figure12, figure13)             # 2nd horizontal transformation matrix.
        tr_v1 = self.transformation(figure11, figure21)             # 1st vertical transformation matrix.
        tr_v2 = self.transformation(figure21, figure31)             # 2nd vertical transformation matrix.

        tr_h = [tr_h1, tr_h2]
        tr_v = [tr_v1, tr_v2]

        # Transformation Matrices used to find the answer.
        tr_h3 = self.transformation(figure31, figure32)
        tr_v3 = self.transformation(figure13, figure23)

        an_h = [tr_h3]
        an_v = [tr_v3]

        # print("\nTransformation Matrices:")
        # print(tr_h1, end="\n\n")
        # print(tr_h2, end="\n\n")
        # print(tr_v1, end="\n\n")
        # print(tr_v2, end="\n\n")
        #
        # print("\nPartial Answer Matrices:")
        # print(tr_h3, end="\n\n")
        # print(tr_v3, end="\n\n")

        # ------------------------------------------------------------------------------------------------------------ #
        #                                        Searching for the Answer                                              #
        # ------------------------------------------------------------------------------------------------------------ #

        self.answer_selector(tr_h, tr_v, an_h, an_v, figure32, figure23, figure_matrix_ans)

        if self.answer < 0:
            self.answer = self.best_guess()


    def best_guess(self):
        result = np.where(self.guess == np.amin(self.guess))
        return result[0][0] + 1

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Helper Methods                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

    # Creates figure matrix for a given figure in the raven's problem.
    # @frame_list       (list<Frame3>)      list containing the frames of the given figure.
    # @return           (FigureMatrix)      matrix representation of the figure.
    def figure_matrix_creator(self, frame_list):
        matrix = FigureMatrix()

        for figure in frame_list:
            matrix.add(figure)

        matrix.show()

        return matrix

    # Compares two matrices for differences and returns a "transformation" matrix that details the differences between
    # the two matrices.
    # @mfm1:        (FigureMatrix)      first matrix to compare.
    # @mfm2:        (FigureMatrix)      second matrix to compare.
    # @return:      (2D List)           "transformation" matrix.
    def transformation(self, fm1, fm2):
        transformation_matrix = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]

        matrix1 = fm1.matrix
        matrix2 = fm2.matrix

        for row in range(0, 3):
            for col in range(0, 3):

                # Transformation array used to keep track of changes between frames.
                tr_array = np.zeros((12, 1))

                for list in range(0, len(matrix1[row][col])):
                    if matrix2[row][col] is None:
                        break
                    else:
                        try:
                            first = matrix1[row][col][list].get_values()
                            second = matrix2[row][col][list].get_values()

                            for i in range(0, len(tr_array)-1):

                                # # Comparing frame elements.
                                # if first[i] != second[i] and i != 1 and i != 3 and i != 4 and i != 6 & i != 9:
                                #     tr_array[i] += 1

                                # Comparing width or height.
                                if i == 1 or i == 4:
                                    if first[i] == "n/a" and second[i] == "n/a":
                                        continue

                                    if first[i] == "n/a":
                                        size1 = self.size_dictionary[first[3]]
                                    else:
                                        size1 = self.size_dictionary[first[i]]

                                    if second[i] == "n/a":
                                        size2 = self.size_dictionary[second[3]]
                                    else:
                                        size2 = self.size_dictionary[second[i]]

                                    if size1 > size2:
                                        tr_array[i] -= 1
                                    elif size1 < size2:
                                        tr_array[i] += 1

                                # Comparing shapes.
                                elif i == 2:
                                    # Making expection for rectangle and square.
                                    if first[i] == "square" and second[i] == "rectangle":
                                        continue
                                    elif first[i] == "rectangle" and second[i] == "square":
                                        continue
                                    else:
                                        if first[i] != second[i]:
                                            tr_array[i] += 1

                                # Comparing sizes.
                                elif i == 3:
                                    if first[i] == "n/a" or second[i] == "n/a":
                                        continue

                                    size1 = self.size_dictionary[first[i]]
                                    size2 = self.size_dictionary[second[i]]

                                    if size1 > size2:
                                        tr_array[i] -= 1
                                    elif size1 < size2:
                                        tr_array[i] += 1

                                # Comparing how many figures the object is inside.
                                elif i == 6:
                                    inside1 = first[i].split(",")
                                    inside2 = second[i].split(",")

                                    if inside1[0] == "n/a" and inside2[0] != "n/a":
                                        tr_array[i] += 1
                                    elif inside1[0] != "n/a" and inside2[0] == "n/a":
                                        tr_array[i] += 1
                                    elif len(inside1) != len(inside2):
                                        tr_array[i] += 1

                                # Comparing frame angle changes.
                                elif i == 9:
                                    first_angle = int(first[i])
                                    second_angle = int(second[i])
                                    tr_array[i] = np.absolute(first_angle - second_angle)

                                # Comparing frames.
                                else:
                                    if first[i] != second[i]:
                                        tr_array[i] += 1

                        except:
                            pass

                        "**********************************************************************************************"
                        "                           NEED TO IMPLEMENT COORDINATE COMPARISON                            "
                        "**********************************************************************************************"

                    # Last element of transformation array details increases/decreases in objects in figures.
                    tr_array[-1] = len(matrix2[row][col])/len(matrix1[row][col])

                    # Adding transformation array into transformation matrix.
                    transformation_matrix[row][col] = tr_array

        return transformation_matrix

    # Selects the answer to the raven's problems by utilizing the tranformation matrices found from the first row and
    # first column of the problem.
    # @tr_h:        (list<Numpy.Matrix>)        transformation matrices of the first row of the problem.
    # @tr_v:        (list<Numpy.Matrix>)        transformation matrices of the first column of the problem.
    # @an_h:        (list<Numpy.Matrix>)        partial transformation list of last row of the problem.
    # @an_v:        (list<Numpy.Matrix>)        partial transformation list of last column of the prolbem.
    def answer_selector(self, tr_h, tr_v, an_h, an_v, figure32, figure23, an_list):
        for i in range(0, len(an_list)):
            ans_matrix = an_list[i]

            tr_h4 = self.transformation(figure32, ans_matrix)
            tr_v4 = self.transformation(figure23, ans_matrix)

            an_h.append(tr_h4)
            an_v.append(tr_v4)

            # print("\nPotential Answer " + str(i+1) + ":")
            # print(an_h, end="\n\n")
            # print(an_v)

            comp1 = self.transformation_comparator(tr_h, an_h)
            comp2 = self.transformation_comparator(tr_v, an_v)

            if comp1 == 0 and comp2 == 0:
                self.answer = i + 1
                break
            else:
                an_h.pop(-1)
                an_v.pop(-1)
                self.guess[i] = comp1 + comp2

    # Helper method that compares lists of transformation matrices.
    # @tr_list1:    (List<2D List>)     first list.
    # @tr_list2:    (List<2D List>)     second list.
    # @return:      (boolean)           true if lists are the same; false if they're not.
    def transformation_comparator(self, tr_list1, tr_list2):
        counter = 0

        for i in range(0, 2):
            tr1 = tr_list1[i]
            tr2 = tr_list2[i]

            for row in range(0, 3):
                for col in range(0, 3):
                    array1 = tr1[row][col]
                    array2 = tr2[row][col]

                    if len(array1) == 0 and len(array2) == 0:
                        continue
                    elif len(array1) == 0 or len(array2) == 0:
                        counter += 1000
                    else:
                        for k in range(0, len(array1)):
                            if array1[k] != array2[k]:
                                # Weight for difference in fill.
                                if k == 0:
                                    counter += 100
                                # Weight for difference in shapes.
                                if k == 2:
                                    counter += 100
                                # Weight for difference in amount of objects.
                                if k == 11:
                                    counter += 1000
                                else:
                                    counter += 1

        return counter
