import sys
from functools import partial
from pathlib import Path

from tqdm import tqdm

from .intcode7 import Computer
import itertools

debug = partial(print, file=sys.stderr)
code = [int(d) for d in Path('input7.txt').read_text().split(',')]


def test_settings(settings_list):
    for phase_setting in tqdm(settings_list):
        output_code = -1
        input_code = 0

        for phase in phase_setting:
            comp = Computer(code)
            program = comp.run()
            next(program)
            program.send(phase)
            output_code = program.send(input_code)
            input_code = output_code

        yield output_code, phase_setting


print(
    max(test_settings(itertools.permutations(range(5))), key=lambda x: x[0])
)


def test_settings_feedback(settings_list):
    for phase_setting in tqdm(settings_list):
        computers = [Computer(code) for _ in range(5)]
        out_signal = -1
        in_signal = 0

        programs = []
        # initialization, phase + 1st input.txt
        for comp, phase in zip(computers, phase_setting):
            program = comp.run()

            next(program)
            program.send(phase)
            out_signal = program.send(in_signal)
            in_signal = out_signal

            programs.append(program)

        i = 5
        for program in itertools.cycle(programs):
            try:
                next(program)
                out_signal = program.send(in_signal)
                in_signal = out_signal
            except StopIteration:
                break
            i += 1

        # print(out_signal, phase_setting)
        yield out_signal, phase_setting, i


print(
    max(test_settings_feedback(itertools.permutations(range(5, 10))), key=lambda x: x[0])
)
print('done')
