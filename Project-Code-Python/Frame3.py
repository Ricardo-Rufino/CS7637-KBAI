import numpy as np

class Frame3:
    # Static variables.
    row = 2
    col = 2

    max_above = 0
    max_left = 0



    # Constructor of class.
    # @id:          (character)     id of frame (i.e. 'a').
    # @attributes:  (dictionary)    contains attributes of the figure (i.e. size, fill, etc.).
    def __init__(self, number, figure, id, attributes):
        self.number = number

        self.figure = figure
        self.id = str(id)
        self.attributes = attributes

        # Attributes corresponding to "physical" characteristics of figure.
        self.fill = "n/a"
        self.height = "n/a"
        self.shape = "n/a"
        self.size = "n/a"
        self.width = "n/a"

        # Attributes corresponding to figure's relative position.
        self.above = "n/a"
        self.inside = "n/a"
        self.left_of = "n/a"
        self.overlaps = "n/a"
        self.angle = "0"

        # Default coordinates; assuming 3x3 figure position matrix.
        self.coordinate = "2,2"

        # All possible keys that attributes dictionary may use.
        self.keys = ["fill", "height", "shape", "size", "width",
                     "above", "inside", "left_of", "overlaps",
                     "angle"]

        # Generating frame's values.
        self.frame_creator()

    # Generates the values of the figure's frame values.
    def frame_creator(self):
        for key in self.keys:
            try:
                value = self.attributes[key]

                if key == "fill":
                    self.fill = value
                elif key == "height":
                    self.height = value
                elif key == "shape":
                    self.shape = value
                elif key == "size":
                    self.size = value
                elif key == "width":
                    self.width = value

                elif key == "above":
                    self.above = value
                elif key == "inside":
                    self.inside = value
                elif key == "left-of":
                    self.left_of = value
                elif key == "overlaps":
                    self.overlaps = value
                elif key == "angle":
                    self.angle = value
            except:
                pass

        # Default coordinate values assuming 3x3 figure position matrix.
        x = 2   # Default x-value of coordinate.
        y = 2   # Default y-value of coordinate.

        "**************************************************************************************************************"
        "                                              NEEDS COMPLETION                                                "
        "**************************************************************************************************************"

        # Number of objects above this.object.
        if self.above == "n/a":
            a = 0
        else:
            a = len(self.above.split(","))

        # Number of objects to the right of this.object.
        if self.left_of == "n/a":
            l = 0
        else:
            l = len(self.left_of.split(","))

        if a > Frame3.max_above:                                    # Move up a row.
            Frame3.max_above = a
            Frame3.row -= 1
        if l > Frame3.max_left:                                     # Move left a column.
            Frame3.max_left = l
            Frame3.col -= 1

        x = Frame3.row
        y = Frame3.col

        # if self.left_of != "n/a":
        #     hor_pos = len(self.left_of.split(","))
        #
        #     if hor_pos < 4:
        #         x = 1
        #     elif hor_pos < 7:
        #         x = 0
        #     else:
        #         x = 2
        #
        # if self.above != "n/a":
        #     ver_pos = len(self.above.split(","))
        #
        #     if ver_pos < 4:
        #         y = 1
        #     elif ver_pos < 7:
        #         y = 0
        #     else:
        #         y = 2

        self.coordinate = str(x) + "," + str(y)

    # Returns list of strings with each element containing the value of the figure's attributes.
    # @return:      (list<string>)      values of figure's attributes.
    def get_values(self):
        return [self.fill, self.height, self.shape, self.size, self.width,
                self.above, self.inside, self.left_of, self.overlaps, self.angle,
                self.coordinate]

    # Returns list representation of coordinate.
    # @return:  (list<int>)     first element is x-coordinate, second element in y-coordinate.
    def get_coordinate(self):
        coordinates = self.coordinate.split(",")

        x = int(coordinates[0])
        y = int(coordinates[1])

        return [x, y]

    # Prints all attributes of the figure's frame.
    def show(self):
        print("Figure: %s, Num: %s, ID: %s, Fill: %s, Height: %s, Shape: %s, Size: %s, Width: %s, "
              "Above: %s, Inside: %s, Left-Of: %s, Overlaps: %s, Angle: %s, "
              "Coordinate: %s" %
              (self.figure, self.number, self.id,
               self.fill, self.height, self.shape, self.size, self.width,
               self.above, self.inside, self.left_of, self.overlaps, self.angle,
               self.coordinate))

    @staticmethod
    def reset_coordinate():
        Frame3.row = 2
        Frame3.col = 2

        Frame3.max_above = 0
        Frame3.max_left = 0


