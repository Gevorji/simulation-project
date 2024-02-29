from map import Map


class BaseRectangleFieldRenderer(Map):

    def __init__(self, rend_obj, *, layout_mappings: dict):
        super().__init__(rend_obj.length, rend_obj.width)
        # an assertion for all keys of layout mappings to be type class instances
        self.layout_mappings = layout_mappings
        self.rend_obj = rend_obj
        
    def render(self):
        for cell, obj in zip(self.field_iterator(return_contents=False), self.rend_obj.field_iterator()): # walks through field and updates self field state
            mapped_obj = self.layout_mappings[type(obj)]
            cell.put(mapped_obj)                                   # expects renderable object to have a method field_iterator.
                                                   # A field iterator returns objects
                                                   # that renderable objects contains in a strict order: from left upper
                                                   # corner to the bottom right corner
 ren

class ConsoleRenderer(BaseRectangleFieldRenderer):

    def display(self):
        padding = 2
        cell_width = max(map(len, self.layout_mappings.values()))
        vert_border = '|'
        horiz_border = '+' + '+'.rjust(cell_width + padding + len(vert_border)*2-1, '-')*self.width
        cells_content = [[self.field[x, y].content.center(cell_width+padding) for x in range(self.width)]
                         for y in range(self.length)]
        rows = [vert_border+vert_border.join(row_of_cells)+vert_border for row_of_cells in cells_content]
        return horiz_border + '\n' + ('\n'+horiz_border+'\n').join(rows) + '\n' + horiz_border


if __name__ == '__main__':
    renderer = ConsoleRenderer(Map(5,5), {type(None): 'Empty'})
    renderer.render()
    print(renderer.display())

