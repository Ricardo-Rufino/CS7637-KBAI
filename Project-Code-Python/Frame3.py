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

        # Variable used to construct image matrix.
        self.coordinate = "0,0"

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

        # Setting up coordinate value for frame.
        if self.left_of != "":
            pass
        if self.above != "":
            pass


    def list_representation(self):
        return [self.id, self.fill, self.height, self.shape, self.shape, self.size, self.width,
                self.above, self.inside, self.left_of, self.overlaps, self.angle,
                self.coordinate]

