import itertools
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional


def parse_opcode(opcode: int):
    opcode_str = str(opcode)
    code = int(opcode_str[-2:])

    if code == 99:
        return {'code': code, 'modes': []}

    modes_str = opcode_str[:- 2]

    padded = modes_str.zfill(4)
    modes = list(padded)[::-1]
    return {'code': code, 'modes': modes}


def get_vals(numbers: List[int], position: int, modes: List[str], num_vals: int, relative_base: int):
    vals = []

    for i in range(num_vals):
        arg = numbers[position + i]

        if modes[i] == "0":
            val = numbers[arg]
        elif modes[i] == "1":
            val = arg
        elif modes[i] == "2":
            val = numbers[relative_base + arg]

        vals.append(val)

    destination = numbers[position + num_vals]
    if modes[num_vals] == "2":
        destination = relative_base + numbers[position + num_vals]

    vals.append(destination)

    return vals


def run_operation(
        numbers: List[int], position: int, inputs: List[int],
        relative_base: int
) -> Tuple[Optional[int], Optional[int], int]:
    code_info = parse_opcode(numbers[position])
    code = code_info['code']
    modes = code_info['modes']
    # print(code, position, numbers)

    if code == 99:
        return None, None, relative_base

    # add / multiply
    if code in [1, 2]:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2, relative_base)

        if code == 1:
            result = val1 + val2
        else:
            result = val1 * val2

        numbers[destination] = result
        return position + 4, None, relative_base

    # get input
    if code == 3:
        [destination] = get_vals(numbers, position + 1, modes, 0, relative_base)

        num_input = inputs.pop(0)

        numbers[destination] = num_input
        return position + 2, None, relative_base

    # print output
    if code == 4:
        [val1, _destination] = get_vals(numbers, position + 1, modes, 1, relative_base)
        return position + 2, val1, relative_base

    # jump if non-zero
    if code == 5:
        [val1, val2, _destination] = get_vals(numbers, position + 1, modes, 2, relative_base)
        should_jump = val1 != 0
        if should_jump:
            return val2, None, relative_base
        return position + 3, None, relative_base

    # jump if zero
    if code == 6:
        [val1, val2, _destination] = get_vals(numbers, position + 1, modes, 2, relative_base)
        should_jump = val1 == 0
        if should_jump:
            return val2, None, relative_base
        return position + 3, None, relative_base

    # compare - less than
    if code == 7:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2, relative_base)
        numbers[destination] = 1 if val1 < val2 else 0
        return position + 4, None, relative_base

    # compare - equals
    if code == 8:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2, relative_base)
        numbers[destination] = 1 if val1 == val2 else 0
        return position + 4, None, relative_base

    # update relative base
    if code == 9:
        [val1, _destination] = get_vals(numbers, position + 1, modes, 1, relative_base)
        return (position + 2, None, relative_base + val1)

    print('fucking code', code)
    raise Exception('fuck')


Point = namedtuple('Point', ['x', 'y'])

DIRECTIONS = ['up', 'right', 'down', 'left']


class Amp:
    position: int = 0
    is_done: bool = False
    relative_base: int = 0
    coordinate: Point = Point(1000, 1000)
    direction = 'up'

    def __init__(self, name, numbers, inputs):
        self.name = name
        self.numbers = numbers
        self.inputs = inputs[:]
        self.all_inputs = inputs[:]

    def run(self) -> Tuple[bool, Optional[int]]:
        # print(f'{self.name=} {self.position=} {self.inputs=}')

        if self.is_done:
            raise Exception('fuc')

        while self.position is not None:
            result = run_operation(
                self.numbers,
                self.position,
                self.inputs,
                self.relative_base,
            )

            (position, output, new_relative_base) = result

            self.position = position
            self.relative_base = new_relative_base

            if output is not None:
                return False, output

        self.is_done = True
        return True, None

    def add_input(self, num: int):
        self.inputs.append(num)
        self.all_inputs.append(num)

    def __repr__(self):
        return f'<Amp {self.name=} {self.inputs=}>'


# 0 is black, 1 is white
# grid_size = 1000 * 10
grid_size = 1000 * 10
grid = []
for x in range(grid_size):
    row = [0] * grid_size
    grid.append(row)


# row - y
# col - x

def tryrun(numbers):
    # print(numbers)
    numbers = numbers + ([0] * 10000)

    amp = Amp(0, numbers, [1])

    panels_painted = set()

    while not amp.is_done:
        result = amp.run()
        (is_done, paint_color) = result

        if is_done:
            break

        panels_painted.add(amp.coordinate)
        grid[amp.coordinate.y][amp.coordinate.x] = paint_color

        result = amp.run()
        (is_done, turn_direction) = result

        direction_idx = DIRECTIONS.index(amp.direction)
        if turn_direction == 1:
            new_direction = DIRECTIONS[(direction_idx + 1) % 4]
        elif turn_direction == 0:
            new_direction = DIRECTIONS[(direction_idx - 1) % 4]
        else:
            raise Exception('Bad output')

        amp.direction = new_direction

        x = amp.coordinate.x
        y = amp.coordinate.y

        if amp.direction == 'up':
            amp.coordinate = Point(x, y - 1)
        if amp.direction == 'down':
            amp.coordinate = Point(x, y + 1)
        if amp.direction == 'right':
            amp.coordinate = Point(x + 1, y)
        if amp.direction == 'left':
            amp.coordinate = Point(x - 1, y)

        amp.add_input(grid[amp.coordinate.y][amp.coordinate.x])
        # print(amp.direction, turn_direction, amp.coordinate)

    min_x = min([min(row.index(1) for row in grid if 1 in row)])

    for i in range(10000):
        if 1 in grid[i]:
            print(i)
            break
    print(min_x)

    for row in grid[1000:1200]:
        print(
            ''.join(['I' if i == 1 else ' ' for i in row[1000:1200]])
        )

    # print('Done')
    # print(len(panels_painted))


with open('./11.txt') as f:
    lines = [l.rstrip('\n') for l in f]
    line = lines[0]

    numbers = [int(num) for num in line.strip().split(',')]
    tryrun(numbers)
