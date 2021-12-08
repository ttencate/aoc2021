import aoc


EXAMPLE1 = '''
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (26, 61229)
    '''
    answer1 = 0
    answer2 = 0

    for line in input.strip().splitlines():
        clue, output = [
            [set(digit) for digit in part.split()]
            for part in line.split(' | ')
        ]

        for digit in output:
            if len(digit) in [2, 3, 4, 7]:
                answer1 += 1

        def find(pred):
            for digit in clue:
                if pred(digit):
                    return digit
            assert False
        digits = [None] * 10
        # Digits 1, 4, 7 and 8 are uniquely identified by their segment count.
        digits[1] = find(lambda d: len(d) == 2)
        digits[7] = find(lambda d: len(d) == 3)
        digits[4] = find(lambda d: len(d) == 4)
        digits[8] = find(lambda d: len(d) == 7)
        # Digits 0, 6 and 9 all have six segments:
        # - 0 is a superset of 7 but not of 4
        # - 6 is a superset of neither 7 nor 4
        # - 9 is a superset of 7 and 4
        digits[0] = find(lambda d: len(d) == 6 and d > digits[7] and not d > digits[4])
        digits[6] = find(lambda d: len(d) == 6 and not d > digits[7] and not d > digits[4])
        digits[9] = find(lambda d: len(d) == 6 and d > digits[7] and d > digits[4])
        # Digits 2, 3 and 5 all have five segments:
        # - 3 is a superset of 1, the other two aren't
        # - 5 is a subset of 9, but 2 isn't
        digits[3] = find(lambda d: len(d) == 5 and d > digits[1])
        digits[5] = find(lambda d: len(d) == 5 and d != digits[3] and d < digits[9])
        digits[2] = find(lambda d: len(d) == 5 and d != digits[3] and d != digits[5])
        answer2 += int(''.join(str(digits.index(digit)) for digit in output))

    return answer1, answer2
