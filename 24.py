import os
import time
from collections import defaultdict
from utils import get_input

os.environ['SAMPLE'] = """
    #.#####
    #...v.#
    #..>..#
    #.....#
    #.....#
    #.....#
    #####.#
    """

os.environ['SAMPLE'] = """
    #.######
    #>>.<^<#
    #.<..<<#
    #>v.><>#
    #<^v^^>#
    ######.#
    """

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def process(inp):
    size = (len(inp[0]) - 2, len(inp) - 2)
    blizzards = defaultdict(list)
    for j, line in enumerate(inp):
        for i, c in enumerate(line):
            if c in ['>', '<', 'v', '^']:
                blizzards[(i - 1, j - 1)].append(c)
    return blizzards, size

red = lambda s: f'\033[1;31m{s}\033[0m'

def render(blizzards, size, player=set()):
    res = "#." + "#" * size[0] + "\n"
    for j in range(size[1]):
        res += "#"
        for i in range(size[0]):
            if (b := (i, j)) in player:
                res += red("*")
            elif b in blizzards:
                if len(bb := blizzards[b]) == 1:
                    res += bb[0]
                elif (l := len(bb)) > 9:
                    res += "X"
                else:
                    res += str(l)
            else:
                res += "."
        res += "#\n"
    res += "#" * size[0] + ".#"
    print(res)

def reset_if_out_of_bounds(pos, size):
    if pos[0] < 0:
        return (size[0] - 1, pos[1])
    if pos[0] >= size[0]:
        return (0, pos[1])
    if pos[1] < 0:
        return (pos[0], size[1] - 1)
    if pos[1] >= size[1]:
        return (pos[0], 0)
    return pos

def step(blizzards, size):
    new = defaultdict(list)
    for pos, elems in blizzards.items():
        for el in elems:
            if el == '>':
                new_pos = add(pos, (1, 0))
            elif el == '<':
                new_pos = add(pos, (-1, 0))
            elif el == 'v':
                new_pos = add(pos, (0, 1))
            elif el == '^':
                new_pos = add(pos, (0, -1))
            else:
                raise ValueError()
            new_pos = reset_if_out_of_bounds(new_pos, size)
            new[new_pos].append(el)
    return new

def get_next_possible_locations(blizzards, size, loc, special_cases=set()) -> set[tuple[int, int]]:
    locations = set()
    for direction in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
        candidate = add(loc, direction)
        # if candidate == (0, 0) or \
        if candidate in special_cases or\
                0 <= candidate[0] < size[0] and 0 <= candidate[1] < size[1] and\
                candidate not in blizzards:
            locations.add(candidate)
    return locations

def time_to_goal(start, goal, blizzards, size, verbose=0):
    possible_locations = {start}
    special_cases = {start, goal}
    i = 0
    while goal not in possible_locations:
        blizzards = step(blizzards, size)
        next_possible_locations = set()
        for loc in possible_locations:
            next_possible_locations |= get_next_possible_locations(
                blizzards, size, loc, special_cases)
        possible_locations = next_possible_locations
        if verbose > 0:
            render(blizzards, size, possible_locations)
        i += 1
    return i, blizzards

def part1(inp):
    blizzards, size = process(inp)
    render(blizzards, size)
    goal = add(size, (-1, -1))
    t, _ = time_to_goal((0, -1), goal, blizzards, size)
    print(f"{t = }")

def part2(inp):
    blizzards, size = process(inp)
    render(blizzards, size)
    start = (0, -1)
    end = add(size, (-1, 0))

    acc = 0

    t, blizzards = time_to_goal(start, end, blizzards, size)
    acc += t
    print(f"{t = }")
    render(blizzards, size)

    t, blizzards = time_to_goal(end, start, blizzards, size)
    acc += t
    print(f"{t = }")
    render(blizzards, size)

    t, blizzards = time_to_goal(start, end, blizzards, size)
    acc += t
    print(f"{t = }")
    render(blizzards, size)

    print(f"{acc = }")

if __name__ == "__main__":
    inp = get_input()
    inp = get_input('input24.txt')
    # part1(inp)
    print("-"*10)
    part2(inp)
