try:
    from abc import ABC
except ImportError: pass


class Entity(ABC):

    def __init__(self, health_points):
        self.health_points = health_points
        self.is_dead = False

    def take_damage(self, damage):
        self.health_points -= damage
        if self.health_points <= 0:
            self.is_dead = True


