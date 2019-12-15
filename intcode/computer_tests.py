from intcode.computer import Computer


def day_9a():
    computer = Computer.parse_input('../9/9.txt')
    computer.add_input(1)

    outputs = []

    while not computer.is_done:
        (is_done, output) = computer.run()
        if output:
            outputs.append(output)

    return outputs[-1]


def day_9b():
    computer = Computer.parse_input('../9/9.txt')
    computer.add_input(2)

    outputs = []

    while not computer.is_done:
        (is_done, output) = computer.run()
        if output:
            outputs.append(output)

    return outputs[-1]


if __name__ == '__main__':
    assert day_9a() == 3533056970
    assert day_9b() == 72852
