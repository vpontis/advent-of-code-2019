import collections
import itertools
import math
import re
import string
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

from util import print_dict_grid, bfs, BfsNode, Point, MANHATTAN_DELTAS

Position = Tuple[int, int]

file_name = './20.txt'
file_name = './201.txt'
file_name = './202.txt'
# file_name = './203.txt'

grid = {}
elem_to_position = {}

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[Point(x, y)] = char

print_dict_grid(grid)

label_to_points = defaultdict(list)
point_to_label = {}

for point, val in grid.items():
    if val != '.':
        continue

    for d in MANHATTAN_DELTAS:
        neighbor = grid.get(point + d)

        if not neighbor:
            continue

        if neighbor in string.ascii_uppercase:
            neighbor2 = grid.get(point + d * 2)

            if not neighbor2:
                continue

            if neighbor2 in string.ascii_uppercase:
                label = ''.join(sorted([neighbor2, neighbor]))
                print(label)
                label_to_points[label].append(point)
                point_to_label[point] = label

pprint(label_to_points)

start = label_to_points['AA'][0]

start = {
    'data': start,
    'steps': 0,
}

end = label_to_points['ZZ'][0]


def expand_node(node: BfsNode) -> List[BfsNode]:
    neighbors = []

    point = node['data']
    steps = node['steps']

    for delta in MANHATTAN_DELTAS:
        if grid.get(point + delta) == '.':
            neighbors.append(
                {'data': point + delta, 'steps': steps + 1}
            )

    if point in point_to_label:
        label = point_to_label[point]

        if label not in ['AA', 'ZZ']:
            friend = [n for n in label_to_points[label] if point != n][0]
            neighbors.append(
                {'data': friend, 'steps': steps + 1}
            )

    return neighbors


def is_end(node):
    return node == end


result = bfs(start, expand_node, is_end)
print(result)
