
from configparser import ConfigParser

import map
from simulation import INP_PARAMETERS_PATTERNS, InpParametersParser, apply_inputted_parameters, ParameterInputError
from worldacts import PopulateWorld
from map import Map
from renderer import ConsoleRenderer
from world_objects import *

configs = ConfigParser()
configs.read('testconfigs.ini')

param_parser = InpParametersParser(INP_PARAMETERS_PATTERNS, '=')

_map = Map(10, 10)
objs_buffer = []

renderer = ConsoleRenderer(_map, layout_mappings={Herbivore: 'H', Predator: 'P', Rock: 'X',
                                                  Grass: 'GR', type(None): ' '})


def clean_map(_map: map.Map):
    for cell in _map.field_iterator(return_contents=False):
        cell.pop()


def get_objs_params(_map: map.Map):
    objs_params = []
    for cont in _map.field_iterator():
        if cont is not None:
            objs_params.append(f'{cont.__class__.__name__}: {repr(cont.__dict__)}')
    return '\n'.join(objs_params)


tested_wacts = [
    PopulateWorld(configs, _map)
]

test_param_inputs = [
    '',
    'r',
    'nHerbivore=3 nPredator=2 nGrass=7 nRock=10',
    'Herbivore.hp=3 Herbivore.ms=4 Predator.ms=1 Predator.ad=1',
    'nHorbovore=4',
    'Herbivore.heal=4'
]

if __name__ == '__main__':
    for test_num, test_input in enumerate(test_param_inputs):
        try:
            parsed = param_parser.parse(test_input)
            if parsed:
                apply_inputted_parameters(parsed, configs)
        except ParameterInputError as e:
            print(f'Test {test_num}: {e}')
        else:
            objs_buffer.clear()
            for wact in tested_wacts:
                wact.execute()
            renderer.render()
            print(f'Test {test_num}:\n{renderer.display()}\nObjects: {get_objs_params(_map)}\n \
Objects numbers: {_map.get_objs_numbers()}')
            clean_map(_map)
            configs.read('testconfigs.ini')


