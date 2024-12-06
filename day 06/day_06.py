from bisect import bisect_left, bisect_right


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

    def __init__(self, start: tuple, is_vertical: bool, direction: int):
        self.row: int = start[0]
        self.col: int = start[1]
        self.mem: set = {self.position}
        self.vertical = is_vertical
        self.direction = direction

    def _v_toggle(self):
        self.vertical ^= True

    def turn(self):
        self.direction = (self.vertical * 2 - 1) * self.direction * -1
        self._v_toggle()

    def move(self, stop):
        if self.vertical:
            steps = abs(self.row - stop) - 1
            trace = [(self.row + self.direction * step, self.col) for step in range(steps)]  # col is fixed
            self.row += steps * self.direction
        else:
            steps = abs(self.col - stop) - 1
            trace = [(self.row, self.col + self.direction * step) for step in range(steps)]  # row is fixed
            self.col += steps * self.direction
        self.mem.update(trace)
        self.mem.add(self.position)

    @property
    def position(self):
        return self.row, self.col


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


# filename = "test_input"
filename = "input"

data = open(filename, "r").read().strip('\n').splitlines()
max_rows = len(data)
max_cols = len(data[0])

obst_rows = [[c for c, symbol in enumerate(row) if symbol == "#"] for row in data]
# it should be easier to identify obstacles if we have them indexed by column-firs also (e.g. when moving vertically)
obst_cols = [[r for r, symbol in enumerate(col) if symbol == "#"] for col in zip(*data)]

guard = Guard.make_guard(data)
obstacle = None
done = False
while not done:
    if guard.vertical:
        the_column = obst_cols[guard.col]
        if guard.direction < 0:
            obstacle_ind = bisect_right(the_column, guard.row) - 1
        else:
            obstacle_ind = bisect_left(the_column, guard.row)
        try:
            obstacle = the_column[obstacle_ind]
        except IndexError:
            obstacle = max_rows
            done = True
    else:
        the_row = obst_rows[guard.row]
        if guard.direction < 0:
            obstacle_ind = bisect_right(the_row, guard.col) - 1
        else:
            obstacle_ind = bisect_left(the_row, guard.col)
        try:
            obstacle = the_row[obstacle_ind]
        except IndexError:
            obstacle = max_cols
            done = True
    if obstacle_ind < 0:
        obstacle = -1
        done = True
    guard.move(obstacle)
    # When guard has moved to next obstacle she turns
    guard.turn()
    # show_map(max_rows, max_cols, obst_rows, guard)

print('\n', len(guard.mem))
print('====')
# print(*obst_rows, sep='\n')
# print('====')
# print(*obst_cols, sep='\n')
