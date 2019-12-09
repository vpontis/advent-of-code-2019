from collections import defaultdict

steps = set()

step_to_requirements = defaultdict(list)


with open('7.txt') as f:
    for line in f:
        step_1 = line[5]
        step_2 = line[36]

        steps.add(step_1)
        steps.add(step_2)

        step_to_requirements[step_2].append(step_1)

done_steps = set()
remaining_steps = set(list(steps))

def can_do_step(step):
    reqs = step_to_requirements[step]
    return len([req for req in reqs if req not in done_steps]) == 0

answer = []

while remaining_steps:
    ok_steps = []

    for step in remaining_steps:
        if can_do_step(step):
            ok_steps.append(step)
    
    for step in ok_steps:
        remaining_steps.remove(step)
        done_steps.add(step)

    answer.extend(sorted(ok_steps))


print(''.join(answer))



