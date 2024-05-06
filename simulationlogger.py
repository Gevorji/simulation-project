import dataclasses

from map import Cell
from world_objects.actions import Actions


@dataclasses.dataclass
class ActionEntry:
    action: Actions | None
    _actor: Cell
    _target: Cell | None

    def __post_init__(self):
        self.actor_pos = self._actor.x, self._actor.y
        self.actor = getattr(self._actor.content, 'name', '(nameless)')
        self.target = 'cell' if not self._target.content else (
            getattr(self._target.content, 'name', self._target.content.__class__.__name__))
        self.target_pos = self._target.x, self._target.y
        self.act_type = {Actions.ATTACK: 'attack', Actions.EAT: 'eating', Actions.MOVE: 'move'}[self.action.type]


@dataclasses.dataclass
class EntityStateEntry:
    cell: Cell
    hp: int

    def __post_init__(self):
        self.entity = getattr(self.cell.content, 'name', self.cell.content.__class__.__name__)
        self.entity_pos = self.cell.x, self.cell.y


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
        assert session is not None, 'No started session to work with'
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
        if action is None:
            return f'{entry.actor} (pos {entry.actor_pos}) does nothing'
        return f'{entry.actor} (pos {entry.actor_pos}) makes {entry.act_type} to {entry.target} (pos {entry.target_pos})'

    if isinstance(entry, EntityStateEntry):
        cell = entry.entity
        return f'{entry.entity} (pos {entry.entity_pos}) state: hp={entry.hp}'

    if isinstance(entry, RestorationObjectsEntry):
        return f'Restoring {entry.object_type}: {str(int(entry.how_much))} units'

