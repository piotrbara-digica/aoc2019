import sys
from functools import partial
from pathlib import Path

debug = partial(print, file=sys.stderr)
array = [line.split(')') for line in Path('input6.txt').read_text().splitlines()]

# object directly orbits only one other
orbited = {b: a for a, b in array}  # which object does B orbit

total_count = 0
for obj in orbited:
    while obj != "COM":  # go to root
        obj = orbited[obj]
        total_count += 1

print(total_count)  # sum of distances to COM from every object

obj = orbited['YOU']
a_path = []
while obj != 'COM':
    a_path.append(obj)
    obj = orbited[obj]

obj = orbited['SAN']
b_path = []
while obj != 'COM':
    b_path.append(obj)
    obj = orbited[obj]

while a_path[-1] == b_path[-1]:
    a_path.pop(), b_path.pop()

print(len(a_path) + len(b_path))
