from dataclasses import dataclass
from collections import defaultdict


class Plot:
    sides = (-1j, 1j, -1, 1)

    def __init__(self, letter, position):
        self.letter = letter
        self.position = position
        self.members: set = {letter}
        self.perimeter: int = 4
        # idea: store 4 sets of members: facing in each direction

    @property
    def area(self):
        return len(self.members)

    def is_neighbor(self, item):
        for side in sides:
            adjacent = item + side
            if adjacent in self.members:
                return True
        return False

    def __contains__(self, item):
        return item in self.members

    def accept(self, item):
        self.members.add(item)
        touch_facets = len(
            {item + side for side in sides} - self.members
        )
        # touching facets of item don't add to perimieter,
        # and also take away from old perim.
        self.perimeter += 4 - 2*touch_facets

    def merge(self, other: Plot):
        # we assume that merging will always occur between
        # a plot in same row (to the left of current item)
        # and a plot in the previous row (right below the item)
        self.perimeter += other.perimeter - 2
        self.members.update(other.members)


# filename = 'test'
filename = 'input'
data = open(filename, 'r').read().strip().splitlines()

all_plots = defaultdict(set)

for r, row in enumerate(data):
    plots_on_last_line = defaultdict(set)
    plot_on_the_left = None
    for c, plant in enumerate(row):
        position = r + c * 1j
        plots_on_last_line.get(plant, {*()}):
            ...
