from .entityabc import Entity


class Grass(Entity):

    def __init__(self, health_points, hp_restore):
        self.health_points = health_points
        self.hp_restore = hp_restore

    def consume(self):
        self.health_points -= 1
