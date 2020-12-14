from functools import reduce
from pathlib import Path

inp = Path('input.txt').read_text().splitlines()


def chinese_remainder(n: [int], a: [int]) -> int:
    # x % n[0] == a[0]
    # x % n[1] == a[1]
    # x % n[2] == a[2]
    # ...
    sum_ = 0
    prod = reduce(lambda x1, x2: x1 * x2, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_ += a_i * mul_inv(p, n_i) * p
    return sum_ % prod


def mul_inv(a: int, b: int) -> int:
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


x = inp
now = int(x[0])
buses = [int(i) if i != 'x' else 0 for i in x[1].split(',')]

min_wait, bus_id = min([(b - now % b, b) for b in buses if b != 0])
part1 = min_wait * bus_id
print(part1)

buses = [int(i) if i != 'x' else 0 for i in x[1].split(',')]
buses = [(b, b - i) for i, b in enumerate(buses) if b != 0]
bus_ids, bus_offsets = zip(*buses)
part2 = chinese_remainder(bus_ids, bus_offsets)

print(part2)

# Easier to understand CRT solution
# We are looking for the following relation to be satisfied:
# ex t st t + v % ids[k] == 0 for each k, v
n = 0
product_running = 1
for bus_id, offset in buses:

    offset = bus_id - offset
    c = 0
    while (n + offset) % bus_id != 0:
        n += product_running
        c += 1

    product_running *= bus_id
    prev_n = n - c * (product_running // bus_id)
    str1 = f"({prev_n} + {c} * {product_running // bus_id}) = "
    print(f"{str1:>50}"
          f"{n:>20} + {offset:>3} % {bus_id:>3} == 0 ")

print(f't = {n}')
