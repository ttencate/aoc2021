import collections
import itertools

import aoc


EXAMPLE1 = '''
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''


def solve(input):
    return count_intersections(input, False), count_intersections(input, True)


def count_intersections(input, diagonal):
    '''
    >>> count_intersections(EXAMPLE1, False)
    5
    >>> count_intersections(EXAMPLE1, True)
    12
    '''
    counts = collections.defaultdict(int)
    for line in input.strip().splitlines():
        a, b = (
            tuple(map(int, endpoints.split(',')))
            for endpoints in line.split(' -> ')
        )
        d = (sign(b[0] - a[0]), sign(b[1] - a[1]))
        if not diagonal and d[0] != 0 and d[1] != 0:
            continue
        p = a
        while p != b:
            counts[p] += 1
            p = (p[0] + d[0], p[1] + d[1])
        counts[p] += 1
    return len([c for c in counts.values() if c > 1])


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
