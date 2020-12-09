import re
import os
from itertools import *
import math
import sys
from functools import partial
from pathlib import Path
from collections import Counter
import numpy as np
from numpy import array as arr

debug = partial(print, file=sys.stderr)
np.set_printoptions(linewidth=150)

a = Path('input.txt').read_text().splitlines()

seats = []
for bp in a: # original approach
    row, col = bp[:7], bp[-3:]
    row = sum([(0 if c == 'F' else 1) * 2 ** pow for pow, c in enumerate(reversed(row))])
    col = sum([(0 if c == 'L' else 1) * 2 ** pow for pow, c in enumerate(reversed(col))])
    seat = row * 8 + col
    seats.append(seat)

# approach 2, better: treat BP identifier as one number
tab = str.maketrans('FBLR', '0101')
seats2 = [int(bp.translate(tab), 2) for bp in a]

print(max(seats))
sts = sorted(seats)
diff_idx = np.diff(sts).argmax()
part2 = sts[diff_idx] + 1
print(part2)

# approach 2
sts = set(seats)
for i in range(max(seats)):
    if i not in sts and i + 1 in sts and i - 1 in sts:
        print(i)


# CODE GOLF!
a = open('input.txt').readlines()
print(max(s := [int(x.translate(str.maketrans('FBLR', '0101')), 2) for x in a]))
s = sorted(s);print(s[np.diff(s).argmax()]+1)  # part 2