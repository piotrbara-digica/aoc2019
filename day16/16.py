import re
import os
from copy import deepcopy
import itertools
import math
import sys
from functools import partial
from pathlib import Path
from collections import Counter, defaultdict
from pprint import pprint
import math

import numpy as np
from tqdm import tqdm

np.set_printoptions(linewidth=150)

# inp = Path('input.txt').read_text().split(',')
# inp = [i for i in inp]

inp = '''7,12,1,0,16,2'''.split(',')
inp = [int(i) for i in inp]
a = '0,3,6'.split(',')
a = [int(i) for i in a]


def part1(x, maxt):
    # nums to their last turns
    mem = defaultdict(list)

    last = -1
    nums = []
    for t, num in enumerate(x):
        nums.append(num)
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
        nums.append(last)

    return last


p1 = part1(a, 2020)
p2 = part1(a, 30_000_000)

print(p1)

