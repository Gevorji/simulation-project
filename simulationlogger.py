import dataclasses

from map import Cell
from world_objects.actions import Actions


@dataclasses.dataclass
class ActionEntry:
    action: Actions | None
    actor: Cell
    target: Cell | None


@dataclasses.dataclass
class EntityStateEntry:
    entity: Cell
    hp: int


@dataclasses.dataclass
class RestorationObjectsEntry:
    object_type: str
    how_much: int

class Logger:
    def __init__(self):
        self.registry = []
        self._current_turn_session = None

    def start_turn_session(self):
        self._current_turn_session = []

    def register(self, entry: ActionEntry | EntityStateEntry):
        session = self._current_turn_session
        assert session, 'No started session to work with'
        session.append(entry)

    def close_turn_session(self):
        self.registry.append(self._current_turn_session)
        self._current_turn_session = None

    def get_turn_logging(self, nturn):
        return tuple(make_presentational_format(entry) for entry in self.registry[nturn-1])


def make_presentational_format(entry):
    if isinstance(entry, ActionEntry):
        action = entry.action
        actor = entry.actor
        target = entry.target
        actor_name, = getattr(actor.content, '_name', '(nameless)'),
        target_name = getattr(target.content, '_name', '(nameless)')
        if action is None:
            return f'{actor_name} (pos {actor.x, actor.y}) does nothing'
        act_type = {Actions.ATTACK: 'attack', Actions.EAT: 'eating', Actions.MOVE: 'move'}[action.type]
        return f'{actor_name} (pos {actor.x, actor.y}) makes {act_type} to {target_name} (pos {target.x, target.y}'

    if isinstance(entry, EntityStateEntry):
        entity = entry.entity
        entity_name = getattr(entity.content, '_name', '(nameless)')
        return f'{entity_name} (pos {entity.x, entity.y}) state: hp={entry.hp}'

    if isinstance(entry, RestorationObjectsEntry):
        return f'Restoring {entry.object_type}: {entry.how_much} units'

