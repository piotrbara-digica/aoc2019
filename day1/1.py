import itertools
import math
import sys
from functools import partial
from pathlib import Path

debug = partial(print, file=sys.stderr)
p = Path('input.txt')
a = [int(line) for line in p.read_text().splitlines()]


def part1():
    for x in a:
        for y in a[1:]:
            if x + y == 2020:
                print(x * y, x, y)
                return


# one-liner
next((x * y, x, y) for x in a for y in a[1:] if x + y == 2020)
# one-liner 2
next((math.prod(n), n) for n in itertools.combinations(a, 2) if sum(n) == 2020)


def part2():
    for x in a:
        for y in a[1:]:
            for z in a[2:]:
                if x + y + z == 2020:
                    print(x * y * z, x, y, z)
                    return


# one-liner 1
next((x * y * z, x, y, z)
     for x in a for y in a[1:] for z in a[2:]
     if x + y + z == 2020)
# one-liner 2
next((math.prod(n), n) for n in itertools.combinations(a, 3) if sum(n) == 2020)

part1()
part2()
