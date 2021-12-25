import heapq

import aoc
from grid import Grid


EXAMPLE1 = '''
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (40, 315)
    '''
    risks = Grid.parse(input, int)
    extended_risks = Grid([
        [0 for x in range(risks.width * 5)]
        for y in range(risks.height * 5)
    ])
    for ry in range(5):
        for rx in range(5):
            for coord_in in risks:
                coord_out = (rx * risks.width + coord_in[0], ry * risks.height + coord_in[1])
                extended_risks[coord_out] = (risks[coord_in] - 1 + rx + ry) % 9 + 1
    return lowest_path_risk(risks), lowest_path_risk(extended_risks)


def lowest_path_risk(risks):
    start = (0, 0)
    destination = (risks.width - 1, risks.height - 1)
    queue = [(0, start)]
    visited = set()
    while queue:
        risk, coord = heapq.heappop(queue)
        if coord == destination:
            return risk
        if coord in visited:
            continue
        visited.add(coord)
        for neighbor in risks.neighbors_4(coord):
            heapq.heappush(queue, (risk + risks[neighbor], neighbor))
    assert(False)
