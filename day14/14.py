import math
import re
from collections import defaultdict
from pathlib import Path


def get_reactions(filename=None):
    if not filename:
        filename = 'input.txt'

    in_text = Path(filename).read_text().rstrip()

    reactions = {}
    for line in in_text.splitlines():
        match = re.search(r'^((?:\d+ [A-Z]+, )*\d+ [A-Z]+) => (\d+) ([A-Z]+)$', line)
        output_amount = int(match.group(2))
        output_name = match.group(3)
        inputs = []
        for in_text in match.group(1).split(', '):
            input_amount, in_name = in_text.split(' ')
            inputs.append((int(input_amount), in_name))
        reactions[output_name] = (output_amount, inputs)
    return reactions


def calc_ore(reactions: {str: (int, [(int, str)])},
             target: str, target_amount: int,
             surplus: {str: int} = None):
    if surplus is None:
        surplus = defaultdict(int)

    if target == 'ORE':  # base case -> end of the reaction chain
        return target_amount
    elif surplus[target] >= target_amount:  # product already made -> use the surplus
        surplus[target] -= target_amount
        return 0

    target_amount -= surplus[target]  # use the surplus if any
    surplus[target] = 0
    output_amount, inputs = reactions[target]

    ore = 0
    multiplier = math.ceil(target_amount / output_amount)
    for in_amount, in_name in inputs:
        in_amount *= multiplier
        # go backwards in reaction chain/tree, depth first
        ore += calc_ore(reactions, in_name, in_amount, surplus)

    surplus[target] += output_amount * multiplier - target_amount

    return ore


def part1(reactions):
    return calc_ore(reactions, 'FUEL', 1)


def part2(reactions):
    ore_given = int(1e12)
    target_amount = ore_given // part1(reactions)
    fuel = 0
    surplus = defaultdict(int)
    while ore_given and target_amount:
        new_surplus = defaultdict(int, surplus)
        ore_used = calc_ore(reactions, 'FUEL', target_amount, new_surplus)
        if ore_used > ore_given:
            target_amount //= 2
        else:
            fuel += target_amount
            ore_given -= ore_used
            surplus = new_surplus

    return fuel


def part2_binary_search(reactions):
    ore_given = int(1e12)
    low_fuel = ore_given // part1(reactions)
    high_fuel = 2 * low_fuel

    class FuelRange:
        def __getitem__(self, amount):
            return calc_ore(reactions, 'FUEL', amount)

    from bisect import bisect
    fuel = bisect(FuelRange(), ore_given, low_fuel, high_fuel) - 1
    return fuel


def part2_fastest(reactions):
    ore_given = int(1e12)
    fuel = 1
    while True:
        ore = calc_ore(reactions, 'FUEL', fuel + 1)
        if ore > ore_given:
            return fuel
        else:
            fuel = max(fuel + 1, ((fuel + 1) * ore_given) // ore)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('input', nargs='?', metavar='input.txt')
    args = parser.parse_args()
    text_input = get_reactions(args.input)
    print(part1(text_input))
    print(part2(text_input))  # 40 iterations
    print(part2_binary_search(text_input))  # 23 iterations
    print(part2_fastest(text_input))  # 3 iterations!
