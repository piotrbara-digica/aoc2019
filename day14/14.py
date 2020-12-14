import re
from collections import defaultdict
from pathlib import Path

inp = Path('input.txt').read_text().splitlines()

mask = None
mem = {}
for x in inp:
    com, val = x.split(' = ')

    if 'mem' in com:
        addr = int(re.search('\d+', com).group())
        bval = format(int(val), '036b')
        masked = ''.join(m if m != 'X' else v for m, v in zip(mask, bval))
        mem[addr] = int(masked, 2)
    else:
        mask = val

part1 = sum(mem.values())
print(part1)

mem = defaultdict(int)
masked = None
for x in inp:
    com, val = x.split(' = ')

    if 'mem' in com:
        addr = int(re.search('\d+', com).group())
        baddr = format(int(addr), '036b')

        masked = ''.join(m if m != '0' else abit for m, abit in zip(mask, baddr))

        nx = masked.count('X')
        possible_x_bits = (format(w, f'0{nx}b') for w in range(2 ** nx))
        addresses = []
        for way in possible_x_bits:
            address = list(masked)
            i_x = 0
            for i, char in enumerate(masked):
                if char == 'X':
                    address[i] = way[i_x]
                    i_x += 1

            addresses.append(int(''.join(address), 2))
        assert len(set(addresses)) == len(addresses)

        for a in addresses:
            mem[a] = int(val)

    else:
        mask = val

part2 = sum(mem.values())
print(part2)
