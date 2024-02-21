from map import Map

class BaseRectangleFieldRenderer(Map):

    def __init__(self, rend_obj, layout_mappings):
        super().__init__(rend_obj.length, rend_obj.width)
        # an assertion for all keys of layout mappings to be type class instances
        self.layout_mappings = layout_mappings
        self.rend_obj = rend_obj
        
    def render(self):
        for cell, obj in zip(self.field_iterator(), self.rend_obj.field_iterator()): # walks through field and updates self field state
            mapped_obj = self.layout_mappings[type(obj)]
            cell.put(mapped_obj)                                   # expects renderable object to have a method field_iterator.
                                                   # A field iterator returns objects
                                                   # that renderable objects contains in a strict order: from left upper
                                                   # corner to the bottom right corner



