import sys
from typing import List


class Computer:
    POSITION, IMMEDIATE = 0, 1

    def __init__(self, code):
        self.program_counter = 0
        self.program: List[int] = code.copy()

    def get_value(self, param, mode):
        if mode == self.POSITION:
            param = self.program[param]
        return param

    def add(self, a, b, dst, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)
        self.program[dst] = a + b

    def multiply(self, a, b, dst, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)
        self.program[dst] = a * b

    def store(self, dst, _):
        code = int(input('type a command...'))
        self.program[dst] = code

    def display(self, a, mode_a):
        a = self.get_value(a, mode_a)
        print(a)

    def jump_non_zero(self, a, b, mode_a, mode_b):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        if a != 0:
            self.program_counter = b
        else:
            self.program_counter += 3

    def jump_zero(self, a, b, mode_a, mode_b):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        if a == 0:
            self.program_counter = b
        else:
            self.program_counter += 3

    def less_than(self, a, b, c, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        self.program[c] = 1 if a < b else 0

    def equals(self, a, b, c, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        self.program[c] = 1 if a == b else 0

    def halt(self):
        print(f'Halting at PC={self.program_counter}')
        sys.exit()

    OPCODES = {
        1: (3, add),
        2: (3, multiply),
        3: (1, store),
        4: (1, display),
        5: (2, jump_non_zero),
        6: (2, jump_zero),
        7: (3, less_than),
        8: (3, equals),
    }

    def parse_instruction(self, address):
        instruction = self.program[address]
        param_modes, opcode = divmod(instruction, 100)

        if opcode == 99:
            self.halt()

        n_params, func = self.OPCODES[opcode]
        param_modes = format(param_modes, '0>' + str(n_params))
        param_modes = [int(x) for x in reversed(param_modes)]

        return func, param_modes

    def run_program(self):

        executed = 0
        while self.program_counter <= len(self.program):
            operation, param_modes = self.parse_instruction(self.program_counter)
            parameters = [self.program[self.program_counter + i + 1] for i, _ in enumerate(param_modes)]
            print(f'{operation.__name__:<15}{parameters}', file=sys.stderr)
            operation(self, *parameters, *param_modes)

            if 'jump' not in operation.__name__:
                self.program_counter += len(parameters) + 1

            executed += 1
            if executed > len(self.program):
                print('infinite loop!')
                break
