import math
from pathlib import Path

inp = Path('input.txt').read_text().splitlines()

ns, ew = 0, 0
direction = 90  # 'east'

for x in inp:
    act, val = x[0], int(x[1:])

    if act == 'N':
        ns += val
    elif act == 'S':
        ns -= val
    elif act == 'E':
        ew += val
    elif act == 'W':
        ew -= val
    elif act == 'L':
        direction -= val
    elif act == 'R':
        direction += val
    elif act == 'F':
        r = math.radians(direction)
        dns = round(val * math.cos(r), 5)
        dew = round(val * math.sin(r), 5)
        ns += dns
        ew += dew
    else:
        raise ValueError

print('part1:', abs(ew) + abs(ns))

wew = 10
wns = 1
ew, ns = 0, 0

for x in inp:
    act, val = x[0], int(x[1:])

    if act == 'N':
        wns += val
    elif act == 'S':
        wns -= val
    elif act == 'E':
        wew += val
    elif act == 'W':
        wew -= val
    elif act in {'R', 'L'}:
        angle = math.atan2(wns, wew)
        d = math.sqrt(wns ** 2 + wew ** 2)
        rot_direction = +1 if act == 'L' else -1
        angle += rot_direction * math.radians(val)
        wew, wns = round(d * math.cos(angle)), round(d * math.sin(angle))

    elif act == 'F':
        ns += wns * val
        ew += wew * val

print('part2:', abs(ew) + abs(ns))
