import math
import sys
from functools import partial
from pathlib import Path

import numpy as np
from tqdm import tqdm


def pgrid(matrix, file=sys.stdout):
    for y in matrix:
        print('|' + '|'.join(['X' if x == 1 else '_' for x in y]) + '|', file=file)


np.set_printoptions(3, linewidth=150)
debug = partial(print, file=sys.stderr)
BLANK, ASTEROID = 0, 1
p = Path('input.txt')
# arr = [line for line in p.read_text().splitlines()]
arr = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''
arr = np.array([[BLANK if x == '.' else ASTEROID for x in y] for y in arr.splitlines()])

# this_position = (8, 5)
# y_ind, x_ind = this_position
# visited = np.zeros_like(arr)
# visited[this_position] = 1
#
# # offsets to reach borders
# rows, cols = arr.shape
# up = y_ind, 0
# down = rows - y_ind - 1, 0
# left = 0, x_ind
# right = 0, cols - x_ind - 1
#
# pgrid(visited)

asteroid_positions = np.argwhere(arr == ASTEROID)

position_counts = []
for this in tqdm(asteroid_positions, 'searching'):
    visible = 0
    for other in asteroid_positions:
        d = other - this
        if np.all(d == 0):
            continue

        multiplier = math.gcd(*d)
        d_base = d // multiplier
        d_obstacles = d_base[:, np.newaxis] * np.arange(1, multiplier)
        obstacles = this + d_obstacles.T
        if all(arr[tuple(obstacles.T)] == BLANK):
            visible += 1

    position_counts.append(visible)

print(position_counts)
best_ix = np.argmax(position_counts)
best_position = asteroid_positions[best_ix]
print(f'position: {best_position} asteroids visible: {position_counts[best_ix]}')
print(best_position[1] * 100 + best_position[0])
# The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which
# asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate?
# (For example, 8,2 becomes 802.)
d_asteroids = best_position - asteroid_positions
degrees = np.array([math.degrees(math.atan2(*d)) + 180 for d in d_asteroids], np.float64)
# second solution to first part...
print(np.unique(np.sort(degrees)).shape)
