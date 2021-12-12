import collections
import math

import aoc


EXAMPLE1 = '''
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''


EXAMPLE2 = '''
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''


EXAMPLE3 = '''
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (10, 36)
    >>> solve(EXAMPLE2)
    (19, 103)
    >>> solve(EXAMPLE3)
    (226, 3509)
    '''
    edges = collections.defaultdict(list)
    for line in input.strip().splitlines():
        a, b = line.split('-')
        edges[a].append(b)
        edges[b].append(a)

    def count_paths(curr, visit_counts, remaining_doubles):
        if curr == 'end':
            return 1
        if curr.islower() and visit_counts[curr] >= 1:
            if not remaining_doubles or curr in ('start', 'end'):
                return 0
            else:
                remaining_doubles -= 1
        visit_counts[curr] += 1
        count = sum(
            count_paths(n, visit_counts, remaining_doubles)
            for n in edges[curr])
        visit_counts[curr] -= 1
        return count

    answer1 = count_paths('start', collections.defaultdict(int), 0)
    answer2 = count_paths('start', collections.defaultdict(int), 1)

    return answer1, answer2
