import os
import re
from utils import get_input

os.environ['SAMPLE'] = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

regex = re.compile(r'(\d+),(\d+)')

def process(inp):
    res = []
    for line in inp:
        res.append([(int(x[0]), int(x[1])) for x in regex.findall(line)])
    return res

def get_inc(a, b):
    if a[0] == b[0]:
        if a[1] > b[1]:
            return (0, -1)
        return (0, 1)
    if a[0] > b[0]:
        return (-1, 0)
    return (1, 0)

def add(a, diff):
    return a[0] + diff[0], a[1] + diff[1]

def display(rocks, src, sand: set[tuple[int, int]], min_x, max_x, min_y, max_y):
    res = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in sand:
                res += "o"
            elif (x, y) == src:
                res += "+"
            elif (x, y) in rocks:
                res += "#"
            else:
                res += "."
        res += "\n"
    print(res[:-1])

def new_grain(rocks, sand, src, max_y, version=1):
    pos = src

    def check(pos):
        if version == 2 and pos[1] > max_y:
            return False
        return pos not in rocks | sand

    if version == 2 and not check(src):
        return None

    while True:
        for diff in [(0, 1), (-1, 1), (1, 1)]:
            if check(new_pos := add(pos, diff)):
                pos = new_pos
                break
        else:
            break
        if version == 1 and pos[1] > max_y:
            return None

    return pos

def update_bounds(x, y):
    global min_x, min_y, max_x, max_y

    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)

def get_rocks(inp):
    global min_x, min_y, max_x, max_y

    rocks = set()
    min_x, max_x = float('inf'), 0
    min_y, max_y = float('inf'), 0

    def add_rock(rock):
        update_bounds(*rock)
        rocks.add(rock)

    for line in inp:
        a = line[0]
        for b in line[1:]:
            inc = get_inc(a, b)
            add_rock(a)
            while a != b:
                a = add(a, inc)
                add_rock(a)
            a = b
    return rocks

def part1(inp):
    rocks = get_rocks(inp)
    src = (500, 0)
    update_bounds(*src)
    sand = set()
    while (grain := new_grain(rocks, sand, src, max_y)):
        sand.add(grain)
        # display(rocks, src, sand, min_x, max_x, min_y, max_y)
    return len(sand)

def part2(inp):
    global max_y

    rocks = get_rocks(inp)
    src = (500, 0)
    update_bounds(*src)
    max_y += 1
    sand = set()
    w = 1
    acc = 0
    for j in range(src[1], max_y + 1):
        for i in range(src[0] - w + 1, src[0] + w):
            p = (i, j)
            if p in rocks:
                if add(p, (-1, 0)) in rocks and add(p, (1, 0)) in rocks:
                    rocks.add(add(p, (0, 1)))
            else:
                sand.add(p)
                acc += 1
        w += 1
    sand.remove(src)
    display(rocks, src, sand, min_x - 20, max_x + 20, min_y, max_y)
    print(acc)

if __name__ == "__main__":
    sample = process(get_input())
    inp = process(get_input('input14.txt'))
    # assert part1(sample) == 24
    # assert part1(inp) == 745
    print("-"*10)
    part2(sample)
    part2(inp)
