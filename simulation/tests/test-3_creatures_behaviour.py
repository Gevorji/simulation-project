'''
TEST CASES DESCRIPTION
PREDATOR
1) Predator walks to a Herbi and hits him. Also rocks located on map
2) Predtor has movement speed of 2, he walks to a Herbi.
3) Predator sees Herbi to which there is no path. Predator wanders.
4) Predator sees 2 Herbis that are both equally close to him. He should choose one and make a movement.
5) Predator is trapped inside rocks. Should yield None on make_move call.

HERBIVORE
1) Herbi walks to Grass and eats it.
2) Herbi sees a grass but there is also Predator around in distance that triggers Herbi runaway case. Herbi should have
available cells to run away to.
3) Herbi sees a grass that is surrounded by rocks (no path to it). Herbi wanders.
4) Herbi is trapped inside rocks. Should yield None on make_move call.
5) Herbi has move speed 2 and walks to grass to eat it.
'''

from world_objects import *
from renderer import ConsoleRenderer
from map import Map
from worldacts import Handler

rocks_location = [
    (5, 2), (6, 1), (7, 2), (6, 3),
    (0, 5), (1, 6), (2, 7)
]

layout_mappings = {Herbivore: 'H', Predator: 'P', Rock: 'X', Grass: 'GR', type(None): ''}

creatures = {
    'Predator1': Predator(1, 1, 1, 4, 'male'),
    'Predator2': Predator(1, 1, 2, 4, 'male'),
    'Herbivore1': Herbivore(1, 1, 4, 'male'),
    'Herbivore2': Herbivore(1, 1, 4, 'male'),
    'Herbivore3': Herbivore(1, 2, 4, 'male'),
    'Grass1': Grass(1, 2)
}

handler = Handler()


class Test:

    def __init__(self, _id, objs_pos: dict, targeted, nturns, _env: Map = None):
        self.targeted = targeted
        self.creatures_pos = objs_pos
        self.nturns = nturns
        self.id = _id
        if not _env:
            _env = Map(10, 10)
            for coords in rocks_location:
                _env[coords].put(Rock())

        self._env = _env
        self.targets_decisions = []
        self.renderer = ConsoleRenderer(self._env, layout_mappings=layout_mappings)

        for creature in objs_pos:
            self._env[objs_pos[creature]].put(creature)

    def run(self, *, show_start_state=False, show_end_state=False):
        print('=' * 50 + '\n' + f'Test {self.id}' + '\n')
        if show_start_state:
            self.show_state()

        for i in range(self.nturns):
            acts = []
            for act in self.targeted.make_move(self._env.field_iterator(return_contents=False)):
                acts.append(act)
                if act:
                    cell = self._env[self.targeted.get_rel_position()]
                    handler.handle(cell, act, self._env)()
            self.targets_decisions.append(acts)

        logged_turns = ' '.join(f'(turn {n}): {turns}' for n, turns in enumerate(self.targets_decisions)).strip()
        print(f'ACTIONS TAKEN BY {type(self.targeted).__name__}: {logged_turns}')

        if show_end_state:
            self.show_state()

        self.clean_up_env()

    def clean_up_env(self):
        for cell in self._env.field_iterator(return_contents=False):
            cont = cell.content
            if isinstance(cont, (Herbivore, Predator, Grass)):
                cell.pop()

    def show_state(self):
        self.renderer.render()
        state_disp = self.renderer.display()
        print('START STATE: \n' + state_disp + '\n')


tests = [
    Test('1P', objs_pos={creatures['Predator1']: (4, 4), creatures['Herbivore1']: (7, 7)},
         targeted=creatures['Predator1'], nturns=6),
    Test('2P', objs_pos={creatures['Predator2']: (4, 4), creatures['Herbivore1']: (7, 7)},
         targeted=creatures['Predator2'], nturns=6),
    Test('3P', objs_pos={creatures['Predator1']: (4, 4), creatures['Herbivore1']: (6, 2)},
         targeted=creatures['Predator1'], nturns=3),
    Test('4P', objs_pos={
        creatures['Predator1']: (4, 4), creatures['Herbivore1']: (7, 7), creatures['Herbivore2']: (1, 1)
    },
         targeted=creatures['Predator1'], nturns=6),
    Test('5P', objs_pos={
        creatures['Predator1']: (6, 2)
    },
         targeted=creatures['Predator1'], nturns=3),

    Test('1H', objs_pos={
        creatures['Herbivore1']: (0, 6),
        creatures['Grass1']: (1, 5)
    },
         targeted=creatures['Herbivore1'], nturns=10),

    Test('2H', objs_pos={
        creatures['Herbivore1']: (4, 4),
        creatures['Grass1']: (6, 0),
        creatures['Predator1']: (3, 3)
    },
         targeted=creatures['Herbivore1'], nturns=10),

    Test('3H', objs_pos={
        creatures['Herbivore1']: (4, 4),
        creatures['Grass1']: (6, 2),
    },
         targeted=creatures['Herbivore1'], nturns=3),

    Test('4H', objs_pos={
        creatures['Herbivore1']: (6, 2),
        creatures['Grass1']: (4, 4),
    },
         targeted=creatures['Herbivore1'], nturns=3),

    Test('5H', objs_pos={
        creatures['Herbivore3']: (0, 6),
        creatures['Grass1']: (1, 5)
    },
         targeted=creatures['Herbivore3'], nturns=6),
]

if __name__ == '__main__':
    for test in tests:
        test.run(show_start_state=True)
