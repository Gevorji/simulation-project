class BaseRenderer: 
    
    def __init__(self, rend_obj, layout_mappings):
        self.layout_mappings = layout_mappings
        self.rend_obj = rend_obj
        self.view = self.render()
        
    def render(self): pass # walks through field and updates a view
    
    def display(self): pass # returns self.view
    
    
    