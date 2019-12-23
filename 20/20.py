import collections
import itertools
import math
import re
import string
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

from util import print_dict_grid

Position = Tuple[int, int]

file_name = './20.txt'
file_name = './201.txt'
# file_name = './202.txt'
# file_name = './203.txt'

grid = {}
elem_to_position = {}

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char

print_dict_grid(grid)

deltas = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

label_to_points = defaultdict(list)
point_to_label = {}

xs = [p[0] for p in grid.keys()]
ys = [p[1] for p in grid.keys()]
max_x = max(xs)
max_y = max(ys)

middle_of_maze = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2

for (x, y), val in grid.items():
    if val != '.':
        continue

    for xd, yd in deltas:
        neighbor = grid.get(((x + xd), (y + yd)))
        if not neighbor:
            continue

        if neighbor in string.ascii_uppercase:
            neighbor2 = grid.get(((x + 2 * xd, y + 2 * yd)))
            if not neighbor2:
                continue

            if neighbor2 in string.ascii_uppercase:
                label = ''.join(sorted([neighbor2, neighbor]))
                print(label)
                label_to_points[label].append((x, y))
                point_to_label[(x, y)] = label, 0

pprint(label_to_points)

start = label_to_points['AA'][0]
end = label_to_points['ZZ'][0]

for label, points in label_to_points.items():
    if len(points) != 2:
        continue

    [p1, p2] = points
    if p1[0] <= 3 or p1[0] >= max_x - 4 or p1[1] <= 3 or p1[1] >= max_y - 4:
        point_to_label[p1] = (label, -1)
        point_to_label[p2] = (label, 1)
    else:
        point_to_label[p2] = (label, -1)
        point_to_label[p1] = (label, 1)


def expand_node(node, allow_warp=True):
    neighbors = []

    x, y, level = node

    for xd, yd in deltas:
        x1, y1 = x + xd, y + yd
        if grid.get((x1, y1)) == '.':
            neighbors.append((x1, y1, level))

    if (x, y) in point_to_label and allow_warp:
        label, ld = point_to_label[(x, y)]

        new_level = level + ld

        if label not in ['AA', 'ZZ'] and new_level >= 0:
            friend = [n for n in label_to_points[label] if (x, y) != n][0]
            neighbors.append((friend[0], friend[1], new_level))

    return neighbors


def get_point_to_point():
    point_to_neighbors = {}

    for point in point_to_label.keys():
        ops = []

        queue = [point]
        seen = set([point])

        steps = 0

        while queue:
            print(point, queue)
            steps += 1

            _q = []

            for n0 in queue:
                neighbors = expand_node(list(n0) + [1], allow_warp=False)

                for neighbor in neighbors:
                    neighbor = neighbor[:2]

                    if neighbor in seen:
                        continue

                    if neighbor in point_to_label:
                        ops.append((neighbor, steps))

                    seen.add(neighbor)
                    _q.append(neighbor)

            queue = _q

        point_to_neighbors[point] = ops

    return point_to_neighbors


point_to_neighbors = get_point_to_point()
pprint(point_to_neighbors)
# raise Exception('e')

pprint(label_to_points)
pprint(point_to_label)
# raise Exception('')

start = start[0], start[1], 0, 0

queue = [start]
seen = {
    start[:3]: 0
}

print(start)

steps = 0

pprint(label_to_points)
pprint(point_to_label)
# raise Exception('')


node_to_path = {
    start: [start]
}


def expand_node_fast(node, allow_warp=True):
    neighbors = []

    level = node[2]
    steps = node[3]

    points = point_to_neighbors[(node[0], node[1])]

    for point, _steps in points:
        label, ld = point_to_label[point]
        new_steps = steps + _steps
        new_level = level + ld

        if label not in ['AA', 'ZZ'] and new_level >= 0:
            neighbors.append((point[0], point[1], new_level, new_steps))

    print('nn', node, neighbors)
    return neighbors


pprint(point_to_neighbors)
while queue:
    node = queue.pop(0)

    neighbors = expand_node_fast(node)
    print('n', neighbors)

    for neighbor in neighbors:
        _steps = neighbor[3]
        point_level = neighbor[:3]

        if seen.get(point_level, 100000) < _steps:
            continue

        seen[point_level] = _steps
        queue.append(neighbor)

        if (neighbor[0], neighbor[1]) == end and neighbor[2] == 0:
            print('ans', neighbor[3])

            pprint(point_to_label)
            pprint(label_to_points)

            print('ans', steps)
            raise Exception('')
