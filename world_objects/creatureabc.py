from abc import abstractmethod

try:
    from .entityabc import Entity
except ImportError:
    from entityabc import Entity


class Creature(Entity):
    def __init__(self, health_points, move_speed, environment):
        self.environment = environment
        self.health_points = health_points
        self.move_speed = move_speed

    @abstractmethod
    def make_move(self): pass

    @property
    def visible_area(self): pass # a collection of cells that creature can see

    def take_damage(self, damage):
        self.health_points -= damage

    def wander(self): pass

if __name__ == '__main__': pass