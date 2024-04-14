import simulationlogger
import world_objects.entityabc
from world_objects import *
from world_objects.actions import Actions as ObjActions
from abc import ABC, abstractmethod
import random

OBJ_TYPES = [
    Herbivore, Predator, Grass, Rock
]


class WorldAction(ABC):

    def __init__(self, world_map):
        self._world_map = world_map

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class ObjectSpawner:

    def __init__(self, _world_map, obj=None, target_cell=None):
        self._world_map = _world_map
        self.target_cell = target_cell
        self.obj = obj

    def spawn(self):
        self.target_cell.put(self.obj)


class RandomLocationObjectSpawner(ObjectSpawner):
    def spawn(self):
        _map, obj = self._world_map, self.obj
        while True:
            x, y = random.randint(0, _map.width), random.randint(0, _map.length)
            try:
                _map[x, y].put(obj)
                break
            except AssertionError:
                continue

class GenerateWorldObjects(WorldAction):

    def __init__(self, parameters, objs_buffer: list,world_map):
        super().__init__(world_map)
        self.objs_buffer = objs_buffer
        self.parameters = parameters

    def execute(self):
        objects = self.objs_buffer
        cells_number = self._world_map.width*self._world_map.length
        wparams = self.parameters
        for obj_type in OBJ_TYPES:
            if not wparams.getboolean('DEFAULT', 'RandomizeMap'):
                n = wparams.get('DEFAULT', f'n{obj_type.__name__}')
            else:
                rand_boundaries = tuple(int(param) * cells_number or 1 for param
                                        in
                                        wparams['RANDOM_OBJ_NUMBERS_RATIOS'][f'{obj_type.__name__}number'].split(','))
                n = random.randint(*rand_boundaries) \

            for i in range(n):
                obj_params = self.get_parameters(obj_type)
                obj = obj_type(obj_params)
                objects.append(obj)

    def get_parameters(self, for_obj_type):
        # if parameter was not initialized on start input request
        # or set up manually in configs.ini, then it is generated randomly
        # using boundaries defined in configs.ini
        gparameters = self.parameters
        obj_parameters = {}
        types_section = gparameters[for_obj_type.__name__.upper()]
        for obj_param in types_section:
            obj_parameters[obj_param] = val = types_section[obj_param]
            if val == 'empty':
                rand_boundaries = [int(b) for b in
                                   gparameters.get(f'RAND.{for_obj_type.__name__.upper()}_PARAMS', obj_param).split(',')]
                fallback = random.randint(*rand_boundaries)
                obj_parameters[obj_param] = fallback
        return obj_parameters

class PopulateWorld(WorldAction):

    def __init__(self, wparams, objs_buffer,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objs_buffer = objs_buffer
        self.obj_types = OBJ_TYPES
        self.wparams = wparams

    def execute(self):
        _map = self._world_map
        # placing objects on map
        spawner = RandomLocationObjectSpawner(_map)
        for obj in self.objs_buffer:
            spawner.obj = obj
            spawner.spawn()


class MakeEachObjDoMove(WorldAction):

    def __init__(self, act_handler, logger: simulationlogger.Logger, world_map):
        super().__init__(world_map)
        self.logger = logger
        self.act_handler = act_handler

    def execute(self):
        _map = self._world_map
        logger = self.logger
        logger.start_turn_session()
        for cell in _map.field_iterator():
            entity = cell.content
            if hasattr(entity, 'make_move'):
                vis_area = self.get_visible_area_for_creature(cell)
                for action in entity.make_move(vis_area):  # because we expect obj to produce 1 or more actions
                    if action is None:
                        logger.register(simulationlogger.ActionEntry(action, cell, cell))
                        continue
                    procedure = self.act_handler.handle(cell, action, _map)
                    target_cell = procedure.args[1]
                    logger.register(simulationlogger.ActionEntry(action, cell, target_cell))
                    procedure()
                    if isinstance(target_cell.content, world_objects.entityabc.Entity):
                        self.act_handler.handle_state(target_cell)
                        logger.register(simulationlogger.EntityStateEntry(target_cell,
                                                                          target_cell.content.health_points))

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
        self.spawner = resource

    def execute(self, *args, **kwargs):
        shortage = self.count_resource() - self.min_resource_limit
        some_extras = random.randint(0, 3) if shortage < 0 else 0
        while shortage < some_extras:
            self.spawner.execute()
            shortage += 1

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
        ObjActions.RIGHT: (0, 1)
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

    @staticmethod
    def handle_state(cell):
        entity = cell.content
        if hasattr(entity, 'is_dead'):
            if entity.is_dead():
                cell.pop()
        # how do we handle eaten Grass?