from collections import defaultdict

planet_to_center = {}
center_to_planets = defaultdict(list)


def get_num_orbits(planet):
    center = planet_to_center.get(planet)
    if not center:
        return 0

    return 1 + get_num_orbits(center)


def get_neighbors(node):
    neighbors = []
    if planet_to_center.get(node):
        neighbors.append(planet_to_center[node])
    if center_to_planets.get(node):
        neighbors.extend(center_to_planets[node])

    return neighbors


def bfs_you_to_san():
    queue = get_neighbors('YOU')

    transfers = 0

    seen_nodes = set(queue)

    while queue:
        next_queue = []

        for node in queue:
            neighbors = get_neighbors(node)

            next_queue.extend(neighbors)

            if node == 'SAN':
                print(transfers - 1)
                return

        next_queue = [node for node in next_queue if node not in seen_nodes]
        for node in next_queue:
            seen_nodes.add(node)

        queue = next_queue

        transfers += 1


def tryrun(orbits):
    for center, planet in orbits:
        planet_to_center[planet] = center
        center_to_planets[center].append(planet)

    bfs_you_to_san()
    # total = 0
    # for planet in planet_to_center.keys():
    #     num = get_num_orbits(planet)
    #     total += num
    #
    # print(total)


with open('./input1.txt') as f:
    lines = [l.rstrip('\n') for l in f]
    orbits = [l.split(')') for l in lines]

    tryrun(orbits)
