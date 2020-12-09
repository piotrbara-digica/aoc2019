from pathlib import Path

inp = Path('input.txt').read_text()


def run(program):
    done_ops = set()
    acc = 0
    pc = 0

    while pc not in done_ops:
        op, arg = program[pc]
        done_ops.add(pc)

        if op == 'acc':
            acc += arg
            pc += 1
        elif op == 'jmp':
            pc += arg
        else:  # NOP
            pc += 1

        if len(program) - 1 in done_ops:
            return True, acc

    return False, acc


def part1(code: str):
    code = [x.strip().split() for x in code.splitlines()]
    code = [(op, int(arg)) for op, arg in code]
    _, acc = run(code)
    print(acc)


def part2(code: str):
    code = [x.strip().split() for x in code.splitlines()]
    code = [(op, int(arg)) for op, arg in code]

    for i, (op, arg) in enumerate(code):
        c = code[:]
        if op == 'jmp':
            c[i] = 'nop', arg
        if op == 'nop':
            c[i] = 'jmp', arg

        term, res = run(c)
        if term:
            print(res)
            break


part1(inp)
part2(inp)
