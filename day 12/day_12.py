from dataclasses import dataclass
from collections import defaultdict
from time import monotonic as mono


class Plot:
    sides = (-1j, -1)

    def __init__(self, spec):
        self.plant = spec.plant
        self.position = spec.position
        self.members: set = {spec.position}
        self.perimeter: int = 4
        self.last: complex = spec.position
        # for P2
        self.walls = 4

    @property
    def area(self):
        return len(self.members)

    @property
    def price(self):
        return self.area * self.perimeter

    @property
    def rebate_price(self):
        return self.area * self.walls

    def is_neighbor(self, item):
        if item.plant != self.plant:
            return False
        for side in self.sides:
            adjacent = item.position + side
            if adjacent in self.members:
                return True
        return False

    def __contains__(self, item):
        if item.plant != self.plant:
            return False
        return item in self.members

    def accept(self, item):
        self.members.add(item.position)
        touch_facets = len(
            {item.position + side for side in self.sides} & self.members
        )
        # touching facets of item don't add to perimieter,
        # and also take away from old perim.
        self.perimeter += 4 - 2*touch_facets
        self.last = item.position
        kernel = [
            1, -2, 1,
            -2, 2, 0
        ]

        self.walls += self._apply_kernel(self.last, kernel)

    def merge(self, other):
        # we assume that merging will always occur between
        # a plot in same row (to the left of current item)
        # and a plot in the previous row (right below the item)
        self.perimeter += other.perimeter - 2
        self.members.update(other.members)
        self.walls += other.walls
        merge_kernel = [
            0, -2, 2,
            0,  0, 0
        ]
        self.walls += self._apply_kernel(self.last, merge_kernel)

    def _apply_kernel(self, position, kernel):
        offsets = [
            -1-1j, -1, -1+1j,
              -1j,  0,    1j
        ]
        patch = [1 if ((position + off) in self.members) else -1 for off in offsets]
        if patch[0] == -1:
            k2 = [
                -1, -2, 1,
                -2, 2, 0
            ]
            return sum(ker * pat for ker, pat in zip(k2, patch))
        return sum(ker * pat for ker, pat in zip(kernel, patch))

    def __str__(self):
        return f'{self.plant}: {self.area=}, {self.perimeter=}, {self.walls=}' \
               f', pos=({self.position.real:n}, {self.position.imag:n})' \
               f', last=({self.last.real:n}, {self.last.imag:n})'


@dataclass
class Plant:
    plant: str
    position: complex


if __name__ == '__main__':
    t00 = mono()
    filename = 'test'
    # filename = 'input'
    data = open(filename, 'r').read().strip().splitlines()

    all_plots = set()

    for r, row in enumerate(data):
        for c, plant in enumerate(row):
            specimen = Plant(plant, r + c*1j)
            neighbors = [plot for plot in all_plots if plot.is_neighbor(specimen)]
            if not neighbors:
                all_plots.add(Plot(specimen))
            elif len(neighbors) == 1:
                neighbors[0].accept(specimen)
            elif len(neighbors) == 2:
                neighbors[0].accept(specimen)
                neighbors[0].merge(neighbors[1])
                all_plots.remove(neighbors[1])
            else:
                raise Exception('Too many neighbors!')
    print(f'Elapsed total time: {mono() - t00:0.3f} sec')
    print(*sorted(all_plots, key= lambda x: (x.position.real, x.position.imag)), sep='\n')
    print(sum(p.price for p in all_plots))
    print(sum(p.rebate_price for p in all_plots))
    print(len(all_plots))
