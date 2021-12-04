import copy

import aoc


EXAMPLE1 = '''
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (4512, 1924)
    '''
    lines = iter(input.strip().splitlines())
    draws = list(map(int, next(lines).split(',')))
    next(lines)
    boards = []
    while True:
        board = []
        while True:
            line = next(lines, None)
            if not line:
                break
            board.append(list(map(int, line.split())))
        boards.append(board)
        if line is None:
            break

    return part1(draws, copy.deepcopy(boards)), part2(draws, copy.deepcopy(boards))


def part1(draws, boards):
    for draw in draws:
        for board in boards:
            mark_number(draw, board)
            if is_won(board):
                return score(board, draw)


def part2(draws, boards):
    board_count = len(boards)
    won_count = 0
    for draw in draws:
        next_boards = []
        for board in boards:
            mark_number(draw, board)
            if is_won(board):
                won_count += 1
                if won_count == board_count:
                    return score(board, draw)
            else:
                next_boards.append(board)
        boards = next_boards


def mark_number(draw, board):
    for row in board:
        for i in range(len(row)):
            if row[i] == draw:
                row[i] = None


def is_won(board):
    for row in board:
        if all(square is None for square in row):
            return True
    for i in range(len(board[0])):
        if all(row[i] is None for row in board):
            return True
    return False


def score(board, draw):
    return sum(sum(square for square in row if square is not None) for row in board) * draw
