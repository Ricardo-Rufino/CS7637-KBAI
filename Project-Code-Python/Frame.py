import numpy as np

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