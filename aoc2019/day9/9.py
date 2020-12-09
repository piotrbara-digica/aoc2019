import sys
from functools import partial
from pathlib import Path

from aoc2019.intcode9 import Computer

debug = partial(print, file=sys.stderr)
p = Path('input.txt').read_text()

array = [int(x) for x in p.split(',')]
# array = [104,1125899906842624,99]
# array = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,day9]

computer = Computer(array, debug=False)
program = computer.run()
