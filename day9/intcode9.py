import sys
from itertools import count

import numpy as np
from tqdm import tqdm

POSITION, IMMEDIATE, RELATIVE = 0, 1, 2
HALT = 99


class Computer:

    def __init__(self, code, debug=False):
        self.program_counter = 0
        self.program = np.zeros(10_000_000, np.int64)
        self.program[:len(code)] = np.array(code, np.int64)
        self.debug_msg = debug
        self.input_code = float('inf')
        self.output_code = float('inf')
        self.relative_base = 0

    def get_value(self, param, p_mode, p_type):

        if p_type == self.READ:
            if p_mode == IMMEDIATE:
                value = param
            elif p_mode == POSITION:
                value = self.program[param]
            elif p_mode == RELATIVE:
                value = self.program[self.relative_base + param]
            else:
                raise ValueError(f'wrong parameter mode: {p_mode}')
        elif p_type == self.WRITE:
            if p_mode == POSITION:
                value = param
            elif p_mode == RELATIVE:
                value = self.relative_base + param
            else:
                raise ValueError(f'wrong parameter mode: {p_mode}')
        else:
            raise ValueError(f'wrong parameter type {p_type}')
        return value

    def add(self, a, b, dst):
        self.program[dst] = a + b

    def multiply(self, a, b, dst):
        self.program[dst] = a * b

    def store(self, dst):
        self.input_code = int(input('type a command...'))
        self.program[dst] = self.input_code

    def display(self, a):
        self.output_code = a
        print(self.output_code)

    def jump_non_zero(self, a, b):
        if a != 0:
            self.program_counter = b

    def jump_zero(self, a, b):
        if a == 0:
            self.program_counter = b

    def less_than(self, a, b, c):
        self.program[c] = 1 if a < b else 0

    def equals(self, a, b, c):
        self.program[c] = 1 if a == b else 0

    def change_relative_base(self, a):
        self.relative_base += a

    READ, WRITE = 0, 1
    OPCODE_TABLE = {
        # opcode: (func_handle, kind_of_param)
        1: (add, READ, READ, WRITE),
        2: (multiply, READ, READ, WRITE),
        3: (store, WRITE),
        4: (display, READ),
        5: (jump_non_zero, READ, READ),
        6: (jump_zero, READ, READ),
        7: (less_than, READ, READ, WRITE),
        8: (equals, READ, READ, WRITE),
        9: (change_relative_base, READ),
    }

    def parse_instruction(self, address):
        instruction = self.program[address]
        param_modes, opcode = divmod(instruction, 100)

        if opcode == HALT:
            return opcode, None

        func, *arg_types = self.OPCODE_TABLE[opcode]
        n_params = len(arg_types)
        param_modes = format(param_modes, '0>' + str(n_params))
        param_modes = [int(x) for x in reversed(param_modes)]

        parameters = [self.program[self.program_counter + i + 1] for i in range(n_params)]
        parameters = [self.get_value(p, m, t) for p, m, t in zip(parameters, param_modes, arg_types)]

        return func, parameters

    def run(self):
        while True:
            operation, parameters = self.parse_instruction(self.program_counter)
            if operation == HALT:
                return
            self.debug(f'{operation.__name__:<15} params:{parameters} base:{self.relative_base}')
            self.program_counter += len(parameters) + 1
            # if operation == Computer.store:
            #     self.input_code = yield
            operation(self, *parameters)
            # if operation == Computer.display:
            #     yield self.output_code

    def debug(self, *args):
        if self.debug_msg:
            print(*args, file=sys.stderr)
