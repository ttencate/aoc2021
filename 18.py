import aoc


EXAMPLE1 = '''
[1,1]
[2,2]
[3,3]
[4,4]
'''

EXAMPLE2 = '''
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
'''

EXAMPLE3 = '''
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
'''

EXAMPLE4 = '''
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
'''

EXAMPLE5 = '''
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''


def parse(line):
    tokens = []
    for i in range(len(line)):
        char = line[i]
        if char in '[,]':
            tokens.append(char)
        else:
            assert(char.isdigit())
            tokens.append(int(char))
    return tokens

def add(a, b):
    return reduce(['['] + a + [','] + b + [']'])

def reduce(tokens):
    while True:
        tokens, exploded = explode(tokens)
        if exploded:
            continue
        tokens, splited = split(tokens)
        if splited:
            continue
        break
    return tokens

def explode(tokens):
    '''
    >>> def test(input):
    ...     tokens, _ = explode(parse(input))
    ...     return ''.join(map(str, tokens))
    >>> test('[[[[[9,8],1],2],3],4]')
    '[[[[0,9],2],3],4]'
    >>> test('[7,[6,[5,[4,[3,2]]]]]')
    '[7,[6,[5,[7,0]]]]'
    >>> test('[[6,[5,[4,[3,2]]]],1]')
    '[[6,[5,[7,0]]],3]'
    >>> test('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
    >>> test('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'
    '''
    nesting = 0
    for i in range(len(tokens)):
        token = tokens[i]
        if token == '[':
            nesting += 1
            if nesting == 5:
                left = tokens[i+1]
                right = tokens[i+3]
                assert(isinstance(left, int))
                assert(tokens[i+2] == ',')
                assert(isinstance(right, int))
                tokens = tokens[:i] + [0] + tokens[i+5:]
                for j in range(i - 1, -1, -1):
                    if isinstance(tokens[j], int):
                        tokens[j] += left
                        break
                for j in range(i + 1, len(tokens)):
                    if isinstance(tokens[j], int):
                        tokens[j] += right
                        break
                return tokens, True
        elif token == ']':
            nesting -= 1
    return tokens, False

def split(tokens):
    for i in range(len(tokens)):
        token = tokens[i]
        if isinstance(token, int) and token >= 10:
            tokens = tokens[:i] + ['[', token // 2, ',', (token + 1) // 2, ']'] + tokens[i+1:]
            return tokens, True
    return tokens, False

def add_all(input):
    '''
    >>> test = lambda input: ''.join(map(str, add_all(input)))
    >>> test(EXAMPLE1)
    '[[[[1,1],[2,2]],[3,3]],[4,4]]'
    >>> test(EXAMPLE2)
    '[[[[3,0],[5,3]],[4,4]],[5,5]]'
    >>> test(EXAMPLE3)
    '[[[[5,0],[7,4]],[5,5]],[6,6]]'
    >>> test(EXAMPLE4)
    '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    '''
    tokenss = map(parse, input.strip().splitlines())
    total = next(tokenss)
    for tokens in tokenss:
        total = add(total, tokens)
    return total

def magnitude(tokens):
    '''
    >>> magnitude(parse('[[1,2],[[3,4],5]]'))
    143
    >>> magnitude(parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'))
    3488
    '''
    def compute(cur):
        if tokens[cur] == '[':
            cur += 1
            magnitude = 0
            left, cur = compute(cur)
            assert(tokens[cur] == ',')
            cur += 1
            right, cur = compute(cur)
            assert(tokens[cur] == ']')
            cur += 1
            return 3 * left + 2 * right, cur
        else:
            assert(isinstance(tokens[cur], int))
            magnitude = tokens[cur]
            cur += 1
            return magnitude, cur
    return compute(0)[0]

def solve(input):
    '''
    >>> solve(EXAMPLE5)
    (4140, 3993)
    '''
    total = add_all(input)
    answer1 = magnitude(total)

    numbers = list(map(parse, input.strip().splitlines()))
    answer2 = max(magnitude(add(a, b)) for a in numbers for b in numbers)

    return answer1, answer2
