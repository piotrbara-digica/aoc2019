import numpy as np

from day9 import intcode9

from pathlib import Path

tiles = {
    0: ' ',
    1: '█',
    2: '▒',
    3: '▬',
    4: '◯',
}

code = Path('input.txt').read_text()
code = [int(c) for c in code.strip().split(',')]

computer = intcode9.Computer(code, False)
program = computer.run()
screen = np.zeros((25, 40), int)
for x in program:
    y, tile = next(program), next(program)
    screen[y, x] = tile


def draw():
    for row in screen:
        print(''.join(tiles[c] for c in row))


draw()
