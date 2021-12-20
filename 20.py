import math

import aoc


EXAMPLE1 = '''
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''


OFFSETS = tuple((dx, dy) for dy in range(-1, 2) for dx in range(-1, 2))


class Grid:
    def __init__(self, nx, ny, fill):
        self.nx = nx
        self.ny = ny
        self.cells = [[False] * nx for y in range(ny)]
        self.fill = fill

    def parse(self, lines):
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self[x, y] = char == '#'

    def __contains__(self, pos):
        return 0 <= pos[0] < self.nx and 0 <= pos[1] < self.ny

    def __getitem__(self, pos):
        return self.cells[pos[1]][pos[0]] if pos in self else self.fill

    def __setitem__(self, pos, value):
        assert(pos in self)
        self.cells[pos[1]][pos[0]] = value

    def count(self):
        if self.fill:
            return math.inf
        else:
            return sum(map(sum, self.cells))

    def __str__(self):
        return '\n'.join(''.join('#' if self[x, y] else '.' for x in range(self.nx)) for y in range(self.ny))


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (35, 3351)
    '''
    algorithm, grid = parse(input)
    for step in range(2):
        grid = enhance(algorithm, grid)
    answer1 = grid.count()
    for step in range(50 - 2):
        grid = enhance(algorithm, grid)
    answer2 = grid.count()
    return answer1, answer2


def parse(input):
    '''
    >>> print(parse(EXAMPLE1)[1])
    #..#.
    #....
    ##..#
    ..#..
    ..###
    '''
    lines = input.strip().splitlines()

    algorithm = [char == '#' for char in lines[0]]
    assert(not lines[1])

    nx = len(lines[2])
    ny = len(lines) - 2
    grid = Grid(nx, ny, False)
    grid.parse(lines[2:])

    return algorithm, grid


def enhance(algorithm, grid):
    '''
    >>> print(enhance(*parse(EXAMPLE1)))
    .##.##.
    #..#.#.
    ##.#..#
    ####..#
    .#..##.
    ..##..#
    ...#.#.
    '''
    new_fill = algorithm[(1 << 9) - 1] if grid.fill else algorithm[0]
    new_grid = Grid(grid.nx + 2, grid.ny + 2, new_fill)
    for y in range(new_grid.ny):
        for x in range(new_grid.nx):
            index = calc_index(x - 1, y - 1, grid)
            new_grid[x, y] = algorithm[index]
    return new_grid


def calc_index(x, y, grid):
    '''
    >>> grid = Grid(3, 3, False)
    >>> grid.parse(['...', '#..', '.#.'])
    >>> calc_index(1, 1, grid)
    34
    '''
    return sum(
        1 << (8 - i) if grid[x + dx, y + dy] else 0
        for i, (dx, dy) in enumerate(OFFSETS)
    )
