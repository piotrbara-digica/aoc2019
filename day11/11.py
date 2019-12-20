import sys
from functools import partial
from pathlib import Path

import numpy as np

from day9.intcode9 import Computer

np.set_printoptions(2, linewidth=150)
debug = partial(print, file=sys.stderr)
BLACK, WHITE = 0, 1

grid = np.zeros((1000, 1000), int)
start_position = grid.shape[0] // 2, grid.shape[1] // 2

# Moves: mind numpy's inverted Y axis
up = -1, 0
down = 1, 0
left = 0, -1
right = 0, 1

p = Path('input.txt')
code = [int(line) for line in p.read_text().split(',')]
computer = Computer(code, debug=False)
computer.run()
