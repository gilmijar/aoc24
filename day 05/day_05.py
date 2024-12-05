from functools import partial
from typing import Sequence


def validate(seq: Sequence, the_rule: tuple) -> bool:
    """check if values in seq are in the order that is specified by rule"""
    try:
        a, b = (seq.index(v) for v in the_rule)
    except ValueError:
        # rule doesn't apply - pages in rule are not in the swq
        return True
    return a < b


def filter_rules(seq: tuple, ruleset: list) -> list:
    """return only the rules that apply to the given update"""
    valid_rules = filter(lambda r: r[0] in seq and r[1] in seq, ruleset)
    return list(valid_rules)


# filename = "test_input"
filename = "input"

data = open(filename, "r").read().splitlines()

rules = [tuple(map(int, datum.split("|"))) for datum in data if "|" in datum]
updates = [tuple(map(int, datum.split(","))) for datum in data if "," in datum]

valid_updates = [upd for upd in updates if all(map(lambda rule: validate(upd, rule), rules))]
valid_middles = [upd[len(upd)//2] for upd in valid_updates]
print(sum(valid_middles), '\n')

print("Part Two", '\n')
"""
For each seq:
1. eliminate rules that don't apply
2. find rule without precedent
3. put first term of that rule at the start
4. for each rule make a minimal change to satisfy it.
    * if not already satisfied
    * take the first term out of list
    * put the first term right before the second term
"""
my_rule_filter = partial(filter_rules, ruleset = rules)
invalid_updates = [upd for upd in updates if not all(map(lambda rule: validate(upd, rule), rules))]

fixed_updates = []
for update in map(list, invalid_updates):
    applicable_rules = my_rule_filter(update)
    # lazy-ass fix: go through rules a few times to hopefully fix all that were violated in the first pass
    for _ in range(4):
        for rule in applicable_rules:
            if validate(update, rule):
                continue
            update.insert(update.index(rule[1]), update.pop(update.index(rule[0])))  # this moves the number/page

    fixed_updates.append(update)

# print(*fixed_updates, sep='\n')
fixed_middles = [upd[len(upd)//2] for upd in fixed_updates]
print(sum(fixed_middles), '\n')
