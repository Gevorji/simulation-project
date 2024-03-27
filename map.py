from collections import OrderedDict


class Map:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.field = OrderedDict(((x, y), Cell(x, y)) for y in range(length) for x in range(width) )

    def __getitem__(self, item):
        return self.field[item]

    def field_iterator(self, from_point=None, to_point=None, *, return_contents=True):
        fwidth, flength = self.width, self.length
        from_point = from_point or (0, 0)
        to_point = to_point or (fwidth-1, flength-1)
        for y in range(from_point[1], to_point[1]+1):
            for x in range(from_point[0], to_point[0]+1):
                yield self[x, y].content if return_contents else self[x, y]

class Cell:

    def __init__(self, x, y, content=None):
        self.content = content
        self.y = y
        self.x = x

    def put(self, what):
        assert not self.content, f'Attempt to put an object into a cell that already contains {self.content}'
        self.content = what

    def pop(self):
        obj = self.content
        self.content = None
        return obj

    def __str__(self):
        return f'A cell with {self.content} and {self.x, self.y} coordinates'