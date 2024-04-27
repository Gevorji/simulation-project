from .entityabc import Entity


class Rock(Entity):

    def __init__(self, health_points):
        super().__init__(health_points)
