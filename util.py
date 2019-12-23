from pprint import pprint
import collections
from typing import TypedDict, Callable, List, NamedTuple

number_regex = '(-?\d+)'


def print_dict_grid(grid: dict):
    xs = [p[0] for p in grid.keys()]
    ys = [p[1] for p in grid.keys()]

    print(f'{min(xs)=} {max(xs)=}')
    print(f'{min(ys)=} {max(ys)=}')

    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            elem = grid.get((x, y), ' ')
            # elem = (x, y, elem)
            print(elem, end='')
        print('')


class BfsNode(TypedDict):
    data: any
    steps: int


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Point(self.x * other, self.y * other)


def bfs(
        start_node: BfsNode,
        expand_node: Callable[[BfsNode], List[BfsNode]],
        is_end: Callable[[any], bool],
        debug=True,
) -> BfsNode:
    queue = collections.deque([start_node])

    seen = {
        start_node['data']: start_node['steps']
    }

    node_to_path = {
        start_node['data']: [start_node]
    }

    while queue:
        node = queue.popleft()

        neighbors = expand_node(node)

        for neighbor in neighbors:
            neighbor_data = neighbor['data']
            neighbor_steps = neighbor['steps']

            if seen.get(neighbor_data, 1000000) < neighbor_steps:
                continue

            if debug:
                node_to_path[neighbor_data] = node_to_path[node['data']] + [neighbor]

            seen[neighbor_data] = neighbor_steps
            queue.append(neighbor)

            if is_end(neighbor_data):
                if debug:
                    pprint(node_to_path[neighbor_data])

                return neighbor


MANHATTAN_DELTAS = (
    Point(1, 0),
    Point(-1, 0),
    Point(0, 1),
    Point(0, -1),
)
