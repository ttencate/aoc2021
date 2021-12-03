import aoc


EXAMPLE1 = '''
forward 5
down 5
forward 8
up 3
down 8
forward 2
'''


def solve(input):
    return part1(input), part2(input)


def parse(input):
    return [
        (line.split()[0], int(line.split()[1]))
        for line in input.strip().splitlines()
    ]


def part1(commands):
    '''
    >>> part1(EXAMPLE1)
    150
    '''
    horizontal = 0
    depth = 0
    for command, n in parse(commands):
        if command == 'forward':
            horizontal += n
        elif command == 'down':
            depth += n
        elif command == 'up':
            depth -= n
        else:
            raise Error(f'Unknown command in line: {line}')
    return horizontal * depth


def part2(commands):
    '''
    >>> part2(EXAMPLE1)
    900
    '''
    horizontal = 0
    depth = 0
    aim = 0
    for command, n in parse(commands):
        if command == 'forward':
            horizontal += n
            depth += aim * n
        elif command == 'down':
            aim += n
        elif command == 'up':
            aim -= n
        else:
            raise Error(f'Unknown command in line: {line}')
    return horizontal * depth
