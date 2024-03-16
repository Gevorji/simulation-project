from enum import Flag, auto


class Actions(Flag):
    MOVE = auto()
    EAT = auto()
    ATTACK = auto()
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    MOVE_RIGHT = MOVE | RIGHT
    MOVE_LEFT = MOVE | LEFT
    MOVE_UP = MOVE | UP
    MOVE_DOWN = MOVE | DOWN
    ATTACK_RIGHT = ATTACK | RIGHT
    ATTACK_LEFT = ATTACK | LEFT
    ATTACK_UP = ATTACK | UP
    ATTACK_DOWN = ATTACK | DOWN
    EAT_RIGHT = EAT | RIGHT
    EAT_LEFT = EAT | LEFT
    EAT_UP = EAT | UP
    EAT_DOWN = EAT | DOWN
    __BASICS = [EAT, ATTACK, MOVE, UP, RIGHT, DOWN, LEFT]

    @property
    def type(self):
        if self.value in Actions.get_basics():
            return None
        return list(self)[0]

    @property
    def direction(self):
        if self.value in Actions.get_basics():
            return None
        return list(self)[1]

    @classmethod
    def get_basics(cls):
        return cls.__BASICS
