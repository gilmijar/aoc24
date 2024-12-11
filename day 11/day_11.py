from math import log10
from array import array
from multiprocessing import Pool
from itertools import chain
from time import monotonic as mono


def blink(stones):
    new_stones = array('Q')  # unsigned long long (8 bytes int)
    for stn in stones:
        if stn == 0:
            new_stones.append(1)
        elif int(log10(stn)) % 2 == 1:  # even-digit numbers will have odd log10 integer part
            new_stones.extend(
                divmod(stn, 10**((int(log10(stn))+1)//2))
            )
        else:
            new_stones.append(stn * 2024)
    return new_stones


def reblink(stone):
    t0 = mono()
    stones = array('Q')
    stones.append(stone)
    for i in range(25):
        stones = blink(stones)
        if i % 10 == 0:
            print(stone, i, mono() - t0)
            t0 = mono()
    return stones


# filename = 'test'
filename = 'input'

data = open(filename, 'r').read().strip().split()
stones = [int(st) for st in data]
final_stones = sum(
    len(part) for part in Pool(8).imap_unordered(reblink, stones, chunksize=2)
)

print(final_stones)
