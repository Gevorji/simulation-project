from typing import Any, Optional, Union

import map as wmap
import simulationlogger
import world_objects.entityabc
from world_objects import *
from world_objects.actions import Actions as ObjActions
from world_objects.creatureabc import Creature
from abc import ABC, abstractmethod
import random

OBJ_TYPES = [
    Herbivore, Predator, Grass, Rock
]


class WorldAction(ABC):

    def __init__(self, world_map: wmap.Map):
        self._world_map = world_map

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class ObjectSpawner:

    _spawn_count = 0

    def __init__(self, _world_map, wparams, obj_type: Union[*OBJ_TYPES] = None, target_cell: wmap.Cell = None):
        self.obj_params = wparams[obj_type.__name__.upper()] if obj_type else None
        self.wparams = wparams
        self._world_map = _world_map
        self.target_cell = target_cell
        self.obj_type = obj_type

    def set_obj_type(self, obj_type):
        self.obj_type = obj_type
        self.obj_params = self.wparams[obj_type.__name__.upper()]

    def generate_obj(self):
        self.__class__._spawn_count += 1
        params = self.get_parameters()
        if issubclass(self.obj_type, Creature):

            params['_id'] = self._spawn_count
        return self.obj_type(**params)

    def spawn(self):
        obj = self.generate_obj()
        self.target_cell.put(obj)

    def get_parameters(self):
        # if parameter was not initialized on start input request
        # or set up manually in configs.ini, then it is generated randomly
        # using boundaries defined in configs.ini
        wparams = self.wparams
        obj_params = self.obj_params
        inst_params = {}
        for obj_param in obj_params:
            if obj_param in wparams['DEFAULT']:  # this lets bypassing of a redundant default keys in section  -
                continue                             # configparser's unwanted behaviour for our case
            val = obj_params[obj_param]
            val = int(val) if val.isdecimal() else val
            inst_params[obj_param] = val
            if not val:
                rand_boundaries = [int(b) for b in
                                   wparams.get(f'RAND.{self.obj_type.__name__.upper()}_PARAMS', obj_param).split(',')]
                fallback = random.randint(*rand_boundaries)
                inst_params[obj_param] = fallback
        return inst_params


class RandomLocationObjectSpawner(ObjectSpawner):
    def spawn(self):
        _map = self._world_map
        obj = self.generate_obj()
        while True:
            x, y = random.randint(0, _map.width-1), random.randint(0, _map.length-1)
            try:
                _map[x, y].put(obj)
                break
            except AssertionError:
                continue


class PopulateWorld(WorldAction):

    def __init__(self, parameters, world_map):
        super().__init__(world_map)
        self.parameters = parameters

    def execute(self):
        cells_number = self._world_map.width*self._world_map.length
        wparams = self.parameters
        for obj_type in OBJ_TYPES:
            spawner = RandomLocationObjectSpawner(self._world_map, wparams, obj_type)
            rand_boundaries = tuple(round(float(param) * cells_number) or 1 for param
                                    in
                                    wparams['RANDOM_OBJ_NUMBERS_RATIOS'][f'{obj_type.__name__}Number'].split(','))
            n = wparams.get('DEFAULT', f'n{obj_type.__name__}')
            if not n:
                n = random.randint(*rand_boundaries)
            else:
                n = int(n)
                if n > rand_boundaries[1]:
                    n = rand_boundaries[1]
            for i in range(n):
                spawner.spawn()


class MakeEachObjDoMove(WorldAction):

    def __init__(self, act_handler, logger: simulationlogger.Logger, world_map):
        super().__init__(world_map)
        self.logger = logger
        self.act_handler = act_handler

    def execute(self):
        _map = self._world_map
        logger = self.logger
        for cell in _map.field_iterator(return_contents=False):
            entity = cell.content
            if hasattr(entity, 'make_move'):
                vis_area = self.get_visible_area_for_creature(cell)
                for action in entity.make_move(vis_area):  # because we expect obj to produce 1 or more actions
                    if action is None:
                        logger.register(simulationlogger.ActionEntry(action, cell, cell))
                        continue
                    procedure = self.act_handler.handle(cell, action, _map)
                    target_cell = procedure.args[1]
                    if action.type is ObjActions.MOVE:
                        cell = target_cell
                    logger.register(simulationlogger.ActionEntry(action, cell, target_cell))
                    procedure()
                    if isinstance(target_cell.content, world_objects.entityabc.Entity):
                        self.act_handler.handle_state(target_cell)
                        logger.register(simulationlogger.EntityStateEntry(target_cell,
                                                                          target_cell.content.health_points))

    def get_visible_area_for_creature(self, cell):

        x_lim = self._world_map.width - 1
        y_lim = self._world_map.length - 1
        creature = cell.content
        vis_rad = creature.vis_radius
        top_left_point_x = cell.x - vis_rad if cell.x > vis_rad else 0
        top_left_point_y = cell.y - vis_rad if cell.y > vis_rad else 0
        bot_right_point_x = cell.x + vis_rad
        bot_right_point_y = cell.y + vis_rad
        bot_right_point_x = x_lim if bot_right_point_x > x_lim else bot_right_point_x
        bot_right_point_y = y_lim if bot_right_point_y > y_lim else bot_right_point_y

        return self._world_map.field_iterator(from_point=(top_left_point_x, top_left_point_y),
                                              to_point=(bot_right_point_x, bot_right_point_y), return_contents=False)


class ResourceRestoring(WorldAction):

    def __init__(self, resource, min_resource_limit, spawner, logger, world_map):
        super().__init__(world_map)
        self.logger = logger
        self.resource = resource
        self.min_resource_limit = min_resource_limit
        self.spawner = spawner

    def execute(self, *args, **kwargs):
        shortage = self.count_resource() - self.min_resource_limit
        some_extras = random.randint(0, 3) if shortage < 0 else 0
        self.logger.register(simulationlogger.RestorationObjectsEntry(self.resource.__name__,
                                                                      abs(shortage) + some_extras))
        while shortage < some_extras:
            self.spawner.spawn()
            shortage += 1

    def count_resource(self):
        return self._world_map.get_objs_numbers().get(self.resource, 0)


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

    def handle(self, cell, action, _map):

        handler = self.action_handler_bindings[action.type]
        from_cell = cell
        offsetx, offsety = self.direction_to_coordinates_offset[action.direction]
        to_cell = _map[from_cell.x + offsetx, from_cell.y + offsety]
        return self._make_suspended_callable(handler, args=(from_cell, to_cell))

    @staticmethod
    def _make_suspended_callable(func, *, args: tuple = (), kwargs: dict = {}):

        class SuspendedCallable:
            def __init__(self):
                self.args = args
                self.kwargs = kwargs

            def __call__(self):
                return func(*self.args, **self.kwargs)

        return SuspendedCallable()

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

    @staticmethod
    def handle_state(cell):
        entity = cell.content
        if hasattr(entity, 'is_dead'):
            if entity.is_dead():
                cell.pop()
        # how do we handle eaten Grass?