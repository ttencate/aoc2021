import aoc


EXAMPLE1 = '''
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''


def neigh(pos):
    return ((pos[0] + i, pos[1] + j) for i in range(-1, 2) for j in range(-1, 2) if i or j)


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (1656, 195)
    '''
    rows = [list(map(int, line)) for line in input.strip().splitlines()]
    energies = {(i, j): rows[i][j] for i in range(10) for j in range(10)}
    answer1 = 0
    step = 0
    while True:
        flashed = set()
        for pos in energies:
            energies[pos] += 1
        while True:
            any_flashed = False
            for pos, energy in energies.items():
                if energy > 9 and pos not in flashed:
                    flashed.add(pos)
                    any_flashed = True
                    if step < 100:
                        answer1 += 1
                    for n in neigh(pos):
                        if n in energies:
                            energies[n] += 1
            if not any_flashed:
                break
        for pos in flashed:
            energies[pos] = 0
        step += 1
        if len(flashed) == len(energies):
            answer2 = step
            break
    return (answer1, answer2)
