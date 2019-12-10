import math
from collections import Counter, defaultdict, namedtuple
import pprint
from typing import NamedTuple


def is_between(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) != 0:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True


def can_asteroid_see(station, looking_for, positions):
    positions = [position for position in positions if position != station and position != looking_for]
    for position in positions:
        if is_between(station, looking_for, position):
            return False

    return True


Point = namedtuple('Point', ['x', 'y'])


def tryrun(grid):
    asteroid_positions = []

    for x in range(len(grid)):
        for y in range(len(grid[1])):
            # print(x, y, grid[y][x])
            if grid[y][x] == '#':
                asteroid_positions.append(Point(x, y))

    position_to_can_see = {}

    for asteroid_position in asteroid_positions:
        can_see = 0

        for asteroid in asteroid_positions:
            if asteroid_position == asteroid:
                continue

            positions = [
                position
                for position in asteroid_positions
                if position != asteroid and position != asteroid_position
            ]

            if can_asteroid_see(asteroid, asteroid_position, positions):
                can_see += 1

        position_to_can_see[asteroid_position] = can_see

    for position, can_see in position_to_can_see.items():
        if can_see > 300:
            print(position, can_see)


def tryvaporize(grid):
    station_position = Point(31, 20)
    # station_position = Point(11, 13)

    num_vaporized = 0

    asteroid_positions = []

    for x in range(len(grid)):
        for y in range(len(grid[1])):
            # print(x, y, grid[y][x])
            if grid[y][x] == '#':
                asteroid_positions.append(Point(x, y))

    asteroid_positions = [
        position for position in asteroid_positions
        if position != station_position]

    position_to_angle = {}

    for position in asteroid_positions:
        if position.x == station_position.x:
            if position.y < station_position.y:
                angle = 0
            else:
                angle = math.pi
        elif position.y == station_position.y:
            if position.x > station_position.x:
                angle = math.pi / 2
            else:
                angle = math.pi * 3 / 2
        else:
            x_diff = position.x - station_position.x
            y_diff = position.y - station_position.y

            if x_diff > 0:
                if y_diff < 0:
                    angle = math.atan(abs(x_diff / y_diff))
                else:
                    angle = math.atan(abs(y_diff / x_diff)) + math.pi / 2
            else:
                if y_diff > 0:
                    angle = math.atan(abs(x_diff / y_diff)) + math.pi
                else:
                    angle = math.atan(abs(y_diff / x_diff)) + math.pi * 3 / 2

        position_to_angle[position] = angle

    can_sees = [
        asteroid for asteroid in asteroid_positions
        if can_asteroid_see(station_position, asteroid, asteroid_positions)
    ]

    while can_sees:
        can_sees = [
            asteroid for asteroid in asteroid_positions
            if can_asteroid_see(station_position, asteroid, asteroid_positions)
        ]

        sorted_can_sees = sorted(can_sees, key=lambda ast: position_to_angle[ast])

        for ast in sorted_can_sees:
            num_vaporized += 1

            print('vaporize', num_vaporized, ast, position_to_angle[ast])
            asteroid_positions.remove(ast)

            if num_vaporized == 200:
                print(ast.x * 100 + ast.y)
                return


filename = './10.txt'
# filename = './101.txt'

with open(filename) as f:
    lines = [l.rstrip('\n') for l in f]

    grid = []
    for line in lines:
        grid.append(line)

    tryvaporize(grid)
