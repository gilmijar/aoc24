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