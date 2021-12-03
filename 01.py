EXAMPLE1 = """199
200
208
210
200
207
240
269
260
263"""


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (7, 5)
    '''
    depths = [int(line) for line in input.splitlines()]
    answer1 = sum([1 for (a, b) in zip(depths[:-1], depths[1:]) if a < b])
    sums = [a + b + c for (a, b, c) in zip(depths[:-2], depths[1:-1], depths[2:])]
    answer2 = sum([1 for (a, b) in zip(sums[:-1], sums[1:]) if a < b])
    return (answer1, answer2)
