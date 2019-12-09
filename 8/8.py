from collections import Counter

width = 25
hieght = 6


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def tryrun(numbers):
    print(numbers)

    layers = list(divide_chunks(numbers, width * hieght))

    min_0s = 100000
    total = 0

    for layer in layers:
        count = Counter(layer)
        num_0s = len([num for num in layer if num == 0])

        if count[0] < min_0s:
            total = count[1] * count[2]
            min_0s = num_0s

    outputs = []

    for pixel in range(width * hieght):
        output = 'o'

        for layer in layers:
            val = layer[pixel]
            print(pixel, layer[pixel], val)
            if layer[pixel] in [0, 1] and output == 'o':
                if layer[pixel] == 0:
                    output = ' '
                    outputs.append(output)
                    break
                if layer[pixel] == 1:
                    output = '1'
                    outputs.append(output)
                    break

    print(outputs)
    rows = divide_chunks(outputs, width)
    for row in rows:
        print(''.join(row))
    print(total)


filename = './8.txt'
# filename = './81.txt'

with open(filename) as f:
    lines = [l.rstrip('\n') for l in f]
    line = lines[0]
    tryrun([int(num) for num in list(line)])
