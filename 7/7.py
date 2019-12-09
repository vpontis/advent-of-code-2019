import itertools
from collections import defaultdict
from typing import List, Tuple, Optional


def parse_opcode(opcode: int):
    opcode_str = str(opcode)
    code = int(opcode_str[-2:])

    if code == 99:
        return {'code': code, 'modes': []}

    modes_str = opcode_str[:- 2]

    padded = modes_str.zfill(3)
    modes = list(padded)[::-1]
    return {'code': code, 'modes': modes}


def get_vals(numbers: List[int], position: int, modes: List[str], num_vals: int):
    vals = []
    for i in range(num_vals):
        arg = numbers[position + i]
        val = numbers[arg] if modes[i] == "0" else arg
        vals.append(val)

    vals.append(numbers[position + num_vals])
    return vals


def run_operation(
        numbers: List[int], position: int, inputs: List[int],
) -> Tuple[Optional[int], Optional[int]]:
    code_info = parse_opcode(numbers[position])
    code = code_info['code']
    modes = code_info['modes']
    # print(code, position, numbers)

    if code == 99:
        return (None, None)

    if code in [1, 2]:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2)

        if code == 1:
            result = val1 + val2
        else:
            result = val1 * val2

        numbers[destination] = result
        return (position + 4, None)

    if code == 3:
        [destination] = get_vals(numbers, position + 1, modes, 0)

        num_input = inputs.pop(0)

        numbers[destination] = num_input
        return (position + 2, None)

    if code == 4:
        [val1, _destination] = get_vals(numbers, position + 1, modes, 1)
        return (position + 2, val1)

    if code == 5:
        [val1, val2, _destination] = get_vals(numbers, position + 1, modes, 2)
        should_jump = val1 != 0
        if should_jump:
            return (val2, None)
        return (position + 3, None)

    if code == 6:
        [val1, val2, _destination] = get_vals(numbers, position + 1, modes, 2)
        should_jump = val1 == 0
        if should_jump:
            return val2
        return (position + 3, None)

    if code == 7:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2)
        numbers[destination] = 1 if val1 < val2 else 0
        return (position + 4, None)

    if code == 8:
        [val1, val2, destination] = get_vals(numbers, position + 1, modes, 2)
        numbers[destination] = 1 if val1 == val2 else 0
        return (position + 4, None)

    print('fucking code', code)
    raise Exception('fuck')


class Amp:
    position: int = 0
    is_done: bool = False

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
            result = run_operation(self.numbers, self.position, self.inputs)
            (position, output) = result

            self.position = position

            if output is not None:
                return False, output

        self.is_done = True
        return True, None

    def add_input(self, num: int):
        self.inputs.append(num)
        self.all_inputs.append(num)

    def __repr__(self):
        return f'<Amp {self.name=} {self.inputs=}>'


def try_phases(numbers, phases):
    amps = [Amp(i, numbers[:], [phases[i]]) for i in range(0, 5)]
    amps[0].add_input(0)

    while any([not amp.is_done for amp in amps]):
        for i, amp in enumerate(amps):
            is_done, output = amp.run()

            if output is not None:
                next_amp_idx = (i + 1) % 5
                amps[next_amp_idx].add_input(output)

    return amps[0].all_inputs[-1]


def tryrun(numbers):
    outputs = []
    for phases in itertools.permutations(list(range(0 + 5, 5 + 5))):
    # for phases in [[9, 8, 7, 6, 5]]:
        phases = list(phases)

        print(phases)
        result = try_phases(numbers, phases)
        print(result)
        outputs.append(result)

    print(max(outputs))


with open('./7.txt') as f:
    lines = [l.rstrip('\n') for l in f]
    line = lines[0]
    numbers = [int(num) for num in line.strip().split(',')]
    tryrun(numbers)
