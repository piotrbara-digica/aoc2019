import sys
from functools import partial
from pathlib import Path

import numpy as np

debug = partial(print, file=sys.stderr)
np.set_printoptions(linewidth=150)
a = Path('input.txt').read_text().splitlines()

grid_map = {'#': 1, '.': 0}
board = [[grid_map[c] for c in r] for r in a]


def part1(grid):
    rows, cols = len(grid), len(grid[0])
    rpos, cpos, res = 0, 0, 0
    sc, sr = 3, 1

    while rpos < rows:
        if grid[rpos][cpos % cols]:
            res += 1
        rpos += sr
        cpos += sc
    return res


def part2(grid):
    rows, cols = len(grid), len(grid[0])
    res = 1
    for sc, sr in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        rpos, cpos, trees = 0, 0, 0

        while rpos < rows:
            if grid[rpos][cpos % cols]:
                trees += 1

            rpos += sr
            cpos += sc
        res *= trees

    return res


print(part1(board))
print(part2(board))
