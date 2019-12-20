import math
import sys
from collections import OrderedDict
from functools import partial
from pathlib import Path
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def pgrid(matrix, file=sys.stdout):
    grid = ''
    for y in matrix:
        grid += f'\n|{"|".join(["X" if x == 1 else "_" for x in y])}|'
    print(grid, file=file)


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
'''.splitlines()
arr = np.array([[BLANK if x == '.' else ASTEROID for x in y] for y in arr])

asteroid_positions = np.argwhere(arr == ASTEROID)

visible_counts = []
fast_solution = True

if not fast_solution:
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

        visible_counts.append(visible)
else:
    for this in tqdm(asteroid_positions, 'searching'):
        d_asteroids = asteroid_positions - this
        degrees = np.array([math.degrees(math.atan2(*d)) + 180 for d in d_asteroids], np.float64)
        visible = len(set(degrees))
        visible_counts.append(visible)

best_ix = int(np.argmax(visible_counts))
best_position = tuple(asteroid_positions[best_ix])
print(f'position: {best_position} asteroids visible: {visible_counts[best_ix]}')


# Part 2
def rad_2_wallclock_degrees(r):
    if r <= 0.5 * np.pi:
        r = -r + 0.5 * np.pi
    else:
        r = -r + 2.5 * np.pi

    return math.degrees(-r)


# print(best_position[1] * 100 + best_position[0])
asteroid_positions = asteroid_positions[np.any(asteroid_positions != best_position, axis=1)]
d_asteroids = asteroid_positions - best_position
distances = np.linalg.norm(d_asteroids, axis=1)
degrees = np.array([rad_2_wallclock_degrees(math.atan2(*d)) for d in d_asteroids], np.float64)
# sort by secondary key: distance
indices = np.argsort(distances, kind='stable')
asteroid_positions = asteroid_positions[indices]
degrees = degrees[indices]
distances = distances[indices]
# sort by primary key: degree of turn
indices = np.argsort(degrees, kind='stable')
asteroid_positions = asteroid_positions[indices]
degrees = degrees[indices]
distances = distances[indices]

to_destroy = {d: [] for d in set(degrees)}
for deg, ap in zip(degrees, asteroid_positions):
    to_destroy[deg].append(tuple(ap))

destroyed = np.zeros_like(arr)
destroyed[best_position] = 1
for p, deg, dist in zip(asteroid_positions, degrees, distances):
    destroyed[tuple(p)] = 1
    plt.matshow(destroyed, 0)
    pgrid(destroyed)
    print(f'{p}\t{deg:.2f}\t{dist:.2f}')
    sleep(0.1)
