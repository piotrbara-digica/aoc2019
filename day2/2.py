import re
import sys
from functools import partial
from pathlib import Path

debug = partial(print, file=sys.stderr)
p = Path('input.txt')
a = [line for line in p.read_text().splitlines()]

correct1, correct2 = 0, 0

for line in a:
    # ns, let, pwrd = line.split()
    # lo, hi = [int(n) for n in ns.split('-')]
    # let = let[0]
    lo, hi, let, pwrd = re.match(r'(\d+)-(\d+) (\w): (\w+)', line).groups()
    lo, hi = int(lo), int(hi)

    if pwrd.count(let) in range(lo, hi + 1):
        correct1 += 1

    if (pwrd[lo - 1] == let) ^ (pwrd[hi - 1] == let):  # only one
        correct2 += 1

print(correct1, correct2)
