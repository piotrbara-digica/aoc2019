import string
from collections import Counter
from pathlib import Path

inp = Path('input.txt').read_text().split('\n\n')
part1, part2 = 0, 0

groups = inp

for group in groups:
    glets = set(group.replace('\n', ''))
    part1 += len(glets)
# OR: part1 = sum(len(set(g.replace('\n', ''))) for g in groups)
print(part1)

for group in groups:
    group = group.strip()
    members = group.count('\n') + 1
    counts = Counter(group.replace('\n', ''))
    part2 += sum(c == members for c in counts.values())

print(part2)
# approach 2
part2 = 0
for group in groups:
    alls = set(string.ascii_lowercase)
    for p in group.strip().split():
        alls &= set(p)
    part2 += len(alls)

print(part2)
