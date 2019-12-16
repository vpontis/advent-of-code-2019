import math
from collections import namedtuple
from pprint import pprint
from typing import List

prob_input = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''
#
# prob_input = '''10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL'''
prob_input = '''2 WZMS, 3 NPNFD => 5 SLRGD
4 QTFCJ, 1 RFZF => 1 QFQPN
2 LCDPV => 6 DGPND
1 MVSHM, 3 XSDR, 1 RSJD => 6 GNKB
6 XJRML, 1 LCDPV => 7 HTSJ
3 LQBX => 3 GKNTG
2 NZMLP, 5 FTNZQ => 2 QSLTQ
8 WZMS, 4 XSDR, 2 NPNFD => 9 CJVT
16 HFHB, 1 TRVQG => 8 QTBQ
177 ORE => 7 DNWGS
10 ZJFM, 4 MVSHM => 8 LCDPV
1 LTVKM => 5 ZJFM
5 QFJS => 6 LTVKM
4 CZHM, 12 CJVT => 9 PGMS
104 ORE => 8 QCGM
1 JWLZ, 5 QTFCJ => 4 DHNL
20 VKRBJ => 3 FQCKM
1 FTNZQ, 1 QSLTQ => 4 HFHB
1 JLPVD => 2 JGJFQ
12 PTDL => 1 LVPK
31 JGJFQ, 5 PGMS, 38 PTDL, 1 PGCZ, 3 LVPK, 47 JGHWZ, 21 LVPJ, 27 LTVKM, 5 ZDQD, 5 LCDPV => 1 FUEL
6 WFJT, 2 VKRBJ => 8 NZMLP
21 HNJW, 3 NXTL, 8 WZMS, 5 SLRGD, 2 VZJHN, 6 QFQPN, 5 DHNL, 19 RNXQ => 2 PGCZ
1 QTBQ, 3 MVSHM => 1 XSDR
25 ZKZNB => 9 VZJHN
4 WHLT => 9 PHFKW
29 QPVNV => 9 JGHWZ
13 ZJFM => 2 RNXQ
1 DGPND, 12 PHFKW => 9 BXGXT
25 ZJFM => 6 WHLT
3 QPVNV => 9 BTLH
1 KXQG => 8 TRVQG
2 JWLZ => 8 JLPVD
2 GKNTG => 6 NXTL
28 VKRBJ => 2 DXWSH
126 ORE => 7 VKRBJ
11 WHLT => 8 QTFCJ
1 NZMLP, 1 DNWGS, 8 VKRBJ => 5 XJRML
16 XJRML => 6 SKHJL
3 QTFCJ, 6 ZTHWQ, 15 GKNTG, 1 NXRZL, 1 DGBRZ, 1 SKHJL, 1 VZJHN => 7 LVPJ
1 HFHB, 16 QTBQ, 7 XJRML => 3 NPNFD
2 TRVQG => 4 JWLZ
8 GKNTG, 1 NSVG, 23 RNXQ => 9 NXRZL
3 QTFCJ => 6 CZHM
2 NPNFD => 8 JQSTD
1 DXWSH, 1 DGPND => 4 DGBRZ
3 DXWSH, 24 QFJS, 8 FTNZQ => 8 KXQG
6 FXJQX, 14 ZKZNB, 3 QTFCJ => 2 ZTHWQ
31 NSVG, 1 NXRZL, 3 QPVNV, 2 RNXQ, 17 NXTL, 6 BTLH, 1 HNJW, 2 HTSJ => 1 ZDQD
5 RNXQ, 23 BXGXT, 5 JQSTD => 7 QPVNV
8 NPNFD => 7 WZMS
6 KXQG => 7 ZDZM
129 ORE => 9 WFJT
9 NZMLP, 5 FQCKM, 8 QFJS => 1 LQBX
170 ORE => 9 GDBNV
5 RSJD, 3 CZHM, 1 GNKB => 6 HNJW
14 HTSJ => 7 FXJQX
11 NPNFD, 1 LCDPV, 2 FXJQX => 6 RSJD
9 DGBRZ => 6 ZKZNB
7 GDBNV, 1 QCGM => 8 QFJS
2 QFQPN, 5 JWLZ => 4 NSVG
8 QFJS, 1 ZDZM, 4 QSLTQ => 7 MVSHM
1 LTVKM => 8 RFZF
4 DNWGS => 3 FTNZQ
6 VZJHN => 9 PTDL'''

lines = prob_input.split('\n')
recipes = {}

Resource = namedtuple('Resource', ['name', 'count'])


def parse(kk):
    idx = kk.find(" ")
    return Resource(kk[idx + 1:], int(kk[:idx]))


for line in lines:
    ing, out = line.split(" => ")

    ing = ing.split(", ")
    ing = [parse(inga) for inga in ing]
    out = parse(out)

    recipes[out.name] = {
        'in': ing,
        'out': out
    }

pprint(recipes)

equations = []


def parse_values(comp_str):
    [num, resource] = comp_str.strip().split(' ')
    return Resource(resource, int(num))


for line in lines:
    line = line.replace('>', '')
    [left, right] = line.split('=')

    reactants = [
        parse_values(reactant_string)
        for reactant_string in left.split(', ')
    ]

    product = parse_values(right)

    equations.append((reactants, product))


#
# def get_num_ore(product: Resource):
#     if product.name == 'ORE':
#         return product.count
#
#     matching_equations = []
#
#     for (reactants, prod) in equations:
#         if product.name != prod.name:
#             continue
#
#         matching_equations.append((reactants, prod))
#
#     ore_amounts = []
#
#     for (reactants, prod) in matching_equations:
#         ore_amounts.append(sum([
#             get_num_ore(reactant) * math.ceil(product.count / prod.count)
#             for reactant in reactants
#         ]))
#
#     print(product, ore_amounts)
#     return min(ore_amounts)
#
#
# print(get_num_ore(Resource('FUEL', 1)))


class ReachableState:
    resource_count: dict
    ore_used: int
    ore_leftover: int

    def __init__(self, resource_to_count, ore_used: int, ore_leftover: int):
        self.resource_to_count = resource_to_count
        self.ore_used = ore_used
        self.ore_leftover = ore_leftover

    def clone(self):
        return ReachableState(
            self.resource_to_count.copy(),
            self.ore_used,
            self.ore_leftover
        )

    def can_run_equation(self, equation) -> bool:
        for reactant in equation[0]:
            if reactant.name == 'ORE':
                continue

            if reactant.name not in self.resource_to_count:
                return False

        return True

    def multiply(self, state_multiple: int):
        for name, count in self.resource_to_count.items():
            self.resource_to_count[name] = count * state_multiple
        self.ore_used *= state_multiple

    def run_equation(self, equation):
        reactants, product = equation

        state_multiple = 1

        for reactant in reactants:
            if reactant.name == 'ORE':
                continue

            state_multiple = max(
                state_multiple,
                math.ceil(reactant.count / self.resource_to_count[reactant.name])
            )

        print(self.resource_to_count, equation, state_multiple)

        self.multiply(state_multiple)

        for reactant in reactants:
            if reactant.name == 'ORE':
                self.ore_used += reactant.count
                continue

            if reactant.name not in self.resource_to_count:
                raise Exception('Cannot run equation')
            if reactant.count > self.resource_to_count[reactant.name]:
                raise Exception('Cannot run equation')

            self.resource_to_count[reactant.name] -= reactant.count

            if self.resource_to_count[reactant.name] == 0:
                del self.resource_to_count[reactant.name]

        if product.name in self.resource_to_count:
            self.resource_to_count[product.name] += product.count
        else:
            self.resource_to_count[product.name] = product.count

    @property
    def resource_tuple(self):
        return tuple(sorted([
            (name, count)
            for name, count in self.resource_to_count.items()
            if count > 0
        ], key=lambda x: x[0]))

    @property
    def resource_types(self):
        return set(
            [name
             for name, count in self.resource_to_count.items()
             if count > 0]
        )

    @classmethod
    def is_state2_new(cls, state1, state2):
        """

        :param state:
        :return:
        """
        if state1.resource_types != state2.resource_types:
            return True

        if state2.ore_used < state1.ore_used:
            return True

        for resource in state1.resource_types:
            ratio1 = state1.ore_used / state1.resource_to_count[resource]
            ratio2 = state2.ore_used / state2.resource_to_count[resource]

            if ratio2 < ratio1:
                return True

        return False

    def __repr__(self):
        return f'<State {self.resource_tuple} {self.ore_used=}/>'


reachable_states = [
    ReachableState({}, 0, 0)
]

reachable = set()


def can_extend_state(reachable_state: ReachableState, equation):
    for reactant in equation[0]:
        if reactant.name == 'ORE':
            continue

        if reachable_state.resource_to_count.get(reactant.name, 0) < reactant.count:
            return False

    return True


def run_equation(reachable_state: ReachableState, equation) -> ReachableState:
    new_state = reachable_state.clone()
    new_state.run_equation(equation)
    return new_state


def extend_state(reachable_state: ReachableState, equation):
    return run_equation(reachable_state, equation)


state_to_ore_count = {}

found_home = False


# # for i in range(50):
# while not found_home:
#     for equation in equations:
#         (reactants, product) = equation
#
#         new_states = []
#
#         for reachable_state in reachable_states:
#             if not reachable_state.can_run_equation(equation):
#                 continue
#
#             new_state = reachable_state.clone()
#             new_state.run_equation(equation)
#
#             # Only add it to reachable states if we are on the Frontier
#             is_new_state = all([
#                 ReachableState.is_state2_new(state1, new_state)
#                 for state1 in reachable_states
#             ])
#
#             if is_new_state:
#                 state_to_ore_count[new_state.resource_tuple] = new_state.ore_used
#                 new_states.append(new_state)
#
#             if product.name == 'FUEL':
#                 found_home = True
#                 print('\n\n')
#                 print(new_state)
#                 print('\n\n')
#                 break
#
#         reachable_states.extend(new_states)
#
#     print(state_to_ore_count)
#
# pprint(sorted(reachable_states, key=lambda x: x.resource_tuple))


def get_required(fuel_amount):
    required = {}
    required['FUEL'] = fuel_amount

    while any(required[key] > 0 and key != "ORE" for key in required):
        to_expand = [
            k for k in required.keys()
            if required[k] > 0 and k != "ORE"
        ][0]

        outq = recipes[to_expand]['out'].count
        times_run = math.ceil(required[to_expand] / outq)

        required[to_expand] -= outq * times_run

        for reactant in recipes[to_expand]['in']:
            if reactant.name in required:
                required[reactant.name] += reactant.count * times_run
            else:
                required[reactant.name] = reactant.count * times_run

    return required['ORE']


one_trillion = 1000000000000
num_produced = int(one_trillion / 201324)

low = 0
high = 20000000

while low < high:
    print(low, high)
    mid = (low + high) // 2
    req = get_required(mid)
    if req > one_trillion:
        high = mid - 1
    elif req < one_trillion:
        low = mid

print(low)
