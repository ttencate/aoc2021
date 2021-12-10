import aoc


EXAMPLE1 = '''
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (26397, 288957)
    '''
    answer1 = 0
    answer2_scores = []
    for line in input.strip().splitlines():
        try:
            parse(line)
        except Corrupted as ex:
            answer1 += {')': 3, ']': 57, '}': 1197, '>': 25137}[ex.char]
        except Incomplete as ex:
            score = 0
            for char in ex.missing:
                score = (score * 5) + {')': 1, ']': 2, '}': 3, '>': 4}[char]
            answer2_scores.append(score)
    answer2_scores.sort()
    answer2 = answer2_scores[len(answer2_scores) // 2]
    return answer1, answer2


def parse(line, curr=0):
    if curr >= len(line):
        return
    start_char = line[curr]
    end_char = {'(': ')', '[': ']', '{': '}', '<': '>'}.get(start_char, None)
    if end_char is None:
        raise Corrupted(start_char)
    curr += 1
    while curr < len(line) and line[curr] != end_char:
        try:
            curr = parse(line, curr)
        except Incomplete as ex:
            raise Incomplete(ex.missing + end_char)
    if curr >= len(line):
        raise Incomplete(end_char)
    curr += 1
    return curr
    

class Corrupted(Exception):
    def __init__(self, char):
        self.char = char


class Incomplete(Exception):
    def __init__(self, missing):
        self.missing = missing
