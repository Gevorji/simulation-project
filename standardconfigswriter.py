import configparser

standard_configs = configparser.ConfigParser()

standard_configs['DEFAULT'] = {
    'field.width': '10',
    'field.length': '10',
    'nHerbivore': '5',
    'nPredator': '5',
    'nRock': '20',
    'nGrass': '30',
    'frspeed': '1',
    'RandomizeMap': 'false'
}

standard_configs['RAND.OBJ_NUMBERS_RATIOS'] = {
    'HerbivoreNumber': '0.05, 0.2',
    'PredatorNumber': '0.05, 0.2',
    'RockNumber': '0.125, 0.33',
    'GrassNumber': '0.125, 0.33'
}

standard_configs['RAND.HERBIVORE_PARAMS'] = {
    'health_pointsBoundaries': '3, 10',
    'movement_speedBoundaries': '1,3'
}

standard_configs['RAND.PREDATOR_PARAMS'] = {
    'health_pointsBoundaries': '3, 10',
    'movement_speedBoundaries': '1, 3',
    'attack_damageBoundaries': '1, 2'
}

