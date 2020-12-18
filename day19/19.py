from datetime import datetime
from itertools import product
from pathlib import Path
import string
import numpy as np
import re

np.set_printoptions(linewidth=150)

inp = Path('input.txt').read_text().splitlines()
ex = '''5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'''


part1 = part2 = 0
print(part1)
print(part2)