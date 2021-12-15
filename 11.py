import aoc
from grid import Grid


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


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (1656, 195)
    '''
    energies = Grid.parse(input)
    answer1 = 0
    step = 0
    while True:
        flashed = set()
        for coord in energies:
            energies[coord] += 1
        while True:
            any_flashed = False
            for coord in energies:
                energy = energies[coord]
                if energy > 9 and coord not in flashed:
                    flashed.add(coord)
                    any_flashed = True
                    if step < 100:
                        answer1 += 1
                    for neighbor in energies.neighbors_8(coord):
                        energies[neighbor] += 1
            if not any_flashed:
                break
        for coord in flashed:
            energies[coord] = 0
        step += 1
        if len(flashed) == len(energies):
            answer2 = step
            break
    return (answer1, answer2)
