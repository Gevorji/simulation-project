from enum import Enum

class Actions(Enum):
    MOVE_RIGHT = 'mrght'
    MOVE_LEFT = 'mlft'
    MOVE_UP = 'mup'
    MOVE_DOWN = 'mdwn'
    ATTACK_RIGHT = 'atkrght'
    ATTACK_LEFT = 'atklft'
    ATTACK_UP = 'atkup'
    ATTACK_DOWN = 'atkdwn'
    EAT_RIGHT = 'etrght'
    EAT_LEFT = 'etlft'
    EAT_UP = 'etup'
    EAT_DOWN = 'etdwn'