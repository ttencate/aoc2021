import re

import aoc


EXAMPLE1 = 'target area: x=20..30, y=-10..-5'


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (45, 112)
    '''
    target = x_min, x_max, y_min, y_max = parse(input)

    initial_vx_min = 0 # TODO can be tightened
    initial_vx_max = x_max
    initial_vy_min = y_min
    initial_vy_max = 2000 # Hack hack

    answer1 = 0
    answer2 = 0
    for initial_vy in range(initial_vy_min, initial_vy_max + 1):
        for initial_vx in range(initial_vx_min, initial_vx_max + 1):
            if hits_target(initial_vx, initial_vy, target):
                answer1 = max(answer1, arc_top(initial_vy))
                answer2 += 1
    return answer1, answer2


def parse(input):
    match = re.match(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-+\d+)$', input.strip())
    x_min, x_max, y_min, y_max = map(int, match.group(1, 2, 3, 4))
    assert(0 <= x_min <= x_max)
    assert(y_min <= y_max <= 0)
    return x_min, x_max, y_min, y_max

def hits_target(initial_vx, initial_vy, target):
    '''
    >>> target = 20, 30, -10, -5
    >>> hits_target(7, 2, target)
    True
    >>> hits_target(6, 3, target)
    True
    >>> hits_target(9, 0, target)
    True
    >>> hits_target(17, -4, target)
    False
    >>> hit_cases = set((
    ...     (23,-10), (25,-9 ), (27,-5 ), (29,-6 ), (22,-6 ), (21,-7 ), (9,0   ), (27,-7 ), (24,-5 ),
    ...     (25,-7 ), (26,-6 ), (25,-5 ), (6,8   ), (11,-2 ), (20,-5 ), (29,-10), (6,3   ), (28,-7 ),
    ...     (8,0   ), (30,-6 ), (29,-8 ), (20,-10), (6,7   ), (6,4   ), (6,1   ), (14,-4 ), (21,-6 ),
    ...     (26,-10), (7,-1  ), (7,7   ), (8,-1  ), (21,-9 ), (6,2   ), (20,-7 ), (30,-10), (14,-3 ),
    ...     (20,-8 ), (13,-2 ), (7,3   ), (28,-8 ), (29,-9 ), (15,-3 ), (22,-5 ), (26,-8 ), (25,-8 ),
    ...     (25,-6 ), (15,-4 ), (9,-2  ), (15,-2 ), (12,-2 ), (28,-9 ), (12,-3 ), (24,-6 ), (23,-7 ),
    ...     (25,-10), (7,8   ), (11,-3 ), (26,-7 ), (7,1   ), (23,-9 ), (6,0   ), (22,-10), (27,-6 ),
    ...     (8,1   ), (22,-8 ), (13,-4 ), (7,6   ), (28,-6 ), (11,-4 ), (12,-4 ), (26,-9 ), (7,4   ),
    ...     (24,-10), (23,-8 ), (30,-8 ), (7,0   ), (9,-1  ), (10,-1 ), (26,-5 ), (22,-9 ), (6,5   ),
    ...     (7,5   ), (23,-6 ), (28,-10), (10,-2 ), (11,-1 ), (20,-9 ), (14,-2 ), (29,-7 ), (13,-3 ),
    ...     (23,-5 ), (24,-8 ), (27,-9 ), (30,-7 ), (28,-5 ), (21,-10), (7,9   ), (6,6   ), (21,-5 ),
    ...     (27,-10), (7,2   ), (30,-9 ), (21,-8 ), (22,-7 ), (24,-9 ), (20,-6 ), (6,9   ), (29,-5 ),
    ...     (8,-2  ), (27,-8 ), (30,-5 ), (24,-7 )
    ... ))
    >>> for case in hit_cases:
    ...     if not hits_target(*case, target):
    ...         print(case)
    >>> miss_cases = set(
    ...     (initial_vx, initial_vy)
    ...     for initial_vx in range(0, 31)
    ...     for initial_vy in range(-10, 11)
    ...     if (initial_vx, initial_vy) not in hit_cases
    ... )
    >>> for case in miss_cases:
    ...     if hits_target(*case, target):
    ...         print(case)
    '''
    x_min, x_max, y_min, y_max = target
    x, y = 0, 0
    vx, vy = initial_vx, initial_vy
    while x < x_max and y > y_min:
        x += vx
        y += vy
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
        if vx > 0:
            vx -= 1
        vy -= 1
    return False


def arc_top(initial_vy):
    '''
    >>> arc_top(-9)
    0
    >>> arc_top(9)
    45
    '''
    if initial_vy < 0:
        return 0
    return initial_vy * (initial_vy + 1) // 2
