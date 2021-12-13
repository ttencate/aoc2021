import aoc


EXAMPLE1 = '''
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (17, '\\n#####\\n#...#\\n#...#\\n#...#\\n#####')
    '''
    lines = iter(input.strip().splitlines())

    points = set()
    for line in lines:
        if not line:
            break
        x, y = map(int, line.split(','))
        points.add((x, y))

    answer1 = None
    for line in lines:
        axis, offset = line.split('=')
        axis = axis[-1]
        offset = int(offset)
        new_points = set()
        for x, y in points:
            if axis == 'x':
                if x > offset:
                    x = 2*offset - x
            else:
                assert(axis == 'y')
                if y > offset:
                    y = 2*offset - y
            new_points.add((x, y))
        points = new_points
        if answer1 is None:
            answer1 = len(points)

    answer2 = ''
    nx = max(x for x, y in points) + 1
    ny = max(y for x, y in points) + 1
    for y in range(ny):
        answer2 += '\n'
        for x in range(nx):
            answer2 += '#' if (x, y) in points else '.'

    return answer1, answer2
