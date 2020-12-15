import sys
from functools import partial
import itertools
from pathlib import Path

import numpy as np

debug = partial(print, file=sys.stderr)
np.set_printoptions(linewidth=150)

inp = Path('input.txt').read_text().splitlines()
inp = [int(i) for i in inp]

b = '''16 10 15 5 1 11 7 19 6 12 4'''.splitlines()
b = sorted(int(x) for x in b)


def part1(code):
    code = sorted(code)
    diff1 = 0
    diff3 = 0
    cur = 0
    left = set(code)
    while left:
        if cur + 1 in left:
            diff1 += 1
        elif cur + 2 in left:
            pass
        elif cur + 3 in left:
            diff3 += 1
        else:
            print('errror')

        cur = left.pop()
    cur += 3
    diff3 += 1

    print(diff1, diff3)
    return diff1 * diff3

def part2():
    pass

p1 = part1(b)
print(p1)
# part2(b)
