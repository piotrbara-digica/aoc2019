from pathlib import Path

inp = Path('input.txt').read_text()
part1, part2 = 0, 0

want = 'shiny gold'
rules = {}

for line in inp.splitlines():
    rule = line.replace('bags', '').replace('bag', '').split('contain')
    outer, inners = rule
    outer = outer.strip()

    inners = [i.strip().split(' ', 1) for i in inners.strip('. ').split(',')]
    inners = [(int(n), color) for n, color in inners if n != 'no']
    rules[outer] = inners


def all_containers_of(bag):
    containers = set()
    for outer, inners in rules.items():
        if bag in {col for _, col in inners}:
            containers.add(outer)
            containers |= all_containers_of(outer)

    return containers


part1 = all_containers_of(want)
print(len(part1))


def bags_within(container) -> int:
    bags = 0
    for n, color in rules[container]:
        bags += n + n * bags_within(color)
        print(container, '->', n, color)

    return bags


part2 = bags_within(want)
print(part2)
