import itertools
from collections import defaultdict
from pprint import pprint
from typing import Union, List

from intcode.computer import Computer
from util import print_dict_grid

grid_size = 1000

grid = {}


def get_val_at(x, y):
    if x < 0 or y < 0:
        return 0

    if grid.get((x, y)) is not None:
        return grid[(x, y)]

    computer = Computer.parse_input('19.txt')

    computer.add_input(x)
    computer.add_input(y)

    (is_done, val) = computer.run()

    grid[(x, y)] = val

    return val


# for x in range(grid_size):
#     print(x)
#     for y in range(grid_size):
#         computer = Computer.parse_input('19.txt')
#
#         val = get_val_at(computer, x, y)
#         grid[(x, y)] = val
#
# print_dict_grid(grid)
# print(len([val for val in grid.values() if val == 1]))


def trace_bottom_diagonal():
    position = (0, 1500)

    while True:
        val = get_val_at(position[0], position[1])

        print(position, val)

        if val == 1:
            # check if good
            other_corner = position[0] + 99, position[1] - 99
            print(position, other_corner)
            __val = get_val_at(other_corner[0], other_corner[1])

            if __val:
                is_good = check_good(position[0], position[1] - 99)
                print('checking good')

                if is_good:
                    for i in range(5):
                        for j in range(5):
                            _is_good = check_good(position[0] - i, position[1] - 99 - j)
                            if _is_good:
                                print('even better', position[0] - i, position[1] - 99 - j)

                    print('fuck')
                    print(position)
                    (x, y) = position
                    print(x * 10_000 + y)
                    return (x, y)

            position = position[0], position[1] + 1
        else:
            position = position[0] + 1, position[1]


def check_good(x, y):
    for i in range(100):
        for j in range(100):
            position = (x + i, y + j)
            val = get_val_at(position[0], position[1])

            if val != 1:
                return False

    return True


def print_grid_section(best, buffer=100):
    x0, y0 = best

    x_min = x0 - buffer // 2
    x_max = x0 + buffer + 5
    y_min = y0 - buffer // 2
    y_max = y0 + buffer + 5

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            get_val_at(x, y)

    mini_grid = {
        (x, y): val
        for (x, y), val in grid.items()
        if x_min < x < x_max and y_min < y < y_max
    }
    print_dict_grid(mini_grid)


best = trace_bottom_diagonal()
print('best')
print_grid_section(best, 100)

# one_positions = [
#     position
#     for position, val in grid.items()
#     if val == 1
# ]
#
# one_positions = sorted(one_positions, key=lambda p: p[0] + p[1])
#
#
#
#
# for (x, y) in one_positions:
#     # check fits
#     is_good = check_good(x, y)
#
#     if is_good:
#         print(x * 10_000 + y)
