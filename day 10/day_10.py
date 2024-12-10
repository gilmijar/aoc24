# filename = 'small_test'
# filename = 'test'
filename = 'input'


def explore(terr: dict, pos: complex, no_repeats: bool = True):
    height = terr[pos]
    if no_repeats:
        del terr[pos]
    if height == 9:
        return 1
    else:
        trails = 0
        for heading in (-1j, 1j, -1, 1):
            direction = pos + heading
            try:
                if terr[direction] == height + 1:
                    trails += explore(terr, direction, no_repeats)
            except KeyError:
                pass
        return trails


traces = {}

data = open(filename, 'r').read().strip().splitlines()
terrain = {r + c * 1j: int(v) for r, row in enumerate(data) for c, v in enumerate(row) if v != '.'}

# find all 0s, but now let's test for ixed pos (0, 0)
t_heads = [k for k, v in terrain.items() if v == 0]
# Since we mutate the terrain map for with each step - every starting point gets its own copy
scores = [explore(dict(terrain), t_h) for t_h in t_heads]
print(scores)
print(sum(scores))

print('\n   Part 2 \n')

scores = [explore(terrain, t_h, no_repeats=False) for t_h in t_heads]
print(scores)
print(sum(scores))
