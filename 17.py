import os
from string import ascii_lowercase as asc
from collections import defaultdict
from itertools import cycle, count
from utils import get_input

os.environ['SAMPLE'] = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

def render(shapes, at_rest, y_range):
    shapes = set().union(*shapes)
    highest_y = get_highest_y(shapes | at_rest)
    res = ""
    p = 5
    pre = " " * p
    for y in range(y_range[1], y_range[0] - 1, -1):
        res += f"{y:<{p-1}} |"
        for x in range(7):
            if (x, y) in shapes:
                res += f"@"
            elif (x, y) in at_rest:
                res += f"#"
            else:
                res += "."
        res += "|\n"
    res += f"{pre}+-------+"
    return res

def shift(block, diff):
    return (block[0] + diff[0], block[1] + diff[1])

def shift_shape(shape, diff):
    return {shift(block, diff) for block in shape}

def check(shape, at_rest):
    for block in shape:
        if block[1] < 0:
            return False
        if block[0] < 0:
            return False
        if block[0] > 6:
            return False
        if block in at_rest:
            return False
    return True

def move_shape(shape, diff, at_rest):
    new_shape = set()
    for block in shape:
        new_shape.add(shift(block, diff))
    if check(new_shape, at_rest):
        return new_shape
    return False

move_down = lambda shape, at_rest: move_shape(shape, (0, -1), at_rest)
move_right = lambda shape, at_rest: move_shape(shape, (1, 0), at_rest)
move_left = lambda shape, at_rest: move_shape(shape, (-1, 0), at_rest)

def printm(move):
    n = 20
    if move == move_right:
        print(">"*n)
    elif move == move_down:
        print("v"*n)

flat_shape = {(2, 3), (3, 3), (4, 3), (5, 3)}
plus_shape = {(3, 5), (2, 4), (3, 4), (4, 4), (3, 3)}
l_shape = {(2, 3), (3, 3), (4, 3), (4, 4), (4, 5)}
pillar_shape = {(2, 3), (2, 4), (2, 5), (2, 6)}
block_shape = {(2, 3), (3, 3), (2, 4), (3, 4)}

def get_highest_y(shape):
    return max(b[1] for b in shape)

def part1(moves):
    shapes = []
    at_rest = set()
    moves = cycle(moves)
    highest_y = -1
    to_add = cycle([flat_shape, plus_shape, l_shape, pillar_shape, block_shape])
    for _ in range(2022):
        shape = shift_shape(next(to_add), (0, highest_y + 1))
        shapes.append(shape)
        while True:
            move = next(moves)
            res = move(shapes[-1], at_rest)
            if res:
                shapes[-1] = res
            elif move == move_down:
                shape = shapes.pop()
                at_rest |= shape
                highest_y = max(highest_y, get_highest_y(shape))
                break
    print(highest_y + 1)

def process(inp):
    moves = []
    for c in inp:
        if c == '>':
            moves.append((move_right, 1))
        elif c == '<':
            moves.append((move_left, -1))
        else:
            raise ValueError()
        moves.append((move_down, 0))
    return moves

def part2(moves):
    placements = placement_generator(moves)
    history = []
    y_history = []
    seen_indices = defaultdict(list)
    found = False
    for i in count():
        plc, y = next(placements)
        for s1 in seen_indices[plc][::-1]:
            cycle_len = i - s1
            s0 = s1 - cycle_len
            if s0 < 0:
                continue
            if history[s0:s1] != history[s1:i]:
                continue
            found = True
            break
        seen_indices[plc].append(i)
        history.append(plc)
        y_history.append(y)
        if found:
            break

    segment = y_history[s0:s1]
    y_start = y_history[s0 - 1]
    y_diff = y_history[s1 - 1] - y_start

    print(f"found cycle starting at {s0} (previous height {y_start}) "
          f"of length {cycle_len} height diff {y_diff}")
    n = int(1e12)
    n_cycles = (n - s0) // cycle_len
    rem = (n - s0) % cycle_len
    if rem == 0:
        remainder = 0
    else:
        remainder = segment[rem - 1] - y_start
    y_total = y_start + (n_cycles * y_diff) + remainder
    print(f"{y_total = }")

def placement_generator(moves):
    shapes = []
    at_rest = set()
    moves = cycle(moves)
    highest_y = -1
    to_add = cycle([
        ('-', flat_shape),
        ('+', plus_shape),
        ('L', l_shape),
        ('|', pillar_shape),
        ('#', block_shape),
    ])
    while True:
        name, original_shape = next(to_add)
        shape = shift_shape(original_shape, (0, highest_y + 1))
        x = 0
        shapes.append(shape)
        while True:
            move, x_diff = next(moves)
            res = move(shapes[-1], at_rest)
            if res:
                shapes[-1] = res
                x += x_diff
            elif move == move_down:
                shape = shapes.pop()
                at_rest |= shape
                highest_y = max(highest_y, get_highest_y(shape))
                break
        yield (name, x), highest_y + 1

if __name__ == "__main__":
    # inp = get_input()[0]
    inp = get_input('input17.txt')[0]
    moves = process(inp)
    # part1(moves)
    print("-"*10)
    part2(moves) # y_total = 1560932944615
