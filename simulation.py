from world_objects import *
from map import Map
from renderer import ConsoleRenderer as Renderer
import random

# standard world properties
# TODO: parameters should be loaded from ini file, user should be able to set his own one-run parameters as
#  commandline args or with input as the initial step after simulation has been launched
STANDARD_FIELD_SZ = (10, 10)
STANDARD_PREDATORS_NUMBER = 5
STANDARD_HERBIVORES_NUMBER = 5
STANDARD_ROCKS_NUMBER = 20
STANDARD_GRASS_NUMBER = 30
RANDOMIZE_CREATURES_NUMBER = False
USR_RAND_BOUNDARIES_FOR_CREATURES = ()
USR_RAND_BOUNDARIES_FOR_ROCKS = ()
USR_RAND_BOUNDARIES_FOR_GRASS = ()



class Simulation:

    def __init__(self):
        self.map = Map(*STANDARD_FIELD_SZ)

    def start(self): pass

    def run(self): pass

    def pause(self): pass

    def populate_world(self):
        _map = self.map
        cells_number = _map.width*_map.length
        obj_howmuch = {}
        rand_creatures_num_boundaries = (USR_RAND_BOUNDARIES_FOR_CREATURES
                                      or (cells_number//20 or 1, cells_number//5 or 1))
        rand_rocks_num_boundaries = (USR_RAND_BOUNDARIES_FOR_ROCKS
                                      or (cells_number//8 or 1, cells_number//3 or 1))
        rand_grass_num_boundaries = (USR_RAND_BOUNDARIES_FOR_GRASS
                                      or (cells_number//8 or 1, cells_number//3 or 1))
        obj_howmuch[Predator] = STANDARD_PREDATORS_NUMBER
        obj_howmuch[Herbivore] = STANDARD_HERBIVORES_NUMBER
        obj_howmuch[Rock] = STANDARD_ROCKS_NUMBER
        obj_howmuch[Grass] = STANDARD_GRASS_NUMBER
        if RANDOMIZE_CREATURES_NUMBER or USR_RAND_BOUNDARIES_FOR_CREATURES:
            obj_howmuch[Predator] = random.randint(*rand_creatures_num_boundaries)
            obj_howmuch[Herbivore] = random.randint(*rand_creatures_num_boundaries)
            obj_howmuch[Rock] = random.randint(*rand_rocks_num_boundaries)
            obj_howmuch[Grass] = random.randint(*rand_grass_num_boundaries)
        for obj, number in obj_howmuch.items():
            for i in range(number):
                while True:
                    x, y = random.randint(0, _map.width), random.randint(0, _map.length)
                    try:
                        _map[x, y].put(obj)
                        break
                    except AssertionError:
                        continue


    def next_turn(self): pass

