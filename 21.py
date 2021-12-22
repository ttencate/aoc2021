import collections

import aoc


EXAMPLE1 = '''
Player 1 starting position: 4
Player 2 starting position: 8
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (739785, 444356092776315)
    '''
    positions = [int(line.split()[-1]) for line in input.strip().splitlines()]
    return answer1(positions[:]), answer2(positions[:])


def deterministic_die():
    while True:
        yield from range(1, 101)


def answer1(positions):
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
    return min(scores) * rolls


ROLLS = [
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1),
]


class State(collections.namedtuple('State', ('pos0', 'pos1', 'score0', 'score1'))):
    def after_roll(self, turn, roll):
        pos0, pos1, score0, score1 = self
        if turn == 0:
            pos0 = ((pos0 - 1 + roll) % 10) + 1
            score0 += pos0
        else:
            pos1 = ((pos1 - 1 + roll) % 10) + 1
            score1 += pos1
        return State(pos0, pos1, score0, score1)

    def max_score(self):
        return max(self.score0, self.score1)


def answer2(positions, win_score=21):
    '''
    >>> answer2((4, 8), 1)
    27
    '''
    states = collections.defaultdict(int)
    wins = [0, 0]
    turn = 0
    states[State(*positions, 0, 0)] = 1
    while states:
        new_states = collections.defaultdict(int)
        for state, count in states.items():
            for roll, num_perms in ROLLS:
                new_state = state.after_roll(turn, roll)
                num_universes = count * num_perms
                if new_state.max_score() >= win_score:
                    wins[turn] += num_universes
                else:
                    new_states[new_state] += num_universes
        turn = 1 - turn
        states = new_states
    return max(wins)
