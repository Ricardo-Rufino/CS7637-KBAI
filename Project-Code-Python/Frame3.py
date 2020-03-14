import numpy as np

class Frame3:

    # Constructor of class.
    # @id:          (character)     id of frame (i.e. 'a').
    # @attributes:  (dictionary)    contains attributes of the figure (i.e. size, fill, etc.).
    def __init__(self, figure, id, attributes):
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
        self.coordinate = "1,1"

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
        x = 1   # Default x-value of coordinate.
        y = 1   # Default y-value of coordinate.

        "**************************************************************************************************************"
        "                                              NEEDS COMPLETION                                                "
        "**************************************************************************************************************"
        # Setting up coordinate value for frame.
        if self.left_of != "n/a":
            pass
        if self.above != "n/a":
            pass

    # Returns list of strings with each element containing the value of the figure's attributes.
    # @return:      (list<string>)      values of figure's attributes.
    def list_representation(self):
        return [self.figure, self.id, self.fill, self.height, self.shape, self.size, self.width,
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
        print("Figure: %s, ID: %s, Fill: %s, Height: %s, Shape: %s, Size: %s, Width: %s, "
              "Above: %s, Inside: %s, Left-Of: %s, Overlaps: %s, Angle: %s, "
              "Coordinate: %s" %
              (self.figure, self.id, self.fill, self.height, self.shape, self.size, self.width,
               self.above, self.inside, self.left_of, self.overlaps, self.angle,
               self.coordinate))

