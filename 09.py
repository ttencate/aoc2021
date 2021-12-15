import aoc
from grid import Grid


EXAMPLE1 = '''
2199943210
3987894921
9856789892
8767896789
9899965678
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (15, 1134)
    '''
    heights = Grid.parse(input)

    answer1 = sum(
        1 + heights[coord] for coord in heights
        if all(heights[n] > heights[coord] for n in heights.neighbors_4(coord)))

    basin_sizes = []
    visited = set()
    for coord in heights:
        basin = set()
        queue = [coord]
        while queue:
            curr = queue.pop()
            if curr in visited:
                continue
            visited.add(curr)
            if heights[curr] >= 9:
                continue
            basin.add(curr)
            for n in heights.neighbors_4(curr):
                queue.append(n)
        if basin:
            basin_sizes.append(len(basin))

    basin_sizes.sort()
    answer2 = basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]

    return (answer1, answer2)
