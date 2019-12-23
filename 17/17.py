import itertools
from collections import defaultdict
from pprint import pprint
from typing import Union, List

from intcode.computer import Computer
from util import print_dict_grid

computer = Computer.parse_input('17.txt')
computer.numbers[0] = 2

# print(computer.numbers[0])
# raise Exception('')

# grid = {}
#
# x = 0
# y = 0
#
# while not computer.is_done:
#     is_done, output = computer.run()
#
#     if is_done:
#         break
#
#     out_str = chr(output)
#     print(out_str, end='')
#
#     if output != 10:
#         grid[(x, y)] = out_str
#         x += 1
#     else:
#         x = 0
#         y += 1

grid = {}
with open('171.txt') as file:
    y = 0
    for line in file:
        line = line.strip()
        for x, char in enumerate(line):
            grid[(x, y)] = char

        y += 1

total = 0
xs = [p[0] for p in grid.keys()]
ys = [p[1] for p in grid.keys()]

intersections = []
for i in range(max(xs)):
    for j in range(max(ys)):
        is_intersection = (
                grid.get((i, j), '.') == '#' and
                grid.get((i - 1, j), '.') == '#' and
                grid.get((i + 1, j), '.') == '#' and
                grid.get((i, j + 1), '.') == '#' and
                grid.get((i, j - 1), '.') == '#'
        )

        if not is_intersection:
            continue

        intersections.append((i, j))
        total += i * j

print('\n\n')

# for x, y in intersections:
#     # print('fucj', x, y)
#     grid[(x, y)] = 'O'

print_dict_grid(grid)
print(total)

# Get the path we should take
line_length = 20

path = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'
path = [
    int(c) if c.isdigit() else c
    for c in path.split(',')
]


def expand_path(path):
    new_path = []
    for step in path:
        if type(step) == int:
            new_path.extend([1] * step)
        else:
            new_path.append(step)

    return new_path


def check_functions(path, part_a, part_b, part_c) -> List[str]:
    if len(path) == 0:
        return []

    a_works = path[:len(part_a)] == part_a
    if a_works:
        return ['A'] + check_functions(path[len(part_a):], part_a, part_b, part_c)

    b_works = path[:len(part_b)] == part_b
    if b_works:
        # b_works = check_functions(path[len(part_b):], part_a, part_b, part_c)
        return ['B'] + check_functions(path[len(part_b):], part_a, part_b, part_c)

    c_works = path[:len(part_c)] == part_c
    if c_works:
        # c_works = check_functions(path[len(part_c):], part_a, part_b, part_c)
        return ['C'] + check_functions(path[len(part_c):], part_a, part_b, part_c)

    return []


def compress_segment(segment):
    new_segment = []

    for step in segment:
        if type(step) == int:
            if new_segment and type(new_segment[-1]) == int:
                new_segment[-1] += step
            else:
                new_segment.append(step)
        else:
            new_segment.append(step)

    return new_segment


segment_len_cache = {}


def get_segment_len(segment):
    _segment = tuple(segment)

    if _segment in segment_len_cache:
        return segment_len_cache[_segment]

    segment = compress_segment(segment)

    length = len(','.join(['a' for s in segment]))
    segment_len_cache[_segment] = length
    return length


def compress_path(path: List[Union[str, int]]):
    # Compress into three parts

    # A has to be at the start
    # C has to be at the end
    path = expand_path(path)
    path_len = len(path)

    min_length = 25

    for len_a in range(min_length, path_len):
        part_a = path[:len_a]

        if get_segment_len(part_a) > line_length:
            break

        for len_b in range(min_length, path_len):
            part_b = path[-len_b:]

            if get_segment_len(part_b) > line_length:
                break

            for len_c in range(min_length, path_len - len_b - 1):
                for start in range(len_a, path_len - len_b - len_c):
                    part_c = path[start:start + len_c]

                    if get_segment_len(part_c) > line_length:
                        break

                    print(f'{len_a=} {len_b=} {len_c=} {path_len=}')

                    works = check_functions(path, part_a, part_b, part_c)

                    if works:
                        pprint(compress_segment(part_a))
                        pprint(compress_segment(part_b))
                        pprint(compress_segment(part_c))
                        return part_a, part_b, part_c

    return None


# print(path)
# print(compress_segment(['L', 1, 1, 1, 1, 1, 1, 'L', 1, 1]))

direction_to_v = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
}

directions_r = ['up', 'right', 'down', 'left']


def get_path():
    # initial
    direction = 'up'
    position = (50, 26)

    # assume a start
    path = ['L']
    direction = 'left'

    while True:
        v = direction_to_v[direction]
        new_position = position[0] + v[0], position[1] + v[1]
        can_go_straight = grid.get(new_position) == '#'

        if can_go_straight:
            path.append(1)
            position = new_position
        else:
            # try right
            direction_idx = directions_r.index(direction)
            new_direction = directions_r[(direction_idx + 1) % 4]
            v = direction_to_v[new_direction]
            new_position = position[0] + v[0], position[1] + v[1]
            can_go_straight = grid.get(new_position) == '#'
            if can_go_straight:
                direction = new_direction
                path.append('R')
                continue

            # try left
            direction_idx = directions_r.index(direction)
            new_direction = directions_r[(direction_idx - 1) % 4]
            v = direction_to_v[new_direction]
            new_position = position[0] + v[0], position[1] + v[1]
            can_go_straight = grid.get(new_position) == '#'
            if can_go_straight:
                direction = new_direction
                path.append('L')
                continue

            break

    print('End position', position)
    return path


position = [key for key, val in grid.items() if val == '^']
print(position)

path = get_path()

# turns = [x for x in path if x in ['L', 'R']]
# print('turns', len(turns))
# raise Exception('')

# print(path)
# print(compress_path(path))

part_a = ['L', 12, 'L', 8, 'R', 10, 'R', 10]
part_b = ['R', 10, 'L', 8, 'L', 4, 'R', 10]
part_c = ['L', 6, 'L', 4, 'L', 12]

letter_to_path = {'A': part_a, 'B': part_b, 'C': part_c}

pprint(compress_segment(path))

movement_line = check_functions(path, expand_path(part_a), expand_path(part_b), expand_path(part_c))
print(movement_line)

_path = []
for func in movement_line:
    _path.extend(letter_to_path[func])

# compress_path(path)
# print(check_functions([1, 2, 3, 4, 5, 1, 2, 3], [1, 2, 3], [4, 5], [6]))

inputs = []
for i, func in enumerate(movement_line):
    inputs.append(func)

    if i + 1 != len(movement_line):
        inputs.append(',')

inputs.append('\n')
print('fuck', len(inputs))

for part in [part_a, part_b, part_c]:
    for i, step in enumerate(part):
        inputs.append(step)

        if i + 1 != len(part):
            inputs.append(',')

    inputs.append('\n')

inputs.extend(['n', '\n'])

for inp in inputs:
    if type(inp) == int:
        for c in list(str(inp)):
            computer.add_input(ord(c))
    else:
        computer.add_input(ord(inp))

for inp in inputs:
    if inp != '\n':
        print(inp, end='')
    else:
        print('')

print(computer.inputs)
# computer.inputs = []

while not computer.is_done:
    (is_done, output) = computer.run()
    print(f'{is_done=} {output=}')

print(is_done)
