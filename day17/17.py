from datetime import datetime
from itertools import product
from pathlib import Path

import numpy as np

np.set_printoptions(linewidth=150)

inp = Path('input.txt').read_text().splitlines()

# plane z = 0
ex = '''.#.
..#
###'''.splitlines()


def step(g) -> [[[int]]]:
    npg = np.array(g)
    npg = np.pad(npg, 2, 'constant', constant_values='.')
    n_z, n_y, n_x = npg.shape
    g: list = npg.tolist()
    ng = np.zeros_like(npg)
    ng[:] = '.'

    dims = 3
    neighbors = list(n for n in product((-1, 0, 1), repeat=dims) if any(n))
    to_check = product(range(1, n_z - 1), range(1, n_y - 1), range(1, n_x - 1))
    for z, y, x in to_check:
        an = sum(g[z + az][y + ay][x + ax] == '#' for az, ay, ax in neighbors)
        this = g[z][y][x]
        if (this == '.' and an == 3) or (this == '#' and an in [2, 3]):
            ng[z][y][x] = '#'
    return ng


grid = [[col for col in row] for row in inp]
grid = [grid]

tic = datetime.now()
for i in range(6):
    # print(i, np.count_nonzero(np.array(grid) == '#'))
    grid = step(grid)
toc = datetime.now()
print(f'took: {toc - tic}')
print(np.count_nonzero(np.array(grid) == '#'))


def step_1(active):
    new_active = {}
    dims = 3
    neighbors = list(n for n in product((-1, 0, 1), repeat=dims) if any(n))
    to_check = product(
        *(range(min(k[dim] for k in active) - 1, max(k[dim] for k in active) + 2)
          for dim in range(dims))
    )
    for (x, y, z) in to_check:
        s = active.get((x, y, z), False)
        an = 0
        for dx, dy, dz in neighbors:
            if dx == dy == dz == 0:
                continue
            if active.get((x + dx, y + dy, z + dz), False):
                an += 1

        if (s and an in (2, 3)) or (not s and an == 3):
            # new_active.add((x, y, z))
            new_active[x, y, z] = True
    assert all(n for n in new_active.values())
    return new_active


def step_2(actives):
    ng = {}
    dims = 4
    neighbors = list(n for n in product((-1, 0, 1), repeat=dims) if any(n))
    to_check = product(
        *(range(min(k[dim] for k in actives) - 1, max(k[dim] for k in actives) + 2)
          for dim in range(dims))
    )
    for (x, y, z, q) in to_check:
        s = actives.get((x, y, z, q), False)
        an = sum(actives.get((x + dx, y + dy, z + dz, q + dq), False)
                 for dx, dy, dz, dq in neighbors)
        if (s and an in (2, 3)) or (not s and an == 3):
            ng[(x, y, z, q)] = True
    return ng


grid = {}
for row, line in enumerate(inp):
    for col, ch in enumerate(line):
        grid[(col, row, 0)] = ch == '#'

tic = datetime.now()
for i in range(6):
    grid = step_1(grid)
toc = datetime.now()
print(f'took: {toc - tic}')
print(len(grid))

grid = {}
for row, line in enumerate(inp):
    for col, ch in enumerate(line):
        grid[(col, row, 0, 0)] = ch == '#'

tic = datetime.now()
for i in range(6):
    print(i, sum(grid.values()))
    grid = step_2(grid)
print(sum(grid.values()))
toc = datetime.now()
print(f'took: {toc - tic}')
