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


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

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
                return self.Solve_2x2(problem)
            else:
                return -1
        else:
            return -1

        return 2

    # Method used to solve 2x2 methods.---------------------------------------------------------------------------------
    def Solve_2x2(self, problem):
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
                frame_ds.append(self.FrameCreator(key, dict[key].attributes))

            # Arranging frames into their respective spot on the matrix.
            list_figure.append(frame_ds)

        for i in range(0, len(raven_obj_answers)):
            dict = raven_obj_answers[i]
            keys = list(dict.keys())
            list.sort(keys)

            frame_ds = []
            for key in keys:
                frame_ds.append(self.FrameCreator(key, dict[key].attributes))

            # Arranging frames into their respective spot on the matrix.
            list_answers.append(frame_ds)

        transform = self.FrameComparator(list_figure[0], list_figure[1])
        print("Transformation: ")
        print(transform)

        answer = self.AnswerSelector(list_figure[2], list_answers, transform)
        print("Answer: ")
        print(answer)

        print("Figures:")
        for i in list_figure:
            for j in i:
                j.show()

        print("Answers:")
        for i in list_answers:
            for j in i:
                j.show()

        return answer

    # Function that creates a frame for a given figure in the raven problem.--------------------------------------------
    def FrameCreator(self, id, attributes):

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

        return self.Frame(id, shape, fill, size, angle=angle, inside=inside, alignment=alignment)

    # Function used to compare frames.----------------------------------------------------------------------------------
    def FrameComparator(self, a, b):

        transform = np.zeros((5, 1))

        if (len(a) < 3 and len(b) < 3) and (len(a) == len(b)):

            transform = np.zeros((5, len(a)))               # Transformation array; used to compare frames.

            for j in range(0, len(a)):

                first = a[j].getValues()
                second = b[j].getValues()

                for i in range(0, 5):

                    if first[i] != second[i] and i != 3:
                        transform[i][j] = 1
                    elif i == 3:                            # Special case when dealing with angles.
                        first_angle = int(first[i])
                        second_angle = int(second[i])
                        transform[i][j] = np.absolute(first_angle-second_angle)

        return transform

    def AnswerSelector(self, c, list_answers, transform):

        for i in range(0, len(list_answers)):
            if (len(list_answers[i]) < 3 and len(c) < 3) and len(list_answers[i]) == len(c):
                difference = self.FrameComparator(c, list_answers[i])
                # print(difference)
                if self.AreEqual(difference, transform):
                    return i + 1

        return -1

    # Fucntion used to compare arrays.
    def AreEqual(self, first, second):

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


    class Frame:
        levels = 1  # Used to identify the amount of shapes in the frame.

        def __init__(self, id, shape, fill, size, angle=None, inside=None, alignment=None):
            self.id = id
            self.shape = shape
            self.fill = fill
            self.size = size

            # Default values for angle, inside and alignment.
            if angle is None:
                self.angle = "0"
            else:
                self.angle = angle

            if inside is None:
                self.inside = "None"
            else:
                self.inside = inside

            if alignment is None:
                self.alignment = "center"
            else:
                self.alignment = alignment


        def show(self):
            print("ID: %s, Shape: %s, Fill: %s, Size: %s, Angle: %s, Inside: %s Alignment: %s" %
                  (self.id, self.shape, self.fill, self.size, self.angle, self.inside, self.alignment))

        def getID(self):
            return self.id

        def getValues(self):
            values = np.array([self.shape, self.fill, self.size, self.angle, self.alignment])
            return values
