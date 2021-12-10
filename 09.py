import aoc


EXAMPLE1 = '''
2199943210
3987894921
9856789892
8767896789
9899965678
'''


def neigh(pos):
    i, j = pos
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (15, 1134)
    '''
    heights = [list(map(int, line)) for line in input.strip().splitlines()]
    ni = len(heights)
    nj = len(heights[0])
    def height(pos):
        i, j = pos
        if i < 0 or i >= ni or j < 0 or j >= nj:
            return 10
        return heights[i][j]
    poses = [(i, j) for i in range(ni) for j in range(nj)]

    answer1 = sum(
        1 + height(pos) for pos in poses
        if all(height(n) > height(pos) for n in neigh(pos)))

    basin_sizes = []
    visited = set()
    for pos in poses:
        basin = set()
        queue = [pos]
        while queue:
            curr = queue.pop()
            if curr in visited:
                continue
            visited.add(curr)
            if height(curr) >= 9:
                continue
            basin.add(curr)
            for n in neigh(curr):
                queue.append(n)
        if basin:
            basin_sizes.append(len(basin))

    basin_sizes.sort()
    answer2 = basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]

    return (answer1, answer2)
