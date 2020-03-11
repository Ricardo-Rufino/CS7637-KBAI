import numpy as np

class Frame3:

    # Constructor of class.
    # @id:          (character)     id of frame (i.e. 'a').
    # @attributes:  (dictionary)    contains attributes of the figure (i.e. size, fill, etc.).
    def __init__(self, id, attributes):
        self.id = str(id)
        self.attributes = attributes

        # Attributes corresponding to "physical" characteristics of figure.
        self.fill = ""
        self.height = ""
        self.shape = ""
        self.size = ""
        self.width = ""

        # Attributes corresponding to figure's relative position.
        self.above = ""
        self.inside = ""
        self.left_of = ""
        self.overlaps = ""
        self.angle = "0"

        # Default coordinates; assuming 3x3 figure position matrix.
        self.coordinate = "1,1"

        # All possible keys that attributes dictionary may use.
        self.keys = ["fill", "height", "shape", "size", "width",
                     "above", "inside", "left_of", "overlaps",
                     "angle"]

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
                    self.size = value

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
        x = 0   # Default x-value of coordinate.
        y = 0   # Default y-value of coordinate.

        "**************************************************************************************************************"
        "                                              NEEDS COMPLETION                                                "
        "**************************************************************************************************************"
        # Setting up coordinate value for frame.
        if self.left_of != "":
            pass
        if self.above != "":
            pass

    # Returns list of strings with each element containing the value of the figure's attributes.
    # @return:      (list<string>)      values of figure's attributes.
    def list_representation(self):
        return [self.id, self.fill, self.height, self.shape, self.shape, self.size, self.width,
                self.above, self.inside, self.left_of, self.overlaps, self.angle,
                self.coordinate]

    # Returns list representation of coordinate.
    # @return:  (list<int>)     first element is x-coordinate, second element in y-coordinate.
    def get_coordinate(self):
        coordinates = self.coordinate.split(",")

        x = int(coordinates[0])
        y = int(coordinates[1])

        return [x, y]

