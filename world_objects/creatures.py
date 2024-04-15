try:
    from .creatureabc import Creature
except ImportError:
    from creatureabc import Creature
from algorithms import evaluate_direct_distance, transform_to_lrud_sequence as to_lrud
from .grass import Grass
from .actions import Actions


def transform_to_lrud_sequence(path: tuple):
    direction_to_action = {'left': Actions.LEFT,
                           'right': Actions.RIGHT,
                           'up': Actions.UP,
                           'down': Actions.DOWN}
    yield from (direction_to_action[direction] for direction in to_lrud(path))


class Predator(Creature):
    haunted_creatures = []

    def __init__(self, attack_damage, health_points, move_speed, vis_radius, sex):
        super().__init__(health_points, move_speed, vis_radius, sex)
        self.attack_damage = attack_damage
        self._memory['_victim'] = None

    def make_move(self, area):
        self.clean_memo()
        super().make_move(area)
        memo = self._memory
        seen_objs = self.lookup(memo['_area_grid'])
        path = None

        closest_ones = list(filter(None,
                                   (self.choose_closest_target(haunted_type, seen_objs)
                                    for haunted_type in self.haunted_creatures)))
        if closest_ones:
            dist, closest = min((self.evaluate_distance_to_cell(creature), creature) for creature in closest_ones)
            if dist == 1.0:
                directions = transform_to_lrud_sequence((self.get_rel_position(), self.get_rel_cell_position(closest)))
                yield from (direction | Actions.ATTACK for direction in directions)
                return
            # try to find a way to target
            path = self.figure_out_a_route(closest)
            path = path[:-1] if path else None

        # no path to
        if not path:
            rand_cell = self.wander()
            if not rand_cell:
                yield None
                return
            path = (self.get_rel_position(), self.get_rel_cell_position(rand_cell))

        directions = transform_to_lrud_sequence(path)
        for i in range(self.move_speed):
            try:
                direction = next(directions)
            except StopIteration:
                break
            yield direction | Actions.MOVE
            self.clean_memo('_rel_pos', '_abs_pos', just_temp_data=False)


class Herbivore(Creature):

    def __init__(self, health_points, move_speed, vis_radius, sex):
        super().__init__(health_points, move_speed, vis_radius, sex)

    def make_move(self, area):
        self.clean_memo()
        super().make_move(area)
        memo = self._memory
        seen_objs = self.lookup(memo['_area_grid'])
        path = None
        closest_food = self.choose_closest_target(Grass, seen_objs)
        closest_danger = self.choose_closest_target(Predator, seen_objs)

        if closest_danger and self.evaluate_distance_to_cell(closest_danger) <= 2:
            av_cells = self.runaway(closest_danger)
            if av_cells:
                runaway_pos = av_cells[0]
                path = (self.get_rel_position(), self.get_rel_cell_position(runaway_pos))

        if closest_food and not path:
            if self.evaluate_distance_to_cell(closest_food) == 1:
                directions = transform_to_lrud_sequence((self.get_rel_position(),
                                                         self.get_rel_cell_position(closest_food)))
                yield from (direction | Actions.EAT for direction in directions)
                return
            else:
                path = self.figure_out_a_route(closest_food)
                path = path[:-1] if path else path

        if not path:
            rand_cell = self.wander()
            if not rand_cell:
                yield None
                return
            path = (self.get_rel_position(), self.get_rel_cell_position(rand_cell))

        directions = transform_to_lrud_sequence(path)
        for i in range(self.move_speed):
            try:
                direction = next(directions)
            except StopIteration:
                break
            yield direction | Actions.MOVE
            self.clean_memo('_rel_pos', '_abs_pos', just_temp_data=False)

    def runaway(self, from_who):
        nearby_cells = self.get_nearby_cells()
        cur_dist = self.evaluate_distance_to_cell(from_who)
        available = list(filter(lambda c: not c.content and
                                evaluate_direct_distance((c.x, c.y),
                                                         (from_who.x, from_who.y)) > cur_dist,
                                nearby_cells))
        return available


# appending Herbivore to Predators target list
Predator.haunted_creatures.append(Herbivore)

if __name__ == '__main__':
    h = Herbivore(10, 10)
    print(h.__dict__)
