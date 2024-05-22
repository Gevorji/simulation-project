# Test integrates such components as simulation orchestrating class (Simulation), all creatures, all world actions.
# The goal here is to make sure that a core mechanics of the whole project work fine together.
# We control turns processing manually with 'n' input during the pause.
# This test is a step that wraps up the main goals of project as they were put up at the begging of developing.

import os
import sys

sys.path.insert(0, 'C:\\Users\\User\\Desktop\\simulation-project')

import simulation

from simulation import Simulation, INP_PARAMETERS_PATTERNS, InpParametersParser, apply_inputted_parameters
from configparser import ConfigParser


configs = ConfigParser()
configs.read('testconfigs.ini')

Spawner = simulation.wacts.ObjectSpawner
spawner = Spawner(None, configs)

pparser = InpParametersParser(INP_PARAMETERS_PATTERNS, '=')

test_input = [
    'mapsz=5*5, nHerbivore=1 nPredator=1 nRock=20',
    'mapsz=20*20',
    ''
]

test_map_configuration = [
    {simulation.wacts.Herbivore: ((0, 2),), simulation.wacts.Predator: ((1, 4),),
     simulation.wacts.Rock: ((1, 3), (1, 2), (2, 2), (2, 0), (3, 4), (3, 5))}
]

def apply_configuration_on_map(_map, number):
    spawner._world_map = _map
    conf_test = test_map_configuration[number]
    for obj_t in conf_test:
        spawner.set_obj_type(obj_t)
        for coords in conf_test[obj_t]:
            spawner.target_cell = _map[coords]
            spawner.spawn()


if __name__ == '__main__':
    test_choice = int(input('test number: '))-1
    map_conf_choice = input('map configuration choice: ')
    applyparams = pparser.parse(test_input[test_choice])
    apply_inputted_parameters(applyparams, configs)

    sim = Simulation(configs)

    if map_conf_choice:
        sim._init_actions.pop(0)
        apply_configuration_on_map(sim._world_map, int(map_conf_choice))

    sim.start()




