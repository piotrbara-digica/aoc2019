from itertools import count
from pathlib import Path

import numpy as np
from scipy.signal import convolve2d

np.set_printoptions(linewidth=150)

inp = Path('input.txt').read_text().splitlines()
inp = [[x for x in i] for i in inp]

grid = np.array(inp)
next_grid = grid.copy()
kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

for i in count(1):
    empty_mask = (grid == 'L').astype(int)
    occ_mask = (grid == '#').astype(int)

    occ_counts = convolve2d(occ_mask, kernel, 'same')
    to_sit = (occ_counts == 0) & empty_mask
    to_free = (occ_counts >= 4) & occ_mask
    next_grid[to_sit == True] = '#'
    next_grid[to_free == True] = 'L'

    if np.array_equal(next_grid, grid):
        print(f'stabilized after {i} rounds')
        break
    grid = next_grid.copy()

part1 = np.count_nonzero(grid == '#')
print('part1:', part1)

grid = inp
grid = np.array(grid)
next_grid = grid.copy()


def count_8way_seats(x: np.ndarray) -> np.ndarray:
    counts = -np.ones_like(x, int)

    for r, c in np.argwhere(x != '.'):
        # [left, up, upr] are reversed for coords to be ordered by distance, ascending
        right = x[r, c:][1:]
        left = x[r, :c][::-1]
        up = x[:r, c][::-1]
        down = x[r:, c][1:]

        offset = c - r
        upl = x[:r, :c].diagonal(offset)[::-1]
        downr = x[r + 1:, c + 1:].diagonal()
        upr = np.flipud(x[:r, c + 1:]).diagonal()
        downl = np.fliplr(x[r + 1:, :c]).diagonal()

        ct = 0
        for d in [up, down, left, right, upl, downr, upr, downl]:
            nearest = next((spot for spot in d if spot != '.'), None)
            if nearest == '#':
                ct += 1

        counts[r, c] = ct

    return counts


for i in count(1):
    occ_counts = count_8way_seats(grid)

    to_sit = (occ_counts == 0)
    to_free = (occ_counts >= 5)
    next_grid[to_sit == 1] = '#'
    next_grid[to_free == 1] = 'L'

    if np.array_equal(next_grid, grid):
        print(i, 'changes')
        break

    grid = next_grid.copy()

part2 = np.count_nonzero(grid == '#')
print('part2:', part2)
