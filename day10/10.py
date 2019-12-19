import math
import sys
from functools import partial
from pathlib import Path

import numpy as np


def pgrid(matrix, file=sys.stdout):
    for y in matrix:
        print('|' + '|'.join(['X' if x == 1 else '_' for x in y]) + '|', file=file)


np.set_printoptions(linewidth=150)
debug = partial(print, file=sys.stderr)
BLANK, ASTEROID = 0, 1
p = Path('input.txt')
# arr = [line for line in p.read_text().splitlines()]
arr = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''.splitlines()
arr = np.array([[BLANK if x == '.' else ASTEROID for x in y] for y in arr])

this_position = (8, 5)
y_ind, x_ind = this_position
visited = np.zeros_like(arr)
visited[this_position] = 1

# offsets to reach borders
rows, cols = arr.shape
up = y_ind, 0
down = rows - y_ind - 1, 0
left = 0, x_ind
right = 0, cols - x_ind - 1

pgrid(visited)
asteroid_positions = np.argwhere(arr == ASTEROID)
other_positions = asteroid_positions[np.all(asteroid_positions != this_position, axis=1)]

visible = 0
for ix in other_positions:
    d = ix - this_position
    multiplier = math.gcd(*d)
    d_base = d // multiplier
    d_obstacles = d_base[:, np.newaxis] * np.arange(1, multiplier)
    obstacles = this_position + d_obstacles.T
    if all(arr[tuple(obstacles.T)] == BLANK):
        visible += 1

print(visible)

# for y in arr:
#     for x in y:
#         print()
