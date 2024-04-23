import os
import os.path
import sys
import re
import time
from dataclasses import dataclass
import configparser

import simulationlogger
from map import Map
from renderer import ConsoleRenderer as Renderer
import worldacts as wacts
from lib import keyboard

# initial world properties
# TODO: parameters should be loaded from ini file, user should be able to set his own one-run parameters as
#  commandline args or with input as the initial step after simulation has been launched

default_gen_parameters = dict(
    STANDARD_FIELD_SZ=(10, 10),
    STANDARD_PREDATORS_NUMBER=5,
    STANDARD_HERBIVORES_NUMBER=5,
    STANDARD_ROCKS_NUMBER=20,
    STANDARD_GRASS_NUMBER=30,
    STANDARD_CREATURE_VELOCITY=1,
    RANDOMIZE_CREATURES_NUMBER=False,
    USR_RAND_BOUNDARIES_FOR_CREATURES=(),
    USR_RAND_BOUNDARIES_FOR_GRASS=(),
    USR_CREATURE_VELOCITY=None
)

INP_PARAMETERS_PATTERNS = [
    '(mapsz)=(\\d+[*]\\d+)',
    '(nHerbivore|nPredator|nGrass|nRock)=(\\d+)',
    '(r)',
    '(frspeed)=(\\d+)',
    '((Herbivore|Predator|Grass)[.](ms|hp|visr|ad|heal))=(\\d+)'
]

INP_PARAM_DELIM = '='

INP_PARAM_CONFIG_PARAM_MAP = {
    'mpsize': 'FIELD'
}


class Simulation:

    pause_options_patterns = [
        re.compile('c'), re.compile('show(\\d+)t'), re.compile('n')
    ]

    def __init__(self, params: configparser.ConfigParser):
        self.params = params
        _map = self._world_map = Map(params.getint('DEFAULT', 'field.width', ), params.getint('DEFAULT', 'field.length', ))
        self.frspeed = params.getint('DEFAULT', 'frspeed')
        action_handler = wacts.Handler()
        self.logger = logger = simulationlogger.Logger()
        objects_buffer = []
        self._init_actions = [
            wacts.PopulateWorld(params, _map)
        ]
        self._turn_actions = [
            wacts.MakeEachObjDoMove(action_handler, logger,_map),
            wacts.ResourceRestoring(wacts.Grass, 0,
                                    wacts.RandomLocationObjectSpawner(_map, params, wacts.Grass), logger, _map)
        ]
        objects_lmappings = {
            wacts.Herbivore: 'H',
            wacts.Predator: 'P',
            wacts.Grass: 'GR',
            wacts.Rock: 'X',
            type(None): ' '
        }
        self.renderer = Renderer(_map, layout_mappings=objects_lmappings)
        self.turn_count: int = 0
        self.last_input = None
        self.is_paused = False

    def start(self):
        for wact in self._init_actions:
            wact.execute()

        self._turn_actions[1].min_resource_limit = 0.3*self._world_map.get_objs_numbers()[wacts.Grass]

        self.renderer.render()
        self.change_frame(self.renderer.display(), '([Нажмите пробел для старта]')
        keyboard.wait('space')

        def on_pause(*args):
            self.is_paused = True

        keyboard.on_press_key('space', on_pause)

        self.run()

    @staticmethod
    def run_with_fixed_frequency(runner_func):

        def execute_controller(self):
            while True:
                if self.is_paused:
                    self.pause()
                start = time.perf_counter()
                runner_func(self)
                end = time.perf_counter()
                lag = 1/self.frspeed - (end-start)
                if lag > 0:
                    time.sleep(lag)

        return execute_controller

    @run_with_fixed_frequency
    def run(self):
        self.next_turn()
        self.change_frame(self.renderer.display(),
                          f'Счетчик ходов: {self.turn_count}')

    def pause(self):
        options_patterns = self.pause_options_patterns
        self.change_frame(self.renderer.display(), input_request='Введите_команду> ')
        while True:
            inp = self.last_input
            try:
                match = next(filter(None, (p.match(inp) for p in options_patterns)))
                break
            except StopIteration:
                self.change_frame(self.renderer.display(),
                                  'Пожалуйста, введите правильную опцию',
                                  input_request='Введите_команду> ')

        if match.re == options_patterns[0]:
            self.is_paused = False
            return

        if match.re == options_patterns[1]:
            nturn = match.group(1)
            log = self.logger.get_turn_logging(nturn)
            self.change_frame(self.renderer.display(), log, input_request='Введите команду>')

        if match.re == options_patterns[2]:
            return

    def next_turn(self):
        self.logger.start_turn_session()
        for wact in self._turn_actions:
            wact.execute()
        self.logger.close_turn_session()
        self.renderer.render()
        self.turn_count += 1

    def change_frame(self, *components, input_request: None | str = None):
        os.system('cls')
        frame = '\n'.join(components)
        print(frame)
        if input_request:
            self.last_input = input(input_request)



@dataclass
class Parameter:

    re: re.Pattern
    name: str
    value: str


class InpParametersParser:

    def __init__(self, patterns: list | tuple, delim: str):
        self.delim = delim
        import re
        self.patterns = [re.compile(p) for p in patterns]
        self._matches = None

    def parse(self, line):
        delim = self.delim
        params = []
        param_strs = line.split()
        print(param_strs)
        for param_str in param_strs:
            for pattern in self.patterns:
                m = pattern.match(param_str)
                if m:
                    groups = m.groups()
                    if delim not in param_str:
                        name, val = groups[0], True
                    else:
                        name, val = groups[0], groups[-1]
                    params.append(Parameter(m.re, name, val))
                    break
            else:
                raise ParameterInputError(f'"{param_str}" - неправильно заданная опция')
        return params

    def add_pattern(self, pattern, cfgs):
        self.patterns.append(re.compile(pattern))


class ParameterInputError(Exception):
    pass

def apply_inputted_parameters(params: list, configs):
    for param in params:
        if param.re.pattern == INP_PARAMETERS_PATTERNS[0]:
            section = configs['DEFAULT']
            width, length = param.value.split('*')
            section['field.width'] = width
            section['field.length'] = length
        if param.re.pattern == INP_PARAMETERS_PATTERNS[1]:
            section = configs['DEFAULT']
            section[param.name] = param.value
        if param.re.pattern == INP_PARAMETERS_PATTERNS[2]:
            section = configs['DEFAULT']
            section['RandomizeMap'] = str(param.value)
        if param.re.pattern == INP_PARAMETERS_PATTERNS[3]:
            section = configs['DEFAULT']
            section[param.name] = param.value
        if param.re.pattern == INP_PARAMETERS_PATTERNS[4]:
            obj_name, attr = param.name.split('.')
            section = configs[f'{obj_name.upper()}']
            attr = {
                'ms': 'move_speed',
                'ad': 'attack_damage',
                'visr': 'vis_rad',
                'hp': 'health_points',
                'heal': ''  # TODO: put full attr name here
            }[attr]
            if attr not in section:
                raise ParameterInputError(f'{obj_name} не имеет параметра {attr}')
            section[attr] = param.value

if __name__ == '__main__':

    param_parser = InpParametersParser(INP_PARAMETERS_PATTERNS)
    configs = configparser.ConfigParser()
    configs.read('configs.ini')
    while True:
        inp = input('Enter stuff: ')
        # inp = 'Herbivore.heal=4'
        try:
            parsed = param_parser.parse(inp)
            print([f'{param.name} set to {param.value}' for param in parsed])
            apply_inputted_parameters(parsed, configs)
        except ParameterInputError as e:
            print(e)
        else:
            break



    # here it is necessary to check whether config file exists
    # if it doesn't exist, we write it with standardconfigswriter.py

