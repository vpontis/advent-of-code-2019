import itertools
from collections import defaultdict, namedtuple
from pprint import pprint
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
        numbers: List[int], position: int, num_input: Optional[int],
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

        if num_input is None:
            raise Exception('need input')

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
        return position + 2, None, relative_base + val1

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

    def __init__(self, name, numbers, get_input):
        self.name = name
        self.numbers = numbers
        self.get_input = get_input

        self.inputs = []
        self.all_inputs = []

    def run(self) -> Tuple[bool, Optional[int], bool]:
        # print(f'{self.name=} {self.position=} {self.inputs=}')

        if self.is_done:
            raise Exception('fuc')

        while self.position is not None:
            try:
                result = run_operation(
                    self.numbers,
                    self.position,
                    None,
                    self.relative_base,
                )
            except Exception as e:
                if str(e) == 'need input':
                    input_num = self.get_input()
                    result = run_operation(
                        self.numbers,
                        self.position,
                        input_num,
                        self.relative_base,
                    )
                else:
                    raise e

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

def print_panels(panels):
    xs = [p[0] for p in panels.keys()]
    ys = [p[1] for p in panels.keys()]
    print(min(xs), min(ys))

    for r in range(max(ys) + 1):
        for c in range(max(xs) + 1):
            # print(panels[(c, r)] or ' ', end='')
            print((c, r), end='')
        print('')


def tryrun(numbers):
    # print(numbers)
    numbers = numbers + ([0] * 10000)
    numbers[0] = 2

    i = 0
    paddle_x = None
    prev_ball = None

    def get_input():
        joystick = 0
        (bx, by) = prev_ball

        if paddle_x < bx:
            joystick = 1
        elif paddle_x > bx:
            joystick = -1

        return joystick

    amp = Amp(0, numbers, get_input)

    panels = defaultdict(int)

    score = 0

    while not amp.is_done:
        result = amp.run()
        (is_done, x) = result

        if is_done:
            print_panels(panels)
            print(i)

            print('is done/??')
            break

        result = amp.run()
        (is_done, y) = result

        result = amp.run()
        (is_done, tile_id) = result

        # print(x, y, tile_id)

        if x == -1 and y == 0:
            print('score---', score)
            score = tile_id
            continue

        if tile_id == 0:
            continue
        elif tile_id == 1:
            panels[(x, y)] = 1
        elif tile_id == 2:
            panels[(x, y)] = 2
        elif tile_id == 3:
            if paddle_x is not None:
                panels[(paddle_x, y)] = 0

            panels[(x, y)] = 3
            paddle_x = x

        elif tile_id == 4:
            print('balling', (x, y))
            if prev_ball:
                panels[prev_ball] = 0

            panels[(x, y)] = 4

            if not prev_ball:
                print_panels(panels)

            prev_ball = (x, y)

        # print(dict(panels))

        num_blocks = len([tile for tile in panels.values() if tile == 2])
        if i % 100 == 0:
            print('numbs', num_blocks)

        if i > 1000 and num_blocks == 0:
            pprint(dict(panels))
            print('score', score)
            return

        i += 1

    num_blocks = (len([tile for tile in panels.values() if tile == 2]))
    print(num_blocks)

    # print(score)
    # pprint(panels)
    # print(len(panels))
    # print(len([tile for tile in panels.values() if tile == 2]))


file_name = './13.txt'
# file_name = './131.txt'

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]
    line = lines[0]

    numbers = [int(num) for num in line.strip().split(',')]
    tryrun(numbers)
