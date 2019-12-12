import itertools
import re
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

Point = namedtuple('Point', ['x', 'y', 'z'])


def parse_positions(grid: List[List[str]], point_val: str) -> List[Point]:
    points = []

    print(len(grid))
    print(len(grid[0]))
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == point_val:
                points.append(Point(c, r))

    return points


planet_to_velocity_x = defaultdict(int)
planet_to_velocity_y = defaultdict(int)
planet_to_velocity_z = defaultdict(int)

num_steps = 1000


# num_steps = 10

class Planet:
    vx = 0
    vy = 0
    vz = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def update_velocity(self, point):
        if self.x < point.x:
            self.vx += 1
            point.vx -= 1
        elif self.x > point.x:
            self.vx -= 1
            point.vx += 1

        if self.y < point.y:
            self.vy += 1
            point.vy -= 1
        elif self.y > point.y:
            self.vy -= 1
            point.vy += 1

        if self.z < point.z:
            self.vz += 1
            point.vz -= 1
        elif self.z > point.z:
            self.vz -= 1
            point.vz += 1

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def get_energy(self):
        ke = sum([abs(val) for val in [self.x, self.y, self.z]])
        pe = sum([abs(val) for val in [self.vx, self.vy, self.vz]])

        return ke * pe

    def get_state(self):
        return [self.x, self.y, self.z, self.vx, self.vy, self.vz]

    def __repr__(self):
        return f'<Planet {self.x=} {self.y=} {self.z=} {self.vx=} {self.vy=} {self.vz=}' \
               f' {self.get_energy()=} />'


def tryrun(planets: List[Planet]):
    states = set()

    state = []
    for p in planets:
        state.extend(p.get_state())
    states.add(tuple(state))

    for i in range(2772 * 100000000):
        # update velocity
        for p1_idx, p1 in enumerate(planets):
            for p2 in planets[p1_idx + 1:]:
                p1.update_velocity(p2)

        # apply velocities
        for p in planets:
            p.update_position()

        state = []
        for p in planets:
            state.extend(p.get_state())

        state = tuple(state)

        if i % 100000 == 0:
            xs = [p.x for p in planets]
            print(xs)
            for p in planets:
                print(p)
            max_x = max([p.x for p in planets])
            min_x = min([p.x for p in planets])
            print(max_x, min_x)
            print(i)

        if state in states:
            print(states)
            print('did it', i)
            return

        states.add(state)

    state = []
    for p in planets:
        state.extend(p.get_state())

    state = tuple(state)
    pprint(state)

    print(states)
    print(list(states)[0])
    print(len(list(states)[0]))
    energies = [p.get_energy() for p in planets]
    for planet in planets:
        print(planet)
    print(sum(energies))


# file_name = './12.txt'
file_name = './121.txt'

regex = '.*x=(-?\d+), y=(-?\d+), z=(-?\d+).*'

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]

    planets = []

    for line in lines:
        print(line)
        x = int(re.match(regex, line).group(1))
        y = int(re.match(regex, line).group(2))
        z = int(re.match(regex, line).group(3))
        planet = Planet(x, y, z)
        planets.append(planet)

    # grid = [list(line) for line in lines]
    # pprint(grid)

    tryrun(planets)
