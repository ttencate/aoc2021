import aoc


EXAMPLE1 = '''
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''


def count_bit(lines, idx, bit):
    count = 0
    for line in lines:
        if line[idx] == bit:
            count += 1
    return count


def majority_bit(lines, idx):
    if count_bit(lines, idx, '1') * 2 >= len(lines):
        return '1'
    else:
        return '0'


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (198, 230)
    '''
    lines = input.strip().splitlines()
    width = len(lines[0])
    count = len(lines)

    gamma = ''
    epsilon = ''
    for i in range(width):
        if majority_bit(lines, i) == '1':
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    power_consumption = int(gamma, base=2) * int(epsilon, base=2)

    numbers = lines[:]
    for i in range(width):
        majority = majority_bit(numbers, i)
        numbers = [
            number for number in numbers
            if number[i] == majority
        ]
        if len(numbers) == 1:
            break
    assert(len(numbers) == 1)
    oxygen_generator_rating = int(numbers[0], base=2)

    numbers = lines[:]
    for i in range(width):
        majority = majority_bit(numbers, i)
        numbers = [
            number for number in numbers
            if number[i] != majority
        ]
        if len(numbers) == 1:
            break
    assert(len(numbers) == 1)
    co2_scrubber_rating = int(numbers[0], base=2)

    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    return power_consumption, life_support_rating
