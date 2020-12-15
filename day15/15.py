from collections import defaultdict

import numpy as np
from tqdm import tqdm

np.set_printoptions(linewidth=150)

# inp = Path('input.txt').read_text().split(',')
# inp = [i for i in inp]
inp = '''7,12,1,0,16,2'''.split(',')
inp = [int(i) for i in inp]
ex = '0,3,6'.split(',')
ex = [int(i) for i in ex]


def part1(x, maxt):
    # nums to their last turns
    mem = defaultdict(list)
    last = -1
    for t, num in enumerate(x):
        mem[num].append(t + 1)
        last = num

    for t in tqdm(range(len(x) + 1, maxt + 1)):
        mem_last = mem[last]
        n = len(mem_last)
        if n == 1:
            last = 0
        elif n > 1:
            last = mem_last[-1] - mem_last[-2]

        mem[last].append(t)

    return last


def f(x, limit):
    # nums to their last turns [0-indexed] except last turn
    d = {n: t for t, n in enumerate(x[:-1])}
    n = x[-1]  # last number
    for t in tqdm(range(len(x), limit)):
        if n in d:
            new = t - 1 - d[n]
        else:
            new = 0
        d[n] = t - 1
        n = new
    return n


p1 = part1(inp, 2020)
p2 = part1(inp, 30_000_000)

print(p1)
