import math

import aoc


EXAMPLE1 = '16,1,2,0,4,2,7,1,2,14'


def arg_min(xs, fn):
    x = min(xs, key=fn)
    return fn(x)


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (37, 168)
    '''
    crabs = sorted(int(x) for x in input.split(','))
    answer1 = arg_min(
        range(crabs[0], crabs[-1] + 1),
        lambda x: sum(abs(x - c) for c in crabs))
    answer2 = arg_min(
        range(crabs[0], crabs[-1] + 1),
        lambda x: sum(abs(x - c) * (abs(x - c) + 1) // 2 for c in crabs))
    return answer1, answer2
