from map import Map


class BaseRectangleFieldRenderer(Map):

    def __init__(self, rend_obj, *, layout_mappings: dict):
        super().__init__(rend_obj.length, rend_obj.width)
        # an assertion for all keys of layout mappings to be type class instances
        self.layout_mappings = layout_mappings
        self.rend_obj = rend_obj

    def render(self):
        for cell, obj in zip(self.field_iterator(return_contents=False),
                             self.rend_obj.field_iterator()):  # walks through field and updates self field state
            mapped_obj = self.layout_mappings[type(obj)]
            cell.pop()
            cell.put(mapped_obj)


class ConsoleRenderer(BaseRectangleFieldRenderer):

    def __init__(self, rend_obj, *, layout_mappings: dict, enumerate_axis=False):
        super().__init__(rend_obj, layout_mappings=layout_mappings)
        self.enumerate_axis = enumerate_axis

    def display(self):
        enumerate_axis = self.enumerate_axis
        padding = 2
        cell_width = max(map(len, self.layout_mappings.values()))
        vert_border = '|'
        enum_y_cell_width = 2
        enum_x = ' ' * enum_y_cell_width + ' '.join(str(num).center(cell_width + padding) for num in range(self.width)) \
            if enumerate_axis else ''
        enum_y = (str(num).ljust(enum_y_cell_width, ' ') for num in range(self.length)) \
            if enumerate_axis else ('' for num in range(self.length))
        horiz_aligning_cavity = ' '.ljust(enum_y_cell_width, ' ') if enumerate_axis else ''
        horiz_border = (horiz_aligning_cavity + '+'
                        + '+'.rjust(cell_width + padding + len(vert_border) * 2 - 1, '-') * self.width)

        cells_content = [[self.field[x, y].content.center(cell_width + padding) for x in range(self.width)]
                         for y in range(self.length)]

        rows = [f'{next(enum_y)}' + vert_border + vert_border.join(row_of_cells)
                + vert_border for row_of_cells in cells_content]

        return enum_x + '\n' + horiz_border + '\n' + ('\n' + horiz_border + '\n').join(rows) + '\n' + horiz_border


class EdgelessConsoleRenderer(ConsoleRenderer):

    def display(self):
        row_enum = (str(y) if self.enumerate_axis else '' for y in range(self.length))
        col_enum = (str(x) if self.enumerate_axis else '' for x in range(self.width))
        rows = [next(row_enum) + ' '.join(self.field[x, y].content for x in range(self.width)) for y in range(self.length)]

        return (' ' + ' '.join(col_enum) + '\n' if self.enumerate_axis else '') + ('\n'*2).join(rows)

if __name__ == '__main__':
    renderer = ConsoleRenderer(Map(5, 5), layout_mappings={type(None): 'Empty'})
    renderer.render()
    print(renderer.display(enumerate_axis=False))
