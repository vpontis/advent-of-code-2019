import re

NUM_CARDS = 10

NUM_CARDS = 119315717514047
# NUM_CARDS = 10

file_name = './22.txt'


def increment(stack, n: int):
    # print(stack)

    stack_len = len(stack)

    _stack = [99999999] * len(stack)

    for i, c in enumerate(stack):
        _stack[(i * n) % stack_len] = c

    if 99999999 in _stack:
        raise Exception('fuck')

    # print(_stack)
    return _stack


# new ok
# increment --
def unincrement(stack, n):
    stack_len = len(stack)

    _stack = [99999999] * len(stack)

    _prev_chunk = 0
    for i, c in enumerate(stack):
        pos = _unincrement(i, n)
        _stack[pos] = c
        continue

    # print(_stack)
    return _stack


def _unincrement(pos, n):
    for x in range(n):
        num = pos + x * NUM_CARDS
        if num % n == 0:
            return num // n


def cut(stack, n: int):
    return stack[n:] + stack[:n]


def _cut(stack, n: int):
    _new_stack = [99999] * NUM_CARDS
    for i, c in enumerate(stack):
        pos = _cut_pos(i, n)
        _new_stack[pos] = c
    return _new_stack


def _cut_pos(position, n):
    if n < 0:
        n += NUM_CARDS

    if position < n:
        return position + (NUM_CARDS - n)
    else:
        return position - n


def uncut(stack, n: int):
    _new_stack = [99999] * NUM_CARDS
    for i, c in enumerate(stack):
        pos = _uncut_pos(i, n)
        _new_stack[pos] = c
    return _new_stack


def _uncut_pos(position, n):
    return _cut_pos(position, -1 * n)


def _new(pos):
    return NUM_CARDS - pos - 1


def get_instructions():
    with open(file_name) as f:
        lines = [l.rstrip('\n') for l in f]
    return lines


instructions = get_instructions()

pos = 2020
# pos = 2019

deltas = set()
seen = set()

for i in range(101741582076661):
    prev_pos = pos

    for line in instructions:
        if 'new' in line:
            pos = _new(pos)
        else:
            n = int(re.search('-?\d+', line).group())

            if 'increment' in line:
                pos = _unincrement(pos, n)
            else:
                pos = _uncut_pos(pos, n)

    delta = abs(prev_pos - pos)

    if pos in seen:
        print('holy shit', pos, i)
    if delta in deltas:
        print('holy delta', delta, i)

    seen.add(pos)

    deltas.add(delta)
    deltas.add(prev_pos + pos)
    deltas.add((prev_pos + pos) % NUM_CARDS)
