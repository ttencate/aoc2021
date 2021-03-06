#!/usr/bin/env python3

import argparse
import datetime
import doctest
import importlib
import os
import os.path
import subprocess
import sys
import urllib.request

import pytz


TEMPLATE = """import aoc


EXAMPLE1 = '''
'''


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    '''
"""


def load_session_cookie():
    filename = '.session_cookie'
    try:
        with open(filename, 'rt') as f:
            return f.read().strip()
    except IOError as ex:
        pass

    print('Get the value of the `session` cookie from your browser console and paste it here:')
    session_cookie = input().strip()
    with open(filename, 'wt') as f:
        f.write(session_cookie + '\n')
    return session_cookie


def fetch(url):
    session_cookie = load_session_cookie()
    request = urllib.request.Request(url, headers={
        'Host': 'adventofcode.com',
        'Accept': '*/*',
        'User-Agent': 'Solutions by ttencate <https://github.com/ttencate/aoc2021>',
        'Cookie': f'session={session_cookie}',
    })
    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as ex:
        print(ex.reason)
        raise


def get_puzzle_input(year, day):
    filename = os.path.join('input', f'{day:02}.in')
    try:
        with open(filename, 'rt') as f:
            return f.read()
    except IOError as ex:
        pass

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    print(f'Fetching puzzle input from {url}')
    puzzle_input = fetch(url)
    with open(filename, 'wt') as f:
        f.write(puzzle_input)
    return puzzle_input


def print_answer(day, part, answer):
    print(f'Answer to day {day} part {part}: {answer}')


def main():
    parser = argparse.ArgumentParser(description='Runs Advent of Code puzzle solutions or tests')
    parser.add_argument('--day', type=int, choices=range(1, 25+1),
                        default=datetime.datetime.now(tz=pytz.timezone('EST')).day,
                        help='Day indicating which solution to run (1-25); defaults to today')
    parser.add_argument('--year', type=int, default=2021,
                        help='Year indicating which solution to run')
    parser.add_argument('--skip_tests', action='store_true',
                        help='Skip doctests and go straight to the puzzle input')
    args = parser.parse_args()

    year = args.year
    day = args.day

    os.chdir(os.path.dirname(__file__))

    filename = f'{day:02}.py'
    if not os.path.exists(filename):
        print(f'Creating {filename}')
        with open(filename, 'wt') as f:
            f.write(TEMPLATE)

        url = f'https://adventofcode.com/{year}/day/{day}'
        print(f'Opening {url} in browser')
        subprocess.run(['xdg-open', url])

        get_puzzle_input(year, day)

        print(f'Launching editor')
        subprocess.run([
            'vim', '-p',
            filename, 
            os.path.join('input', f'{day:02}.in')
        ])

        return

    module = importlib.import_module(f'{day:02}')

    if not args.skip_tests:
        (failure_count, test_count) = doctest.testmod(module)
        if test_count == 0:
            print('Warning: no doctests found')
        else:
            print(f'Doctest: {test_count - failure_count}/{test_count} passed')
        if failure_count > 0:
            return 1

    puzzle_input = get_puzzle_input(year, day)
    answer = module.solve(puzzle_input)

    if answer is None:
        print('solve() returned None; please implement it')
    else:
        if isinstance(answer, tuple):
            print_answer(day, 1, answer[0])
            if len(answer) >= 2:
                print_answer(day, 2, answer[1])
        else:
            print_answer(day, 1, answer)

    return 0


if __name__ == '__main__':
    sys.exit(main())
