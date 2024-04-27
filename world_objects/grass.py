from .entityabc import Entity


class Grass(Entity):

    def __init__(self, health_points, hp_restore):
        super().__init__(health_points)
        self.hp_restore = hp_restore

    def consume(self):
        self.take_damage(1)
        return self.hp_restore
