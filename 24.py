import functools

import aoc


EXAMPLE1 = '''
inp x
mul x -1
'''


EXAMPLE2 = '''
inp z
inp x
mul z 3
eql z x
'''


EXAMPLE3 = '''
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
'''


def generate_python(input):
    '''
    >>> print(generate_python(EXAMPLE2))
    z = next(inp)
    x = next(inp)
    z *= 3
    z = 1 if z == x else 0
    '''
    code = []
    for line in input.strip().splitlines():
        parts = line.split()
        instr, *args = parts
        for arg in args:
            if arg not in 'xyzw':
                int(arg)
        if instr == 'inp':
            code.append(f'{args[0]} = next(inp)')
        elif instr == 'add':
            code.append(f'{args[0]} += {args[1]}')
        elif instr == 'mul':
            code.append(f'{args[0]} *= {args[1]}')
        elif instr == 'div':
            code.append(f'{args[0]} //= {args[1]}')
        elif instr == 'mod':
            code.append(f'{args[0]} %= {args[1]}')
        elif instr == 'eql':
            code.append(f'{args[0]} = 1 if {args[0]} == {args[1]} else 0')
        else:
            assert False, line
    return '\n'.join(code)


def compile_python(code):
    return compile(code, '<AOC input>', 'exec')


def run(code, inp):
    '''
    >>> run(compile_python(generate_python(EXAMPLE1)), [5])['x']
    -5
    >>> run(compile_python(generate_python(EXAMPLE2)), [3, 8])['z']
    0
    >>> run(compile_python(generate_python(EXAMPLE2)), [3, 9])['z']
    1
    '''
    registers = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
    eval(code, {'inp': iter(inp)}, registers)
    return registers


# Input-specific constants.
A = [  1,   1,   1,  26,   1,  26,   1,   1,   1,  26,  26,  26,  26,  26]
B = [ 15,  12,  13, -14,  15,  -7,  14,  15,  15,  -7,  -8,  -7,  -5, -10]
C = [ 15,   5,   6,   7,   9,   6,  14,   3,   1,   3,   4,   6,   7,   1]


def next_z(z, i, w):
    x = (z % 26 + B[i]) != w
    z //= A[i]
    if x:
        z = z * 26 + w + C[i]
    return z


def compute_z(model_number):
    '''
    This function is just to check my understanding and to test `next_z`, but
    not actually used in solving the problem.

    >>> with open('input/24.in') as f:
    ...     monad = compile_python(generate_python(f.read()))
    >>> model_number = list(map(int, '13579246899999'))
    >>> run(monad, model_number)['z']
    5044254108
    >>> compute_z(model_number)
    5044254108
    '''
    z = 0
    for i, w in enumerate(model_number):
        z = next_z(z, i, w)
    return z


def solve(unused_input):
    '''
    >>> solve('')
    (49917929934999, 11911316711816)
    '''
    return solve_part(range(9, -1, -1)), solve_part(range(1, 10, 1))


def solve_part(ws):
    table = [0]
    for i in range(13, -1, -1):
        next_table = []
        # Upper bound determined empirically. pypy recommended. Probably a
        # memoized recursive function would be faster because we avoid all the
        # None cases.
        for z in range(26**5):
            best_number = None
            for w in ws:
                nz = next_z(z, i, w)
                if nz < len(table) and table[nz] is not None:
                    best_number = w * 10**(13 - i) + table[nz]
                    break
            next_table.append(best_number)
        table = next_table
    return table[0]
