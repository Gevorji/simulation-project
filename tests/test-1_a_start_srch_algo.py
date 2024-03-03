import sys
from map import Map
from algorithms import a_star_search, graph_from_grid
from world_objects import *
from renderer import ConsoleRenderer

sys.path.insert(1, r'../')

Obstacle = Rock
obstacles_testcases = [
    {'start_point': (0, 0), 'end_point': (5, 5), 'obstacles_config': ((4, 6), (4, 5), (5, 4), (6, 3), (7, 3))},
    {'start_point': (0, 0), 'end_point': (5, 5),
     'obstacles_config': ((4, 6), (4, 5), (5, 4), (6, 3), (7, 3), (5, 6), (6, 5))},
    {'start_point': (0, 0), 'end_point': (2, 2), 'obstacles_config': ((1, 1), (2, 1))}
]


class WalkTracePrinter(ConsoleRenderer):

    def __init__(self, field):
        super().__init__(field, layout_mappings={Obstacle: '\U0001f92a', type(None): ' '})

    def mark_route(self, root):
        for point in root:
            self.field[point].put('Х')

    def print_field(self):
        print(self.display())


def obstacles_passing():
    class FieldWithObstacles(Map):
        def __init__(self, obstacles_config):
            super().__init__(10, 10)
            for x, y in obstacles_config:
                self[x, y].put(Obstacle())

    def additional_constraints(node):
        return False if field[node].content else True

    shower = WalkTracePrinter(Map(10, 10))

    for testcase in obstacles_testcases:
        field = FieldWithObstacles(testcase['obstacles_config'])
        graph = graph_from_grid(field.length, field.width)
        shower.rend_obj = field
        shower.render()
        route = a_star_search(testcase['start_point'],
                              testcase['end_point'],
                              graph,
                              additional_constraints_to_successors=additional_constraints)
        if route:
            shower.mark_route(route)
        else: 'Root wasnt found'
        shower.print_field()

if __name__ == '__main__':
    obstacles_passing()
