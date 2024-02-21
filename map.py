from collections import OrderedDict


class Map:

    def __init__(self, length, width):
        self.width = width
        self.length = length
        self.field = OrderedDict(((row, column), Cell(row, column)) for column in range(width) for row in range(length))

    def __getitem__(self, item):
        return self.field[item]

    def field_iterator(self, *, return_contents=True):
        for cell in self.field.values():
            yield cell.content if return_contents else cell


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