from math import gcd
from itertools import combinations

import numpy as np

from pathlib import Path
import re

positions = Path('input.txt').read_text()
# positions = '''<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>'''


def print_state(ps, vs):
    for p, v in zip(ps, vs):
        print(p, v)


positions = positions.splitlines()
positions = [p.split(', ') for p in positions]
positions = [[int(re.search(r'-?\d+', c).group()) for c in p]
             for p in positions]

positions = np.array(positions)
velocities = np.zeros_like(positions)

start_positions, start_velocities = positions.copy(), velocities.copy()
time_steps = 3000

print_state(positions, velocities)


def simulate_step(posits, velos):
    # 1. gravity 2. velocity
    for a, b in combinations(range(len(posits)), 2):
        for i, (pa, pb) in enumerate(zip(posits[a], posits[b])):
            if pa < pb:
                d_v = 1
            elif pa > pb:
                d_v = -1
            else:
                d_v = 0

            velos[a, i] += d_v
            velos[b, i] -= d_v
    # 3. position
    posits += velos


for ts in range(1, time_steps + 1):
    simulate_step(positions, velocities)
    if np.array_equal(positions, start_positions) and np.array_equal(velocities, start_velocities):
        print('repeated state!')
        print(f'aftep step {ts}:')
        print_state(positions, velocities)
        break

potential = np.abs(positions).sum(axis=1)
kinetic = np.abs(velocities).sum(axis=1)
total = potential * kinetic
total_sum = total.sum()

print('Energy in the system:\n', np.column_stack((potential, kinetic, total)))
print('Total energy:', total_sum)


def lcm(a, b): return a * b // gcd(a, b)


steps_dim = []
total = 1
positions, velocities = start_positions.copy(), start_velocities.copy()
for i in range(positions.shape[1]):
    ps, vs = positions[:, i][..., np.newaxis], velocities[:, i][..., np.newaxis]
    start_ps, start_vs = start_positions[:, [i]], start_velocities[:, [i]]

    steps = 0
    while True:
        steps += 1
        simulate_step(ps, vs)
        if np.array_equal(ps, start_ps) and np.array_equal(vs, start_vs):
            break
    print(f'state for dim={i} repeated after {steps}')
    steps_dim.append(steps)

    total = lcm(total, steps)
    print(total)
