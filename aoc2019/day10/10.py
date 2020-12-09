import math
import sys
from functools import partial
from pathlib import Path

import numpy as np
from tqdm import tqdm


def pgrid(matrix, file=sys.stdout):
    field = ''
    for y in matrix:
        field += f'\n|{"|".join(["X" if x == 1 else "_" for x in y])}|'
    print(field, file=file)


np.set_printoptions(2, linewidth=150)
debug = partial(print, file=sys.stderr)
BLANK, ASTEROID = 0, 1
p = Path('input.txt')
grid = [line for line in p.read_text().splitlines()]
grid = np.array([[BLANK if x == '.' else ASTEROID for x in y] for y in grid])

asteroid_positions = np.argwhere(grid == ASTEROID)

visible_counts = []
for this in tqdm(asteroid_positions, 'searching'):
    d_asteroids = asteroid_positions - this
    azimuths = np.array([math.degrees(math.atan2(*d)) + 180 for d in d_asteroids], np.float64)
    visible = len(set(azimuths))
    visible_counts.append(visible)

best_ix = int(np.argmax(visible_counts))
best_position = tuple(asteroid_positions[best_ix])
print(f'position: {best_position} asteroids visible: {visible_counts[best_ix]}')


# Part 2
def displacement_2_azimuth(disp_vector):
    # displacement vector to angle in [-pi, pi]
    y, x = disp_vector
    r = math.atan2(-y, x)  # GOTCHA: numpy's Y axis is inverted
    # angle to angle in [0, 2pi], clockwise rotation
    if r <= 0.5 * np.pi:
        r = -r + 0.5 * np.pi
    else:
        r = -r + 2.5 * np.pi

    return math.degrees(r)


asteroid_positions = asteroid_positions[np.any(asteroid_positions != best_position, axis=1)]
d_asteroids = asteroid_positions - best_position
distances = np.linalg.norm(d_asteroids, axis=1)
azimuths = np.array([displacement_2_azimuth(d) for d in d_asteroids], np.float64)
# sort by secondary key: distance, descending
indices = np.argsort(-distances, kind='stable')
asteroid_positions = asteroid_positions[indices]
azimuths = azimuths[indices]
distances = distances[indices]
# sort by primary key: azimuth
indices = np.argsort(azimuths, kind='stable')
asteroid_positions = asteroid_positions[indices]
azimuths = azimuths[indices]
distances = distances[indices]

to_destroy = {d: [] for d in set(azimuths)}
for deg, ap in zip(azimuths, asteroid_positions):
    to_destroy[deg].append(tuple(ap))

asteroids_destroyed = []
while to_destroy:
    azimuths_queue = sorted(to_destroy)
    for k in azimuths_queue:
        if to_destroy[k]:
            print(f'{k:.2f}\t\t{to_destroy[k][-1]}')
            asteroids_destroyed.append(to_destroy[k].pop())
        else:
            del to_destroy[k]

target = asteroids_destroyed[200 - 1]
print('200th target:', target[1] * 100 + target[0])

# for ast in asteroids_destroyed:
#     grid[tuple(ast)] = 0
#     plt.matshow(grid, 0)
#     plt.show()
#     pgrid(grid)
#     sleep(0.15)
