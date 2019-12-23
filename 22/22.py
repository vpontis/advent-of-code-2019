import collections
import itertools
import math
import re
import string
from pprint import pprint
from collections import defaultdict, namedtuple
from typing import List, Tuple, Optional

Position = Tuple[int, int]

NUM_CARDS = 10_007

Deck = List[int]


def new_stack(stack):
    # print(stack)
    stack = stack[::-1]
    # print(stack)
    return stack


def cut_stack(stack, n: int):
    # print(stack)
    _stack = stack[n:] + stack[:n]
    # print(_stack)
    return _stack


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


# new_stack(list(range(10))
# cut_stack(list(range(10)), 3)
# cut_stack(list(range(10)), -4)
# increment(list(range(10)), 3)

# NUM_CARDS = 119315717514047

# print(increment(deck, 54))
# raise Exception('e')
file_name = './22.txt'


# file_name = './221.txt'
# file_name = './222.txt'
# file_name = './223.txt'



def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# new ok
# increment --
def unincrement(stack, n):
    stack_len = len(stack)

    _stack = [99999999] * len(stack)

    chunks = []
    for i in range(n):
        chunks.append(stack[n * i:n * (i + 1)])

    print(chunks)

    chunks = []
    for i in range(n):
        chunks.append(list(range(10))[n * i:n * (i + 1)])

    print(chunks)

    _prev_chunk = 0
    for i, c in enumerate(stack):
        chunk_num = i // n
        print(f'{chunk_num=}')
        rem = i % n

        # if i % n == 0:
        #     _stack[i // n] = c
        #     continue

        print('rem', rem, 'now', i, '-->', c, '\n')
        continue

        # print('f', modinv(i, stack_len))
        print('f', modinv(i, n))
        print(i, c)
        print(i * n, i * i % stack_len)
        print('\n\n')
        # _stack[i * n % stack_len] = c

    # print(_stack)
    return _stack


incr = 3
deck = list(range(NUM_CARDS))
print(deck)
deck = increment(deck, incr)
print(deck)
deck = unincrement(deck, incr)
print(deck.index(99999999), deck)
raise Exception('')


def _unincrement(position, n):
    pos = position
    for _ in range(n):
        pos = _increment(position, n)

    return pos


def _uncut(position, n):
    if n < 0:
        if position < NUM_CARDS + n:
            return (position + NUM_CARDS + n) % NUM_CARDS
        else:
            return (position + n) % NUM_CARDS

    if n >= 0:
        if position > n:
            return (position - NUM_CARDS + n) % NUM_CARDS
        else:
            return (position + n) % NUM_CARDS


deck = []


def get_instructions():
    with open(file_name) as f:
        lines = [l.rstrip('\n') for l in f]
    return lines[:1]


def shuffle_deck(num_cards):
    lines = get_instructions()

    deck = list(range(num_cards))
    pos = deck.index(2019)

    for line in lines:
        # print(line)
        if 'new' in line:
            deck = new_stack(deck)
            pos = _new_stack(pos)
        else:
            n = int(re.search('-?\d+', line).group())

            if 'increment' in line:
                if n < 0:
                    raise Exception('fuckk')

                deck = increment(deck, n)
                pos = _increment(pos, n)
                # pos = _unincrement(pos, n)
            else:
                deck = cut_stack(deck, n)
                pos = _cut_stack(pos, n)
                # pos = _uncut(pos, n)

    print(pos)
    return deck


def unshuffle_deck(pos):
    lines = get_instructions()
    lines = lines[::-1]

    for line in lines:
        if 'new' in line:
            pos = _new_stack(pos)
        else:
            n = int(re.search('-?\d+', line).group())

            if 'increment' in line:
                print('increment fuck')
                pos = _unincrement(pos, n)
            else:
                pos = _uncut(pos, n)

    return pos


deck_a = shuffle_deck(10007)
index = deck_a.index(2019)
print(index)
print(unshuffle_deck(index))


# lines = get_instructions()
#
# lines = lines[::-1]
#
# # deck = list(range(NUM_CARDS))
# # deck = list(range(10))
#
# # print(deck[-5:])
#
# # pos = deck.index(2019)
#
# pos = 2020
#
# seen_positions = set()
#
# for i in range(101741582076661):
#     for line in lines:
#         # print(line)
#         if 'new' in line:
#             # deck = new_stack(deck)
#             # pos = _new_stack(pos)
#             pos = _new_stack(pos)
#         else:
#             n = int(re.search('-?\d+', line).group())
#
#             if 'increment' in line:
#                 if n < 0:
#                     raise Exception('fuckk')
#
#                 # deck = increment(deck, n)
#                 # pos = _increment(pos, n)
#                 pos = _unincrement(pos, n)
#             else:
#                 # deck = cut_stack(deck, n)
#                 # pos = _cut_stack(pos, n)
#                 pos = _uncut(pos, n)
#
#     print(i, pos, pos in seen_positions)
#     seen_positions.add(pos)
#
# # print(deck)
# # print(deck.index(2019))
# print(pos)
# # pprint(list(enumerate(deck)))

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


NUM_CARDS = 119315717514047
NUM_CARDS = 10_007
NUM_CARDS = 10


def _increment(position, n):
    return (position * n) % NUM_CARDS
