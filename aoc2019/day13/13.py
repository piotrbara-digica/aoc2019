from pathlib import Path

import numpy as np

from aoc2019 import intcode_final

PADDLE, BALL = 3, 4
tiles = {0: ' ', 1: '█', 2: '▒', PADDLE: '▬', BALL: '◯', }

code = Path('input.txt').read_text()
code = [int(c) for c in code.strip().split(',')]

computer = intcode_final.Computer(code, debug=False)
program = computer.run()
screen = np.zeros((25, 40), int)
for x in program:
    y, tile = next(program), next(program)
    screen[y, x] = tile


def draw():
    board_str = ''
    for row in screen:
        board_str += ''.join(tiles[c] for c in row) + '\n'
    print(board_str)


draw()

print('Part 2\n')
computer = intcode_final.Computer(code, debug=False)
computer.program[0] = 2  # play the game for free
program = computer.run()
screen = np.zeros((24, 40), int)
ball_pos = paddle_pos = score = -1


def get_input(method: str):
    if method == 'human':
        key_pressed = input('give input')
        inp = {'a': -1, 's': 0, 'd': 1}.get(key_pressed)
    elif method == 'computer':
        if ball_pos > paddle_pos:
            inp = +1
        elif ball_pos < paddle_pos:
            inp = -1
        else:
            inp = 0
    else:
        raise ValueError('invalid method')

    return inp


for x in program:
    if x is None:  # wait for input
        # time.sleep(0.10)
        draw()
        # print(f'SCORE: {score}')
        game_input = get_input('computer')
        x = program.send(game_input)  # yields next value after receiving input

    if x == -1:  # score instruction
        next(program)
        score = next(program)
    else:  # update board
        y = next(program)
        tile = next(program)
        assert tile in tiles, f'{tile} is not a valid tile code'
        screen[y, x] = tile

        if tile == BALL:
            ball_pos = x
        elif tile == PADDLE:
            paddle_pos = x

print(f'SCORE: {score}')
print('game over!')
