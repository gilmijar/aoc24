""" this has been played with after completing the tasks """
from functools import partial
from operator import add, mul
from time import monotonic


def apply(funcs, inp, target=None):
    if len(inp) == 1:
        return inp[0],
    others = apply(funcs, inp[1:], target)
    return [func(x, inp[0]) for x in others for func in funcs if (target is None or x <= target)]


def concat(a, b):
    return a * 10 ** len(str(b)) + b


filename = 'input'
# filename = 'test'

addmul = partial(apply, (add, mul))
addmulconcat = partial(apply, (add, mul, concat))

data = open(filename, 'r').read().splitlines()
sets = [(int(line.partition(':')[0]), [int(x) for x in line.partition(':')[2].split()]) for line in data]
t0 = monotonic()
good = [r for r, x in sets if r in addmul(x[::-1])]
print(f'addmul, no target: {monotonic() - t0 :0.6f}')

t0 = monotonic()
good = [r for r, x in sets if r in addmul(x[::-1], r)]
print(f'addmul, with target: {monotonic() - t0 :0.6f}')
print('Part 1', sum(good))

t0 = monotonic()
good = [r for r, x in sets if r in addmulconcat(x[::-1])]
print(f'addmulconcat, no target: {monotonic() - t0 :0.6f}')

t0 = monotonic()
good = [r for r, x in sets if r in addmulconcat(x[::-1], r)]
print(f'addmulconcat, with target: {monotonic() - t0 :0.6f}')

print('Part 2', sum(good))