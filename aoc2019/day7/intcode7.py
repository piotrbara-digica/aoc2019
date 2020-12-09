import sys
from typing import List

POSITION, IMMEDIATE = 0, 1
HALT = 99


class Computer:

    def __init__(self, code, debug=False):
        self.program_counter = 0
        self.program: List[int] = code.copy()
        self.debug_msg = debug
        self.code = float('inf')
        self.out_code = float('inf')
        self.relative_base = 0

    def get_value(self, param, mode):
        if mode == POSITION:
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
        # code = int(input.txt('type a command...'))
        self.program[dst] = self.code

    def display(self, a, mode_a):
        self.out_code = self.get_value(a, mode_a)
        self.debug(self.out_code)

    def jump_non_zero(self, a, b, mode_a, mode_b):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        if a != 0:
            self.program_counter = b

    def jump_zero(self, a, b, mode_a, mode_b):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        if a == 0:
            self.program_counter = b

    def less_than(self, a, b, c, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        self.program[c] = 1 if a < b else 0

    def equals(self, a, b, c, mode_a, mode_b, _):
        a = self.get_value(a, mode_a)
        b = self.get_value(b, mode_b)

        self.program[c] = 1 if a == b else 0

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

        if opcode == HALT:
            return opcode, None

        n_params, func = self.OPCODES[opcode]
        param_modes = format(param_modes, '0>' + str(n_params))
        param_modes = [int(x) for x in reversed(param_modes)]

        return func, param_modes

    def debug(self, *args):
        if self.debug_msg:
            print(*args, file=sys.stderr)

    def run(self):

        # while self.program_counter <= len(self.program):
        while True:
            operation, param_modes = self.parse_instruction(self.program_counter)
            if operation == HALT:
                return

            parameters = [self.program[self.program_counter + i + 1] for i, _ in enumerate(param_modes)]
            self.debug(f'{operation.__name__:<15}{parameters}')

            self.program_counter += len(parameters) + 1
            if operation == Computer.store:
                self.code = yield
            operation(self, *parameters, *param_modes)
            if operation == Computer.display:
                yield self.out_code
