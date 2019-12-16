import itertools
import math
import re
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

file_name = './16.txt'
# file_name = './161.txt'

with open(file_name) as f:
    lines = [l.rstrip('\n') for l in f]
    line = lines[0]

    numbers = [int(num) for num in list(line)]

# numbers = [int(num) for num in '03036732577212944063491565474664']

# numbers = [int(num) for num in '12345678']

numbers = numbers * 10_000

# numbers = numbers * 5
# numbers = numbers * 10

offset = int(''.join([str(n) for n in numbers[:7]]))
# offset = 0
halfway = int(len(numbers) * 0.8)
print(offset, halfway)

base_pattern = [0, 1, 0, -1]

idx_to_pattern = {}

len_numbers = len(numbers)
print(f'{len_numbers=}')


def get_pattern(idx: int):
    if idx in idx_to_pattern:
        return idx_to_pattern[idx]

    pattern = []
    for num in base_pattern:
        pattern.extend([num] * (idx + 1))

    pattern = pattern[1:] + [pattern[0]]
    idx_to_pattern[idx] = pattern
    return pattern


idx_to_positions = {}


for idx in range(halfway, len(numbers)):
    positions = []

    _pos = []
    start = idx
    mult = 1

    num_positions = math.ceil((len_numbers - idx) / (idx + 1) * 2 / 4)
    for i in range(num_positions):
        start = idx + (idx + 1) * 2 * i
        end = min(len(numbers) - 1, start + idx)
        _pos.append((mult, start, end))
        mult *= -1

    idx_to_positions[idx] = _pos

    if idx % 10000 == 0:
        print(idx)

# print(list(get_pattern(0)))
# pprint(idx_to_positions)
print('got idxs', len(idx_to_positions))


# print(len(idx_to_positions))
# raise Exception('')


def get_sums(inp: List[int]) -> List[int]:
    nums = [0]

    summation = 0
    for num in inp:
        summation += num
        nums.append(summation)

    return nums


numbers = numbers[halfway:]


def get_next_num(inp: List[int]):
    new_num = []

    sums = get_sums(inp)

    for idx, num in enumerate(inp):
        positions = idx_to_positions[idx + halfway]

        num = 0
        for (mult, start, end) in positions:
            if start < halfway:
                continue

            num += mult * (sums[(end + 1) % halfway] - sums[start % halfway])

        result = abs(num) % 10

        new_num.append(result)

    # print(inp)
    # print(new_num)
    # print('\n\n')
    return new_num


# steps = 2
steps = 100
for i in range(steps):
    numbers = get_next_num(numbers)
    print(i)

offset = offset - halfway

print(''.join([str(n) for n in numbers[offset:offset + 8]]))
