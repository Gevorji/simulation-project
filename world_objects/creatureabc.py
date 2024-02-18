try:
    from .entityabc import Entity
except ImportError:
    from entityabc import Entity


class Creature(Entity):
    def __init__(self, health_points, move_speed):
        self.health_points = health_points
        self.move_speed = move_speed

    def make_move(self): pass

    @property
    def visible_area(self): pass # a collection of cells that creature can see

    def take_damage(self): pass

    def wander(self): pass