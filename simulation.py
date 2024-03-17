from world_objects import *
from world_objects.actions import Actions
from map import Map
from renderer import ConsoleRenderer as Renderer
import random

# initial world properties
# TODO: parameters should be loaded from ini file, user should be able to set his own one-run parameters as
#  commandline args or with input as the initial step after simulation has been launched

default_gen_parameters = dict(
                              STANDARD_FIELD_SZ = (10, 10),
                              STANDARD_PREDATORS_NUMBER = 5,
                              STANDARD_HERBIVORES_NUMBER = 5,
                              STANDARD_ROCKS_NUMBER = 20,
                              STANDARD_GRASS_NUMBER = 30,
                              STANDARD_CREATURE_VELOCITY = 1,
                              RANDOMIZE_CREATURES_NUMBER = False,
                              USR_RAND_BOUNDARIES_FOR_CREATURES = (),
                              USR_RAND_BOUNDARIES_FOR_GRASS = (),
                              USR_CREATURE_VELOCITY = None
                              )

class Simulation:

    def __init__(self):
        pass

    def start(self):
        pass

    def run(self):
        pass

    def pause(self):
        pass

    def next_turn(self):
        pass






