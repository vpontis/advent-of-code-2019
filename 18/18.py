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
# file_name = './18.txt'
file_name = './181.txt'
# file_name = './182.txt'
# file_name = './183.txt'

grid = {}
elem_to_position = {}

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char in string.ascii_lowercase or char in string.ascii_uppercase or char == '@':
                elem_to_position[char] = (x, y)

# print(f'{numbers=}')

print_dict_grid(grid)

position = [(x, y) for (x, y), val in grid.items() if val == '@'][0]

key_to_position = {}
door_to_position = {}

for (x, y), val in grid.items():
    if val in string.ascii_lowercase:
        key_to_position[val] = (x, y)
    if val in string.ascii_uppercase:
        door_to_position[val] = (x, y)

pprint(f'{key_to_position=}')
pprint(f'{door_to_position=}')

order = []
for upper, lower in zip(string.ascii_uppercase, string.ascii_lowercase):
    order.extend([lower, upper])
order.reverse()
order.append('@')

final_position = None

for elem in order[:]:
    if elem in elem_to_position and not final_position:
        final_position = elem_to_position[elem]
    elif elem not in elem_to_position:
        order.remove(elem)

print(final_position)
pprint(order)


def get_next_nodes(position, seen_nodes):
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    next_nodes = []

    x, y = position
    for (xd, yd) in deltas:
        new_position = x + xd, y + yd

        if new_position not in grid:
            continue

        val = grid[new_position]
        if val == '#':
            continue

        if new_position in seen_nodes:
            continue

        next_nodes.append(new_position)

    return next_nodes


def navigate_to(position: Position, next_position: Position):
    # print(f'{position=} {next_elem=}')
    # bfs to find the shortest path, then find all things on that path

    levels = 0
    queue = [position]
    seen_nodes = set([position])

    while True:
        # print(f'{next_position=} {queue=} {levels=}')
        levels += 1

        _queue = []

        for node in queue:
            next_nodes = get_next_nodes(node, seen_nodes)

            for next_node in next_nodes:
                seen_nodes.add(next_node)

            if next_position in next_nodes:
                return levels

            _queue.extend(next_nodes)

        queue = _queue


lower_to_upper = {
    lower: upper
    for upper, lower in zip(string.ascii_uppercase, string.ascii_lowercase)
}

steps = 0

# order = ['a', 'A', 'b', 'B', 'c', 'd', 'e', 'E', 'f']
# for c in order:
#     next_position = elem_to_position[c]
#     steps += navigate_to(position, next_position)
#     position = next_position
#
# print(steps)

# order.pop(0)
#
# while order:
#     next_elem = order.pop(0)
#
#     # Get path to next thing
#     _steps, _position, found = navigate_to(final_position, next_elem)
#
#     for f in found:
#         # f is string
#         if f in order:
#             # you can only see the door after you have seen the key
#
#             # you can only get the key before you have been thru the door
#             if f in string.ascii_lowercase:
#                 if f.upper() not in order:
#                     print('found  key', f)
#                     order.remove(f)
#             if f in string.ascii_uppercase:
#                 if f.lower() in order:
#                     print('found door', f)
#                     order.remove(f)
#
#     print('found     ', next_elem)
#
#     steps += _steps
#     final_position = _position
#
#     # print(steps, final_position)
#
# print(steps)

order.reverse()
print(order)


def get_options(position: Position, keychain):
    # a key is an option if you can see the key and door

    levels = 0
    queue: List[Position] = [position]
    seen_nodes = set([position])

    doors = set()
    keys = set()

    while queue:
        levels += 1
        _queue = []

        for node in queue:
            val = grid[node]

            if val in string.ascii_uppercase and val not in keychain:
                doors.add(val)
                continue

            if val in string.ascii_lowercase and val not in keychain:
                keys.add(val)
                continue

            next_nodes = get_next_nodes(node, seen_nodes)
            for n in next_nodes:
                seen_nodes.add(n)

            _queue.extend(next_nodes)

        queue = _queue

    options = list(keys)
    for door in doors:
        if door.lower() in keychain:
            options.append(door)

    # print(f'{options=}')
    return options


pair_to_distance = {}
for i, a in enumerate(order):
    for b in order[i:]:
        if a == b:
            continue

        steps = navigate_to(elem_to_position[a], elem_to_position[b])

        pair_to_distance[(a, b)] = steps
        pair_to_distance[(b, a)] = steps

pprint(pair_to_distance)

steps = 0
keychain = set()

elem = '@'

print(order)

num_options = 0

seen_funcs = {}

num_calls = 0

# raise Exception('')
all_opts = set()


def get_steps(elem: str, keychain: set):
    global num_calls
    global all_opts

    num_calls += 1

    if set(order) == keychain:
        return 0

    key = (elem, tuple(keychain))
    if key in seen_funcs:
        return seen_funcs[key]

    start = elem_to_position[elem]
    options = get_options(start, keychain)

    # print(f'fuck {keychain}')
    # print(f'yea {options}')

    option_to_distance = {}

    for option in options:
        to_option = pair_to_distance[(elem, option)]
        _keychain = keychain.copy()
        _keychain.add(option)

        option_to_distance[option] = get_steps(option, _keychain) + to_option

    dist = min(option_to_distance.values())
    seen_funcs[key] = dist

    if num_calls % 10000 == 0:
        print(num_calls, len(keychain), dist, elem)

    return dist

    # print(option_to_distance)


# print('starting stepper')
# print(get_steps(elem, set('@')))

first_elem = ('@', set(['@']), 0)


def get_key(elem, keychain, steps):
    return elem, tuple(keychain), steps


seen_to_steps = {
}

queue = collections.deque([first_elem])

while queue:
    print(len(queue))

    [elem, keychain, steps] = queue.popleft()

    key = (elem, tuple(keychain))
    if seen_to_steps.get(key, 1000000) < steps:
        continue
    else:
        seen_to_steps[key] = steps

    if keychain == set(order):
        break

    options = get_options(elem_to_position[elem], keychain)

    for option in options:
        to_option = pair_to_distance[(elem, option)]

        _keychain = keychain.copy()
        _keychain.add(option)

        _steps = steps + to_option
        key = (option, tuple(_keychain))
        if seen_to_steps.get(key, 1000000) < _steps:
            continue

        queue.append((option, _keychain, _steps))
