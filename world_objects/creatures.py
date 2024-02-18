try:
    from .creatureabc import Creature
except ImportError:
    from creatureabc import Creature

class Predator(Creature): pass


class Herbivore(Creature):

    def __init__(self, health_points, movement_speed):
        super().__init__(health_points, movement_speed)


if __name__ == '__main__':
    h = Herbivore(10, 10)
    print(h.__dict__)
