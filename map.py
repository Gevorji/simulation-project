from collections import OrderedDict


class Map:

    def __init__(self, length, width):
        self.width = width
        self.length = length
        self.field = OrderedDict(((row, column), Cell(row, column)) for column in range(width) for row in range(length))

    def __getitem__(self, item):
        return self.field[item]

    def field_iterator(self, from_point=None, to_point=None, *, return_contents=True, rectangle_area=False):
        fwidth, flength = self.width, self.length
        from_point = from_point or 0, 0
        to_point = to_point or fwidth, flength
        width_range = range(from_point[0], to_point[0]) if rectangle_area \
            else (x for y in range(to_point[1]) for x in range(fwidth) if x)
        for x in range(fwidth): pass


class Cell:

    def __init__(self, x, y, content=None):
        self.content = content
        self.y = y
        self.x = x

    def put(self, what):
        self.content = what

    def pop(self):
        obj = self.content
        self.content = None
        return obj

    def __str__(self):
        return f'A cell with {self.content} and {self.x, self.y} coordinates'