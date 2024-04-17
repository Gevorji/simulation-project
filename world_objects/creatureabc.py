import random
from abc import abstractmethod
from algorithms import a_star_search, graph_from_grid, evaluate_direct_distance
try:
    from .entityabc import Entity
except ImportError:
    from entityabc import Entity


class Creature(Entity):
    _temp_data_keys = ['_rel_pos',
                       '_area',
                       '_area_grid',
                       '_area_size',
                       '_abs_pos']

    def __init__(self, health_points, move_speed, vis_radius, sex, _id=None):  # sex field is reserved for breeding mechanics
        self.sex = sex
        self.vis_radius = vis_radius
        self.health_points = health_points
        self.move_speed = move_speed
        self.is_alive = True
        self._memory = dict(_path=None, _area_graph=None)
        self._id = _id

    @abstractmethod
    def make_move(self, area):
        area = tuple(area)
        self._memory['_area'] = area
        self.get_area_grid()

    def take_damage(self, damage):
        self.health_points -= damage
        if self.health_points <= 0:
            self.is_alive = False

    def get_nearby_cells(self):
        grid = self._memory['_area_grid']
        cur_pos = self.get_rel_position()
        nearby_cells = []
        for x, y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            try:
                to_cell = grid[cur_pos[0] + x, cur_pos[1] + y]
            except KeyError:
                pass
            else:
                nearby_cells.append(to_cell)
        return nearby_cells

    def wander(self):
        nearby_cells = self.get_nearby_cells()
        empty_cells = list(filter(lambda c: not c.content, nearby_cells))
        return random.choice(empty_cells) if empty_cells else None

    @staticmethod
    def lookup(area):  # returns collection [(creature, cell)...]
        found = {}
        for coords in area:
            cell = area[coords]
            if cell.content:
                obj = type(cell.content)
                if obj in found:
                    found[obj].append(cell)
                else:
                    found[obj] = [cell]
        return found

    def choose_closest_target(self, of_type, seen_objs: dict):
        cells = seen_objs.get(of_type)
        if cells:
            by_ascending = cells[:]
            by_ascending.sort(key=self.evaluate_distance_to_cell)
            return by_ascending[0]
        return None

    def evaluate_distance_to_cell(self, cell):
        return evaluate_direct_distance(self.get_abs_position(), (cell.x, cell.y))

    def figure_out_a_route(self, to_cell):
        memo = self._memory
        area_grid = self.get_area_grid()
        graph = graph_from_grid(*memo['_area_size'])
        start_point = self.get_rel_position()
        end_point = self.get_rel_cell_position(to_cell)

        def cell_is_empty_condition(node):
            return not area_grid[node].content or node == end_point

        path = a_star_search(start_point,
                             end_point,
                             graph,
                             additional_constraints_to_successors=cell_is_empty_condition)
        return path

    def clean_memo(self, *param_names, just_temp_data=True):
        if just_temp_data:
            param_names = []
            for param in self._temp_data_keys:
                self._memory[param] = None
            return
        for param in param_names:
            self._memory[param] = None

    def get_abs_position(self):
        memo = self._memory
        if not memo.get('_abs_pos'):
            for cell in memo['_area']:
                if cell.content is self:
                    memo['_abs_pos'] = cell.x, cell.y

        return memo['_abs_pos']

    def get_rel_position(self):  # that is, inside a given area where top left cell counts as (0,0) point
        memo = self._memory
        grid = self.get_area_grid()
        if not memo.get('_rel_pos'):
            for coords in grid:
                if grid[coords].content is self:
                    memo['_rel_pos'] = coords

        return memo['_rel_pos']

    def get_rel_cell_position(self, cell):
        first = self.get_area_grid()[0, 0]
        offset = first.x, first.y
        return cell.x - offset[0], cell.y - offset[1]

    def get_area_grid(self):
        memo = self._memory
        if not memo.get('_area_grid'):
            width, length = self.get_area_size()
            cell_gen = (cell for cell in memo['_area'])
            memo['_area_grid'] = dict(((x, y), next(cell_gen)) for y in range(length) for x in range(width))

        return memo['_area_grid']

    def get_area_size(self):
        memo = self._memory
        if not memo.get('_area_size'):
            width = 1
            for cell in memo['_area'][1:]:
                if memo['_area'][0].x == cell.x:
                    break
                else:
                    width += 1

            length = len(memo['_area']) // width
            memo['_area_size'] = (width, length)

        return memo['_area_size']

    @property
    def name(self):
        return f'{self.__class__.__name__}{self._id if self._id else "(w/out id)"}'


if __name__ == '__main__': pass