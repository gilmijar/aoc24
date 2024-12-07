from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from copy import deepcopy
from functools import partial


class Guard:
    @classmethod
    def make_guard(cls, room):
        configs = [
            ('^', True, -1),
            ('>', False, 1),
            ('v', True, 1),
            ('<', False, -1)
        ]
        row_size = len(room[0])
        flat_room = ''.join(room)
        for mark, axis, direction in configs:
            position = flat_room.find(mark)
            if position > -1:
                row, col = divmod(position, row_size)
                return cls((row, col), axis, direction)
        raise ValueError("Guard not found!")

    def __init__(self, start: tuple, vertical: bool, direction: int):
        self.row: int = start[0]
        self.col: int = start[1]
        self.mem: set = {self.position}
        self.vertical: bool = vertical
        self.direction: int = direction
        self.legs: list = []

    def _v_toggle(self):
        self.vertical ^= True

    def turn(self):
        self.direction = (self.vertical * 2 - 1) * self.direction * -1
        self._v_toggle()

    def move(self, stop):
        if self.vertical:
            steps = abs(self.row - stop) - 1
            trace = [(self.row + self.direction * step, self.col) for step in range(steps)]  # col is fixed
            alignment = 'vertical' if self.vertical else 'horizontal'
            leg = Leg(alignment, self.direction, self.col, self.row, -1)
            self.row += steps * self.direction
            leg.stop = self.row
        else:
            steps = abs(self.col - stop) - 1
            trace = [(self.row, self.col + self.direction * step) for step in range(steps)]  # row is fixed
            alignment = 'vertical' if self.vertical else 'horizontal'
            leg = Leg(alignment, self.direction, self.row, self.col, -1)
            self.col += steps * self.direction
            leg.stop = self.col
        self.mem.update(trace)
        self.mem.add(self.position)
        self.legs.append(leg)
        return trace

    def check_cycle(self):
        tested_leg = self.legs[-1]
        return any((tested_leg in other_leg) for other_leg in self.legs[:-2])

    @property
    def position(self):
        return self.row, self.col


@dataclass
class Leg:
    alignment: str
    direction: int
    number: int
    start: int
    stop: int

    def _overlaps(self, other):
        return self.number == other.number and \
               self.alignment == other.alignment and \
               self.direction == other.direction and \
               min(self.start, self.stop) <= max(other.start, other.stop) and \
               max(self.start, self.stop) >= min(other.start, other.stop)

    def __contains__(self, item):
        return self._overlaps(item)


def show_map(y, x, obs, g):
    print('\n' * 3)
    for r in range(y):
        obst_row = obs[r]
        for c in range(x):
            if (r, c) == g.position:
                configs = {(True, -1): '^', (False, 1): '>', (True, 1): 'v', (False, -1): '<'}
                print(configs[(g.vertical, g.direction)], end='')
            elif (r, c) in g.mem:
                print("o", end='')
            elif c in obst_row:
                print("#", end='')
            else:
                print(".", end='')
        print()

def find_obstacle(obs_rows, obs_cols, g):
    if g.vertical:
        the_column = obs_cols[g.col]
        if g.direction < 0:
            obstacle_ind = bisect_right(the_column, g.row) - 1
        else:
            obstacle_ind = bisect_left(the_column, g.row)
        try:
            obstacle = the_column[obstacle_ind]
        except IndexError:
            obstacle = max_rows
            done = True
    else:
        the_row = obs_rows[g.row]
        if g.direction < 0:
            obstacle_ind = bisect_right(the_row, g.col) - 1
        else:
            obstacle_ind = bisect_left(the_row, g.col)
        try:
            obstacle = the_row[obstacle_ind]
        except IndexError:
            obstacle = max_cols
            done = True
    if obstacle_ind < 0:
        obstacle = -1
        done = True
    return obstacle, done


def action(obs_rows, obs_cols, g):
    obstacle = None
    done = False
    diversions = []
    while not done:
        obstacle, done = find_obstacle(obs_rows, obs_cols, g)
        g.move(obstacle)
        # When g has moved to next obstacle she turns
        g.turn()


def action_2(obs_rows, obs_cols, g):
    obstacle = None
    done = False
    diversions = []
    while not done:
        obstacle, done = find_obstacle(obs_rows, obs_cols, g)
        new_g = deepcopy(g)
        trace = g.move(obstacle)
        for pos in trace:
            if new_g.vetical:
                obstacle = pos[0]

        # When g has moved to next obstacle she turns
        g.turn()


if __name__ == "__main__":
    filename = "test_input"
    # filename = "input"

    data = open(filename, "r").read().strip('\n').splitlines()
    max_rows = len(data)
    max_cols = len(data[0])

    obst_rows = [[c for c, symbol in enumerate(row) if symbol == "#"] for row in data]
    # it should be easier to identify obstacles if we have them indexed by column-first (e.g. when moving vertically)
    obst_cols = [[r for r, symbol in enumerate(col) if symbol == "#"] for col in zip(*data)]

    _action = partial(action, obst_rows, obst_cols)

    guard = Guard.make_guard(data)

    _action(guard)

    print('\n', len(guard.mem))
    print('\n   Part 2   \n')

