def calc_bb(point, bounds):
    distances = min(point[0], bounds[0] - point[0]), min(point[1], bounds[1] - point[1])
    bb = {
        'rows': {'min': point[0]-distances[0], 'max': point[0]+distances[0]},
        'cols': {'min': point[1]-distances[1], 'max': point[1]+distances[1]}
    }


def in_bb(point, bb):
    return bb['rows']['min'] <= point[0] <= bb['rows']['max'] and \
           bb['cols']['min'] <= point[1] <= bb['cols']['max']


filename = 'test'
# filename = 'input'

file = open(filename, 'r').read()
frequencies = set(file) - set('\n#.')
locations = {}
for freq in frequencies:
    locations[freq] = [(r, c)
                       for r, row in enumerate(file.splitlines())
                       for c, symbol in enumerate(row) if symbol == freq]

print(locations)
