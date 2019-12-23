import itertools
from collections import defaultdict
from pprint import pprint
from typing import Union, List, Tuple

from intcode.computer import Computer
from util import print_dict_grid

computer = Computer.parse_input('21.txt')


# file_name = './21.txt'
# # file_name = './211.txt'
# # file_name = './212.txt'
# # file_name = './213.txt'
#
# grid = {}
# elem_to_position = {}
#
# with open(file_name) as f:
#     lines = [l.rstrip('\n') for l in f]
#
#     for y, line in enumerate(lines):
#         for x, char in enumerate(line):
#             grid[(x, y)] = char

def get_computer_demand():
    out_string = ''

    while True:
        try:
            is_done, output = computer.run()
            if is_done:
                print('fuck', out_string)
                return out_string
            try:
                out_string += chr(output)
            except Exception as e:
                print(output)
                raise e
        except Exception as e:
            print(str(e))
            if str(e) == 'Need input':
                return out_string

            raise e


def send_line(s):
    s += '\n'

    for c in s:
        computer.add_input(ord(c))

    print('Sent line', s)


commands = '''
NOT T T
AND A T
AND B T
AND C T -- T is true A-C are walkable
NOT T T -- T is true if there is a hole

AND D T -- T is true if there is a hole AND D is landable

OR E J
OR H J
AND T J

RUN
'''.splitlines()


def process_command(c):
    print(c)
    if '--' not in c:
        return c.strip()

    c = c.split('--')[0].strip()
    return c


commands = [
    process_command(c) for c in commands
    if c.strip()
]


def run_program(commands):
    out_string = get_computer_demand()
    print(out_string)

    for c in commands:
        send_line(c)

    out_string = get_computer_demand()
    print(out_string)


run_program(commands)
