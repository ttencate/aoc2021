import aoc
from grid import Grid


EXAMPLE1 = '''
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    58
    '''
    grid = Grid.parse(input)
    steps = 0
    while True:
        moved = False
        if move(grid, '>', 1, 0):
            moved = True
        if move(grid, 'v', 0, 1):
            moved = True
        steps += 1
        if not moved:
            break
    return steps


def move(grid, char, dx, dy):
    '''
    >>> grid = Grid.parse("""
    ... ..........
    ... .>v....v..
    ... .......>..
    ... ..........
    ... """)
    >>> move(grid, '>', 1, 0)
    True
    >>> move(grid, 'v', 0, 1)
    True
    >>> print(str(grid).replace('.', '-')) # Triple dot triggers line continuation.
    ----------
    ->--------
    --v----v>-
    ----------
    '''
    moving = []
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[x, y] == char:
                next_x = (x + dx) % grid.width
                next_y = (y + dy) % grid.height
                if grid[next_x, next_y] == '.':
                    moving.append((x, y, next_x, next_y))

    for x, y, next_x, next_y in moving:
        grid[next_x, next_y] = grid[x, y]
        grid[x, y] = '.'

    return bool(moving)
