from typing import Protocol


class HasFieldIterator(Protocol):
    def field_iterator(self): ...


class BaseRectangleFieldRenderer:
    
    def __init__(self, rend_obj: HasFieldIterator, layout_mappings):
        self.layout_mappings = layout_mappings
        self.rend_obj = rend_obj
        self.field = [[None]*self.rend_obj.width for row in range(self.rend_obj.length)]
        self.layout = self.render()
        
    def render(self):
        for obj in self.rend_obj.field_iterator(): # walks through field and updates self field state
            self.layout                            # expects renderable object to have a method field_iterator.
                                                   # A field iterator returns objects
                                                   # that renderable objects contains in a strict order: from left upper
                                                   # corner to the bottom right corner

    def field_iterator(self):
        for row_num in range(len(self.field)):
            for col_num in range(row_num):
                yield self.field


    def display(self): pass # returns self.view


    