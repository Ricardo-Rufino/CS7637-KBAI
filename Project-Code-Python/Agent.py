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

            for j in range(0, len(dict)):
                obj = dict[keys[j]]
                frame = self.frameCreator(keys[j], obj.attributes)
                print(figure_keys[i], end=" ")
                print(keys[j], end=" ")
                frame.show()

        return 0

    # Function that creates a frame for a given figure in the raven problem.--------------------------------------------
    def frameCreator(self, id, attributes):

        values = list(attributes.values())  # Casting values to a list.

        # Potential attributes of figure.
        sizeType = ["huge", "very large", "large", "medium", "small"]
        fillType = ["yes", "no"]
        shapType = ["square", "circle", "cross", "plus", "right triangle", "pac-man", "octagon", "diamond", "heart"]

        # Default values of attributes.
        size, fill, shape, angle, inside = "", "", "", "", ""

        for i in values:
            if i in sizeType:
                size = i
            elif i in fillType:
                fill = i
            elif i in shapType:
                shape = i
            elif str.isdigit(i):
                angle = int(i)
            elif str.isalpha(i) and len(i) == 1:
                inside = i

        frame = None

        if angle == "" and inside == "":
            frame = self.Frame(id, shape, fill, size)
        elif angle == "":
            frame = self.Frame(id, shape, fill, size, inside=inside)
        elif inside == "":
            frame = self.Frame(id, shape, fill, size, angle=angle)
        else:
            frame = self.Frame(id, shape, fill, size, angle=angle, inside=inside)

        return frame

    # Function used to compare frames.----------------------------------------------------------------------------------
    def compare(self, a, b):
        return 0

    class Frame:
        levels = 1  # Used to identify the amount of shapes in the frame.

        def __init__(self, id, shape, fill, size, angle=None, inside=None):
            self.id = id
            self.shape = shape
            self.fill = fill
            self.size = size

            if angle is None:
                self.angle = 0
            else:
                self.angle = angle

            if inside is None:
                self.inside = "None"
            else:
                self.inside = inside

        def show(self):
            print("ID: %s, Shape: %s, Fill: %s, Size: %s, Angle: %d, Inside: %s" %
                  (self.id, self.shape, self.fill, self.size, self.angle, self.inside))

        def getID(self):
            return self.id
