from collections import defaultdict

from intcode.computer import Computer

computer = Computer.parse_input('15.txt')

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (1, 0),
    4: (-1, 0),
}

command_to_opposite = {
    1: 2,
    2: 1,
    3: 4,
    4: 3,
}

# o - open
# w - wall
grid = {
    (0, 0): 'o',
}


def print_grid():
    xs = [p[0] for p in grid.keys()]
    ys = [p[1] for p in grid.keys()]
    print(f'{min(xs)=} {max(xs)=}')
    print(f'{min(ys)=} {max(ys)=}')

    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            elem = grid.get((x, y), ' ')
            if elem == 'o':
                elem = '.'
            if y == 0 and x == 0:
                elem = 'V'
            print(elem, end='')
        print('')


position = (0, 0)
path_home = []

o2_position = None

while True:
    for (command, direction) in directions.items():
        new_position = position[0] + direction[0], position[1] + direction[1]

        if new_position in grid:
            continue

        computer.add_input(command)
        (is_done, output) = computer.run()

        if output == 0:
            grid[new_position] = 'w'
        elif output == 1:
            grid[new_position] = 'o'

            path_home.append(command_to_opposite[command])
            position = new_position
            break
        elif output == 2:
            grid[new_position] = '2'
            o2_position = new_position

            path_home.append(command_to_opposite[command])
            position = new_position
            break
    else:
        # We weren't able to explore a new path so let's go one home
        # print_grid()
        if not path_home:
            print_grid()
            break

        command = path_home.pop()
        computer.add_input(command)
        (is_done, output) = computer.run()
        if output not in [1, 2]:
            print(command, output, path_home, position)
            raise Exception('Not going home good')

        direction = directions[command]
        position = position[0] + direction[0], position[1] + direction[1]

queue = [o2_position]
levels = 0
seen = set()

while len([val for val in grid.values() if val == 'o']):
    levels += 1
    next_level = []

    for position in queue:
        for (command, direction) in directions.items():
            new_position = position[0] + direction[0], position[1] + direction[1]
            if new_position in seen:
                continue

            if grid.get(new_position) != 'o':
                continue

            seen.add(new_position)
            next_level.append(new_position)

            grid[new_position] = '2'
            # print(new_position, levels)

    queue = next_level

print_grid()
print(levels)
