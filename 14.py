import collections

import aoc


EXAMPLE1 = '''
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (1588, 2188189693529)
    '''
    lines = input.strip().splitlines()
    initial = lines[0]
    rules = dict(line.split(' -> ') for line in lines[2:])

    return answer(initial, rules, 10), answer(initial, rules, 40)


def answer(initial, rules, steps):
    pair_counts = collections.defaultdict(int)
    for i in range(len(initial) - 1):
        pair_counts[initial[i:i+2]] += 1
    for _ in range(steps):
        new_pair_counts = collections.defaultdict(int)
        for pair, count in pair_counts.items():
            middle = rules[pair]
            new_pair_counts[pair[0] + middle] += count
            new_pair_counts[middle + pair[1]] += count
        pair_counts = new_pair_counts

    counts = collections.defaultdict(int)
    for pair, count in pair_counts.items():
        counts[pair[0]] += count
    counts[initial[-1]] += 1

    values = sorted(list(counts.values()))
    return values[-1] - values[0]
