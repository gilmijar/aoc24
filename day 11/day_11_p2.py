from math import log10
from array import array
from multiprocessing import Pool
from functools import partial
from time import monotonic
from sys import argv


def blink(stones):
    new_stones = []  # array('Q')  # unsigned long long (8 bytes int)
    for stn in stones:
        if stn == 0:
            new_stones.append(1)
        elif int(log10(stn)) % 2 != 1:  # even-digit numbers will have odd log10 integer part
            new_stones.append(stn * 2024)
        else:
            new_stones.extend(
                divmod(stn, 10 ** ((int(log10(stn)) + 1) // 2))
            )
    return new_stones


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
    BLINKS = int(argv[1]) if len(argv) == 2 else 42
    # filename = 'test'
    filename = 'input'
    data = open(filename, 'r').read().strip().split()
    stones = [int(st) for st in data]
    d = BLINKS
    t0 = monotonic()
    # Expand the list of stones,
    # so that we have more individual stones to feed the recurive counter
    while monotonic() - t0 < 20:
        stones = blink(stones)
        d -= 1
    print(f'Elapsed: {monotonic() - t0} seconds')
    print(BLINKS - d, 'generations.', 'Stones after expansion:', len(stones))
    print('I shall begin commencing...')
    follow_2 = partial(follow_stone, depth=d)
    P = Pool(4)
    t0 = monotonic()
    # final_stones = map(follow_2, stones)  # This is for comparison - single-process
    final_stones = P.imap_unordered(follow_2, stones, 1_000_000)
    print(sum(final_stones))
    print(f'Elapsed: {monotonic() - t0} seconds')

