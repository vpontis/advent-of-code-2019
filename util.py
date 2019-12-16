number_regex = '(-?\d+)'


def print_dict_grid(grid: dict):
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
