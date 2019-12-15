import itertools
import re
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

Point = namedtuple('Point', ['x', 'y', 'z'])

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

    def clone(self):
        return Planet(self.x, self.y, self.z)

    def get_energy(self):
        ke = sum([abs(val) for val in [self.x, self.y, self.z]])
        pe = sum([abs(val) for val in [self.vx, self.vy, self.vz]])

        return ke * pe

    def get_state(self):
        return [self.x, self.y, self.z, self.vx, self.vy, self.vz]

    def __repr__(self):
        return f'<Planet {self.x=} {self.y=} {self.z=} {self.vx=} {self.vy=} {self.vz=}' \
               f' {self.get_energy()=} />'


def triag(n: int):
    '''efficiently memoized recursive function, returns a Fibonacci number'''
    return n * (n + 1) // 2


def ground_covered_in_turns(v0: int, turns: int, delta_v: int):
    return triag(turns) * delta_v + v0 * turns

    # velocity = v0
    # position = 0
    #
    # print(f'{velocity=} {turns=} {delta_v=}')
    #
    # for i in range(turns):
    #     print(f'{i=} {position=} {velocity=} {triag(i)=}')
    #
    #     velocity += delta_v
    #     position += velocity
    #
    # print('\n\n')
    # print(position, triag(turns) * delta_v + v0 * turns)
    # return position


def turns_to_cover_ground(v0, delta_v, ground):
    for i in range(1000):
        if abs(ground_covered_in_turns(v0, i, delta_v)) > abs(ground):
            return i

    raise Exception(f'didnt cover {v0=} {delta_v=} {ground=}')


# velocity 0
# increment 1
# 1 -> 1
# 2 -> 3
# 3 -> 6
# 4 -> 10

# velocity 1
# increment 1
# 1 -> 2, 2
# 2 -> 4, 3
# 3 -> 7, 4
# 4 -> 11, 5

# velocity 2
# increment 1
# 1 -> 3, 3
# 2 -> 6, 4
# 3 -> 10, 5
# 4 -> 15, 6

# velocity 0
# increment 2
# 1 -> 2, 2
# 2 -> 6, 4
# 3 -> 12, 6
# 4 ->  20, 8


def time_to_intersect(planets: List[Planet], dimension: str, velocity: str):
    sorted_planets = sorted(planets, key=lambda p: getattr(p, dimension))

    [out1, in1, in2, out2] = sorted_planets
    [out1v, in1v, in2v, out2v] = [getattr(p, velocity) for p in sorted_planets]
    [out1d, in1d, in2d, out2d] = [getattr(p, dimension) for p in sorted_planets]

    ttis = [
        # right
        turns_to_cover_ground(out1v, 3, abs(out1d + in1d) / 2),
        turns_to_cover_ground(in1v, 1, abs(in1d + in2d) / 2),
        turns_to_cover_ground(in2v, -1, abs(in2d + out2d) / 2),

        # left
        turns_to_cover_ground(out2v, -3, abs(in2d + out2d) / 2),
        turns_to_cover_ground(in2v, -1, abs(in1d + in2d) / 2),
        turns_to_cover_ground(in1v, 1, abs(out1d + in1d) / 2),
    ]

    min_tti = min(ttis)
    return min_tti


def update_until_intersection(planets: List[Planet], dimension: str, velocity: str):
    turns = time_to_intersect(planets, dimension, velocity)

    sorted_planets = sorted(planets, key=lambda p: getattr(p, dimension))

    for (planet, delta_v) in zip(sorted_planets, [3, 1, -1, -3]):
        prev_pos = getattr(planet, dimension)
        prev_v = getattr(planet, velocity)

        new_pos = prev_pos + ground_covered_in_turns(prev_v, turns, delta_v)
        new_v = prev_v * turns

        setattr(planet, dimension, new_pos)
        setattr(planet, velocity, new_v)

    return turns


def get_period(planets: List[Planet], dimension, velocity):
    def get_state():
        state = []
        for p in planets:
            state.extend([getattr(p, dimension), getattr(p, velocity)])
        return tuple(state)

    init_state = get_state()

    nums = []

    for i in range(10000000):
        # update velocity
        for p1_idx, p1 in enumerate(planets):
            for p2 in planets[p1_idx + 1:]:
                p1.update_velocity(p2)

        # apply velocities
        for p in planets:
            p.update_position()

        state = get_state()
        if state == init_state:
            nums.append(i)

            if len(nums) > 2:
                print(nums)
                for num1, num2 in zip(nums, nums[1:]):
                    print(num2 - num1)
                return nums[0], nums[1] - nums[0]

    raise Exception('didnt get the period')


ten_mil = 10_000_000


def tryfast(planets: List[Planet]):
    # x0, vx = get_period([p.clone() for p in planets], 'x', 'vx')
    # print(f'{x0=} {vx=}')
    # y0, vy = get_period([p.clone() for p in planets], 'y', 'vy')
    # print(f'{y0=} {vy=}')
    # z0, vz = get_period([p.clone() for p in planets], 'z', 'vz')
    # print(f'{z0=} {vz=}')

    x0 = 268295
    vx = 268296
    
    y0 = 113027
    vy = 113028
    
    z0 = 231613
    vz = 231614

    import math
    
    print(f'{math.gcd(vx, vy)=}')
    print(f'{math.gcd(vy, vz)=}')
    print(f'{math.gcd(vx, vz)=}')

    print(vx * vy * vz)
    print(int(vx * vy * vz / math.gcd(vx, vy) / math.gcd(vy, vz) / math.gcd(vz, vx) * 2))
    return

    print('got periods!!')

    ys = set()
    zs = set()

    for i in range(0, 1_000_000_000):

        x = x0 + vx * i
        y = y0 + vy * i
        z = z0 + vz * i

        ys.add(y)
        zs.add(z)

        if x in ys and x in zs:
            print(x)
            return

        if i % 1_000_000 == 0:
            print(i)
            min_val = min(x, y, z)

            ys = set([val for val in ys if val >= min_val])
            zs = set([val for val in zs if val >= min_val])
            print(min_val)


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
            print('ttix', time_to_intersect(planets, 'x', 'vx'))
            print('ttiy', time_to_intersect(planets, 'y', 'vy'))
            print('ttiz', time_to_intersect(planets, 'z', 'vz'))
            max_x = max([p.x for p in planets])
            min_x = min([p.x for p in planets])
            print(max_x, min_x)
            print(i)

        if state in states:
            print('did it', i)
            return

        states.add(state)

    for planet in planets:
        print(planet)


# file_name = './12.txt'
file_name = './121.txt'

regex = '.*x=(-?\d+), y=(-?\d+), z=(-?\d+).*'

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]

    planets = []

    for line in lines:
        x = int(re.match(regex, line).group(1))
        y = int(re.match(regex, line).group(2))
        z = int(re.match(regex, line).group(3))
        planet = Planet(x, y, z)
        planets.append(planet)

    # tryrun(planets)
    for p in planets:
        print(p)

    tryfast(planets)
