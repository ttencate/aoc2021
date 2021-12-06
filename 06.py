import aoc


EXAMPLE1 = '3,4,3,1,2'


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (5934, 26984457539)
    '''
    timers = [0] * 9
    for fish in map(int, input.strip().split(',')):
        timers[fish] += 1
    for day in range(1, 256+1):
        timers = timers[1:7] + [
            timers[7] + timers[0], # 6
            timers[8], # 7
            timers[0], # 8
        ]
        if day == 80:
            answer1 = sum(timers)
        elif day == 256:
            answer2 = sum(timers)
    return answer1, answer2
