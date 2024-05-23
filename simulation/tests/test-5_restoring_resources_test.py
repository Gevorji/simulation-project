from map import Map
from worldacts import ResourceRestoring, RandomLocationObjectSpawner
from world_objects import Grass, Herbivore
from simulationlogger import Logger
from configparser import ConfigParser

_map = Map(10, 10)

configs = ConfigParser()
configs.read('testconfigs.ini')


logger = Logger()


spawners = {
    Herbivore: RandomLocationObjectSpawner(_map, configs, Herbivore),
    Grass: RandomLocationObjectSpawner(_map, configs, Grass)
}

def clean_map(_map: Map):
    for cell in _map.field_iterator(return_contents=False):
        cell.pop()

testresamount = [
    {
        Grass: 2,
        Herbivore: 1
    },
    {
        Grass: 5,
        Herbivore: 3
    },
    {
        Grass: 4,
        Herbivore: 2
    },
    {
        Grass: 0,
        Herbivore: 0
    },

]

wacts = [
    ResourceRestoring(Grass, 4, spawners[Grass], logger, _map),
    ResourceRestoring(Herbivore, 2, spawners[Herbivore], logger, _map)
]


if __name__ == '__main__':
    for num, test_case in enumerate(testresamount):
        logger.start_turn_session()
        print(f'Test {num}\n')
        for obj in test_case:
            spawner = spawners[obj]
            nobjs = test_case[obj]
            for n in range(nobjs):
                spawner.spawn()
        print(f'Before: {_map.get_objs_numbers()}\n')
        for wact in wacts:
            wact.execute()
        print(f'After: {_map.get_objs_numbers()}\n')
        clean_map(_map)
        logger.close_turn_session()



