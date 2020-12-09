import sys
from functools import partial
from pathlib import Path

from aoc2019.day5.intcode import Computer

debug = partial(print, file=sys.stderr)
p = Path('input5.txt')

array = [int(x) for x in p.read_text().split(',')]
# array = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,day9]

computer = Computer(array)
computer.run_program()
