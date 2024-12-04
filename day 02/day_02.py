

def pairwise(coll):
    iter_col = iter(coll)
    mem = next(iter_col)
    for itm in iter_col:
        yield mem, itm
        mem = itm


def deltas(line):
    return [a-b for a, b in pairwise(line)]


def same_sign(delta):
    signs = [x//(abs(x) or 1) for x in delta]
    return all(x == 1 for x in signs) or all(x == -1 for x in signs)


def gen_variants(nums):
    variants = []
    for i in range(len(nums)):
        c = nums[:]
        del c[i]
        variants.append(c)
    return tuple(variants)


lines = [[int(x) for x in line.split()] for line in open('input', 'r').read().splitlines()]

# part 1

good_lines = [same_sign(deltas(line)) and all(1 <= abs(x) <= 3 for x in deltas(line)) for line in lines]
print("Part One", good_lines.count(True))

# part two

new_lines = [gen_variants(line) for line in lines]
good_lines = [
    any(same_sign(deltas(variant)) and all(1 <= abs(x) <= 3 for x in deltas(variant)) for variant in variants) for variants in new_lines
]
print("Part Two", good_lines.count(True))
