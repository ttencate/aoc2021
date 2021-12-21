import aoc


EXAMPLE1 = '''
Player 1 starting position: 4
Player 2 starting position: 8
'''


def deterministic_die():
    while True:
        yield from range(1, 101)


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    739785
    '''
    positions = [int(line.split()[-1]) for line in input.strip().splitlines()]
    scores = [0, 0]
    die = deterministic_die()
    turn = 0
    rolls = 0
    while all(score < 1000 for score in scores):
        total = next(die) + next(die) + next(die)
        rolls += 3
        positions[turn] = ((positions[turn] - 1 + total) % 10) + 1
        scores[turn] += positions[turn]
        turn = 1 - turn
    answer1 = min(scores) * rolls
    return answer1
