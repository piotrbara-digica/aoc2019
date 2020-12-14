from itertools import combinations
from pathlib import Path

inp = Path('input.txt').read_text().splitlines()


def part1(code, plen=25):
    for i, num in enumerate(code[plen:]):
        if not any(num == sum(pair)
                   for pair in combinations(code[i: i + plen], 2)
                   if pair[0] != pair[1]):
            return num


def part2(code, want):
    code.remove(want)
    for r in range(2, 50):
        for i in range(len(code) - r):
            cont = code[i:i + r]
            if sum(cont) == want:
                return min(cont) + max(cont)


p1 = part1(inp, 25)
print(p1)
p2 = part2(inp, p1)
print(p2)
