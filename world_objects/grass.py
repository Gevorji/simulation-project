from .entityabc import Entity


class Grass(Entity):

    def __init__(self, hp_restore):
        self.hp_restore = hp_restore
