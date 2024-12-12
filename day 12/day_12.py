from collections import defaultdict
UP = -1
LEFT = -1j

filename = 'test'
# filename = 'input'
data = open(filename, 'r').read().strip().splitlines()

results = defaultdict(lambda: {'area': 0, 'perimeter': 0})

for r, row in enumerate(data):
    plots_on_last_line = defaultdict(set)
    plot_on_the_left = None
    for c, plant in enumerate(row):
        position = r + c * 1j
