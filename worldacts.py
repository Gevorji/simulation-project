from world_objects import *
from world_objects.actions import Actions as ObjActions
from abc import ABC, abstractmethod
import random


class WorldAction(ABC):

    def __init__(self, world_map):
        self._world_map = world_map

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class ObjectSpawner(WorldAction): pass

class PopulateWorld(WorldAction):

    def execute(self, wparams):
        _map = self._world_map
        cells_number = _map.width * _map.length
        obj_howmuch = {}
        rand_creatures_num_boundaries = (wparams['USR_RAND_BOUNDARIES_FOR_CREATURES']
                                         or (cells_number // 20 or 1, cells_number // 5 or 1))
        rand_rocks_num_boundaries = (wparams['USR_RAND_BOUNDARIES_FOR_ROCKS']
                                     or (cells_number // 8 or 1, cells_number // 3 or 1))
        rand_grass_num_boundaries = (wparams['USR_RAND_BOUNDARIES_FOR_GRASS']
                                     or (cells_number // 8 or 1, cells_number // 3 or 1))
        obj_howmuch[Predator] = wparams['STANDARD_PREDATORS_NUMBER']
        obj_howmuch[Herbivore] = wparams['STANDARD_HERBIVORES_NUMBER']
        obj_howmuch[Rock] = wparams['STANDARD_ROCKS_NUMBER']
        obj_howmuch[Grass] = wparams['STANDARD_GRASS_NUMBER']
        if wparams['RANDOMIZE_CREATURES_NUMBER'] or wparams['USR_RAND_BOUNDARIES_FOR_CREATURES']:
            obj_howmuch[Predator] = random.randint(*rand_creatures_num_boundaries)
            obj_howmuch[Herbivore] = random.randint(*rand_creatures_num_boundaries)
            obj_howmuch[Rock] = random.randint(*rand_rocks_num_boundaries)
            obj_howmuch[Grass] = random.randint(*rand_grass_num_boundaries)
        for obj, number in obj_howmuch.items():
            for i in range(number):
                while True:
                    x, y = random.randint(0, _map.width), random.randint(0, _map.length)
                    try:
                        _map[x, y].put(obj)
                        break
                    except AssertionError:
                        continue


class MakeEachObjDoMove(WorldAction):

    def __init__(self, act_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.act_handler = act_handler

    def execute(self):
        _map = self._world_map
        for cell in _map.field_iterator():
            entity = cell.content
            if hasattr(entity, 'make_move'):
                vis_area = self.get_visible_area_for_creature(cell)
                actions = list(entity.make_move(vis_area))  # because we expect obj to produce 1 or more actions
                for action in actions:
                    procedure = self.act_handler.handle(cell, action, _map)
                    procedure()

    def get_visible_area_for_creature(self, cell):
        x_lim = self._world_map.width
        y_lim = self._world_map.length
        creature = cell.content
        vis_rad = creature.vis_radius
        top_left_point_x = cell.x - vis_rad if cell.x > vis_rad else 0
        top_left_point_y = cell.y - vis_rad if cell.y > vis_rad else 0
        bot_right_point_x = cell.x + vis_rad
        bot_right_point_y = cell.y + vis_rad
        bot_right_point_x = x_lim if bot_right_point_x > x_lim else bot_right_point_x
        bot_right_point_y = y_lim if bot_right_point_y > y_lim else bot_right_point_y

        return self._world_map.field_iterator(from_point=(top_left_point_x, top_left_point_y),
                                              to_point=(bot_right_point_x, bot_right_point_y))


class ResourceRestoring(WorldAction):

    def __init__(self, resource, min_resource_limit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = resource
        self.min_resource_limit = min_resource_limit

    def execute(self, *args, **kwargs):
        if self.count_resource() <= self.min_resource_limit: pass


    def count_resource(self):
        count = 0
        for cell in self._world_map.field_iterator():
            if isinstance(cell.content, self.resource):
                count += 1
        return count


class Handler:
    """
    Handles interactions between objects
    """
    direction_to_coordinates_offset = {
        ObjActions.UP: (0, -1),
        ObjActions.DOWN: (0, 1),
        ObjActions.LEFT: (-1, 0),
        ObjActions.RIGHT: (1, 0)
    }
    action_handler_bindings = {}

    def __init__(self):
        pass

    def handle(self, cell, action, _map):  # return a function that will be placed in queue

        handler = self.action_handler_bindings[action.type]
        from_cell = cell
        offsetx, offsety = self.direction_to_coordinates_offset[action.direction]
        to_cell = _map[from_cell.x + offsetx, from_cell.y + offsety]

        return self._make_function_for_suspended_call(handler, args=(from_cell, to_cell))

    @staticmethod
    def _make_function_for_suspended_call(func, *, args: tuple = (), kwargs: dict = {}):

        def to_call_later():
            return func(*args, **kwargs)

        return to_call_later

    @staticmethod
    def handle_replace(from_cell, to_cell):
        obj = from_cell.pop()
        to_cell.put(obj)

    action_handler_bindings[ObjActions.MOVE] = handle_replace

    @staticmethod
    def handle_attack(from_cell, to_cell):
        attacker = from_cell.content
        receiver = to_cell.content
        if hasattr(receiver, 'take_damage'):
            receiver.take_damage(attacker.attack_damage)

    action_handler_bindings[ObjActions.ATTACK] = handle_attack

    @staticmethod
    def handle_eating(from_cell, to_cell):
        eater = from_cell.content
        consumable = to_cell.content
        if hasattr(consumable, 'consume') and hasattr(eater, 'restore_hp'):
            eater.restore_hp(consumable.consume())

    action_handler_bindings[ObjActions.EAT] = handle_eating
