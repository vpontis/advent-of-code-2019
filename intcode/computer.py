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

        # print('getting input', inputs)

        # consider taking in a function
        if len(inputs) == 0:
            raise Exception('Need input')

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
        return position + 2, None, relative_base + val1

    raise Exception('fuck')


Point = namedtuple('Point', ['x', 'y'])


class Computer:
    position: int = 0
    is_done: bool = False
    relative_base: int = 0
    get_input = None

    def __init__(self, name, numbers, inputs, get_input=None):
        self.name = name
        self.numbers = numbers + [0] * 1_000
        self.inputs = inputs[:]
        self.all_inputs = inputs[:]
        self.get_input = get_input

    def run(self) -> Tuple[bool, Optional[int]]:
        """
        :return: is_done, output
        """
        if self.is_done:
            raise Exception('Running a halted computer.')

        while self.position is not None:
            try:
                (position, output, new_relative_base) = run_operation(
                    self.numbers,
                    self.position,
                    self.inputs,
                    self.relative_base,
                )
            except Exception as e:
                if str(e) == 'Need input':
                    if not self.get_input:
                        raise Exception('Need input')

                    input_num = self.get_input()
                    self.add_input(input_num)

                    (position, output, new_relative_base) = run_operation(
                        self.numbers,
                        self.position,
                        self.inputs,
                        self.relative_base,
                    )
                else:
                    raise e

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
        return f'<Computer {self.name=} {self.inputs=}>'

    @staticmethod
    def parse_input(file_name: str):
        with open(file_name) as f:
            lines = [l.rstrip('\n') for l in f]
            line = lines[0]

            numbers = [int(num) for num in line.strip().split(',')]
            return Computer(file_name, numbers, [])
