import itertools
from collections import defaultdict, namedtuple
from pprint import pprint
from typing import List, Tuple, Optional
from intcode.computer import Computer

computer = Computer.parse_input('13.txt')
computer.numbers[0] = 2

# 0 is black, 1 is white
# grid_size = 1000 * 10
grid_size = 100 * 10
grid = []
for x in range(grid_size):
    row = [0] * grid_size
    grid.append(row)


# row - y
# col - x


# print(numbers)

i = 0
paddle_x = None
ball_x = None
ball_velocity = 0

ball_path = []


def get_input():
    global ball_x
    global paddle_x

    joystick = 0

    if paddle_x < ball_x:
        joystick = 1
    elif paddle_x > ball_x:
        joystick = -1

    return joystick


computer.get_input = get_input

panels = defaultdict(int)
score = 0

while not computer.is_done:
    (is_done, x) = computer.run()
    if is_done:
        break

    (_, y) = computer.run()
    (_, tile_id) = computer.run()

    if x == -1 and y == 0:
        score = tile_id
        print('score---', score)
    elif tile_id == 3:
        paddle_x = x
    elif tile_id == 4:
        ball_x = x

num_blocks = len([tile for tile in panels.values() if tile == 2])
print(num_blocks)
