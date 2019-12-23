import re

NUM_CARDS = 119315717514047


# NUM_CARDS = 10007


def _new_stack(position):
    return NUM_CARDS - position - 1


def _cut_stack(position, n):
    if n < 0:
        if position > NUM_CARDS + n - 1:
            return position - (NUM_CARDS + n)
        else:
            return position - n

    if n >= 0:
        if position < n:
            return position + (NUM_CARDS - n)
        else:
            return position - n


file_name = './22.txt'


def _increment(position, n):
    return (position * n) % NUM_CARDS


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
        # print(line)
        if 'new' in line:
            # deck = new_stack(deck)
            # pos = _new_stack(pos)
            pos = _new_stack(pos)
        else:
            n = int(re.search('-?\d+', line).group())

            if 'increment' in line:
                pos = _increment(pos, n)
            else:
                pos = _cut_stack(pos, n)

    delta = abs(prev_pos - pos)

    if pos in seen:
        print('holy shit', pos, i)
    if delta in deltas:
        print('holy delta', delta, i)

    seen.add(pos)

    deltas.add(delta)
    deltas.add(prev_pos + pos)
    deltas.add((prev_pos + pos) % NUM_CARDS)
