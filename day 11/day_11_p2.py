# It also can solve part 1
from math import log10
from functools import partial
from time import monotonic
from sys import argv
from functools import lru_cache


@lru_cache(30000)
def follow_stone(stone: int, depth: int):
    while stone == 0 or int(log10(stone)) % 2 != 1:  # even-digit numbers will have odd log10 integer part
        if stone == 0:
            stone = 1
        else:
            stone *= 2024
        depth -= 1
        if depth == 0:
            return 1
    if depth == 1:
        return 2
    else:
        a, b = divmod(stone, 10 ** ((int(log10(stone)) + 1) // 2))
        return follow_stone(a, depth-1) + follow_stone(b, depth-1)


if __name__ == '__main__':
    BLINKS = int(argv[1]) if len(argv) == 2 else 25
    # filename = 'test'
    filename = 'input'
    data = open(filename, 'r').read().strip().split()
    stones = [int(st) for st in data]
    d = BLINKS
    t0 = monotonic()
    follow_2 = partial(follow_stone, depth=d)
    final_stones = map(follow_2, stones)
    print(sum(final_stones))
    print(f'Elapsed: {monotonic() - t0} seconds')
