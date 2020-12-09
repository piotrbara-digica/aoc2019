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
# a = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm
#
# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929
#
# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm
#
# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in'''.splitlines()

ps = []
p = {}
for line in a:
    if not line:
        ps.append(p)
        p = {}
    else:
        for x in line.split():
            k, v = x.split(':')
            p[k] = v
ps.append(p)

ps = list(filter(None, ps))
required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

part1 = 0
part2 = 0
for p in ps:
    if not required.issubset(p.keys()):
        continue
    part1 += 1

    valid = True
    for k, v in p.items():
        if k == 'byr':
            if not 1920 <= int(v) <= 2002:
                valid = False
        elif k == 'iyr':
            if not 2010 <= int(v) <= 2020:
                valid = False
        elif k == 'eyr':
            if not 2020 <= int(v) <= 2030:
                valid = False
        elif k == 'hgt':
            h = int(re.match('(\d+)', v).group())
            if v.endswith('cm'):
                if not 150 <= h <= 193:
                    valid = False
            elif v.endswith('in'):
                if not 59 <= h <= 76:
                    valid = False
            else:
                valid = False
        elif k == 'hcl':
            if not re.fullmatch('#[0-9a-f]{6}', v):
                valid = False
        elif k == 'ecl':
            if v not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
                valid = False
        elif k == 'pid':
            if not re.fullmatch('\d{9}', v):
                valid = False

    if valid:
        part2 += 1

print(part1), print(part2)
