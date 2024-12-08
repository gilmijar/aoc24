from itertools import combinations


def calc_bb(point, bounds):
    distances = min(point[0], bounds[0] - 1 - point[0]), min(point[1], bounds[1] - 1 - point[1])
    bb = {
        'rows': {'min': point[0]-distances[0], 'max': point[0]+distances[0]},
        'cols': {'min': point[1]-distances[1], 'max': point[1]+distances[1]}
    }
    return bb


def in_bb(point, bb):
    return bb['rows']['min'] <= point[0] <= bb['rows']['max'] and \
           bb['cols']['min'] <= point[1] <= bb['cols']['max']


def calc_antinode(point, other):
    r1, c1 = point
    r2, c2 = other
    r = r1 - r2 + r1
    c = c1 - c2 + c1
    return r, c


def calc_harm(points, bounds):
    r1, c1 = points[0]
    r2, c2 = points[1]
    step = r2 - r1
    rise = c2 - c1
    skip = r1 % step
    shift = c1 - rise * (r1 // step)
    rows = range(skip, bounds[0], step)
    if rise < 0:
        cols = range(shift, -1, rise)
    else:
        cols = range(shift, bounds[1], rise)
    return [(r, c) for r, c in zip(rows, cols) if 0 <= c < bounds[1]]


def cmp(antinodes, board):
    print(' '+''.join(map(str, range(len(board[0])))))
    for r, row in enumerate(board):
        print(r, end='')
        for c, mark in enumerate(row):
            if mark not in '.' and (r, c) not in antinodes:
                print('*', end='')
            elif mark == '.' and (r, c) in antinodes:
                print('!', end='')
            else:
                print(mark, end='')
        print()


def show(antinodes, board):
    print('   ' + ' '.join(map(str, range(len(board[0])))))
    for r, row in enumerate(board):
        print(f'{r: =2}', end=' ')
        for c, mark in enumerate(row):
            if mark not in '.' and (r, c) in antinodes:
                print(mark, end=' ')
            elif (r, c) in antinodes:
                print('#', end=' ')
            else:
                print('.', end=' ')
        print()


# filename = 'test'
filename = 'input'

file = open(filename, 'r').read()
lines = file.splitlines()
max_row = len(lines)
max_col = len(lines[0])
frequencies = set(file) - set('\n#.')
locations = {}
for freq in frequencies:
    locations[freq] = [(r, c)
                       for r, row in enumerate(lines)
                       for c, symbol in enumerate(row) if symbol == freq]

focals = set()
for freq in frequencies:
    for antenna in locations[freq]:
        a_bb = calc_bb(antenna, (max_row, max_col))
        antennae = locations[freq][:]
        antennae.remove(antenna)
        focals.update(calc_antinode(antenna, other_antenna) for other_antenna in antennae if in_bb(other_antenna, a_bb))

print(len(focals))
print("\nPart 2\n")

focals = set()
for freq in frequencies:
    print(f"{freq=}")
    antenna_pairs = combinations(sorted(locations[freq]), 2)
    for antenna, other_antenna in antenna_pairs:
        print(antenna, other_antenna)
        harmonics = calc_harm((antenna, other_antenna), (max_row, max_col))
        focals.update(harmonics)
        print(harmonics)

print()
print("harmonics count:", len(focals))
# for p in sorted(focals):
#     print(p)

