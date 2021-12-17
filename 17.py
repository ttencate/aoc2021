import re

import aoc


EXAMPLE1 = 'target area: x=20..30, y=-10..-5'


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    45
    '''
    match = re.match(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-+\d+)$', input.strip())
    x_min, x_max, y_min, y_max = map(int, match.group(1, 2, 3, 4))

    initial_vy = 0
    answer1 = 0
    while True:
        y = 0
        vy = initial_vy
        top = y
        while y > y_max:
            y += vy
            vy -= 1
            top = max(top, y)
        hit = y >= y_min
        #print(f'initial_vy = {initial_vy}, y = {y}, top = {top}, hit = {hit}')
        if hit:
            answer1 = top
        #else:
        #    break
        initial_vy += 1
        if initial_vy >= 2000:
            break
    return answer1
