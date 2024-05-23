#  For configs bootstraping
#  Import this module then call main()


import configparser

standard_configs = configparser.ConfigParser()

standard_configs['DEFAULT'] = {
    'field.width': '10',
    'field.length': '10',
    'nHerbivore': '',
    'nPredator': '',
    'nRock': '',
    'nGrass': '',
    'frspeed': '1',
    'RandomizeMap': 'false',
    'axis_enumeration': 'false'
}

standard_configs['RAND.OBJ_NUMBERS_RATIOS'] = {
    'HerbivoreNumber': '0.05, 0.1',
    'PredatorNumber': '0.02, 0.05',
    'RockNumber': '0.05, 0.15',
    'GrassNumber': '0.1, 0.15'
}

standard_configs['GRASS'] = {
    'health_points': '1',
    'hp_restore': ''
}

standard_configs['HERBIVORE'] = {
    'health_points': '',
    'move_speed': '',
    'vis_radius': '5',
    'sex': ''
}

standard_configs['PREDATOR'] = {
    'attack_damage': '',
    'health_points': '',
    'move_speed': '',
    'vis_radius': '5',
    'sex': ''
}

standard_configs['ROCK'] = {
    'health_points': ''
}

standard_configs['RAND.GRASS_PARAMS'] = {
    'health_points': '1, 3',
    'hp_restore': '1, 3'
}

standard_configs['RAND.HERBIVORE_PARAMS'] = {
    'health_points': '3,6',
    'move_speed': '1,2',
    'vis_radius': '5,5',
    'sex': '1,2'
}

standard_configs['RAND.PREDATOR_PARAMS'] = {
    'attack_damage': '1,2',
    'health_points': '2,4',
    'move_speed': '1,2',
    'vis_radius': '5,5',
    'sex': '1,2'
}

standard_configs['RAND.ROCK_PARAMS'] = {
    'health_points': '2,6',
}

standard_configs['CONSOLE_LAYOUT_SYMBOLS'] = {
    'NoneType': '26AB',
    'Herbivore': '1f999',
    'Predator': '1F43A',
    'Grass': '1F966',
    'Rock': '1F5FB'
}


def main():
    with open('configs.ini', 'w') as f:
        standard_configs.write(f)
