import os
from collections import defaultdict
from utils import get_input

# os.environ['SAMPLE'] = """
    # .....
    # ..##.
    # ..#..
    # .....
    # ..##.
    # .....
    # """

os.environ['SAMPLE'] = """
    ..............
    ..............
    .......#......
    .....###.#....
    ...#...#.#....
    ....#...##....
    ...#.###......
    ...##.#.##....
    ....#..#......
    ..............
    ..............
    ..............
    """

def render(elves, bounds):
    x, y = bounds
    res = ""
    for j in range(y):
        for i in range(x):
            if (i, j) in elves:
                res += "#"
            else:
                res += "."
        res += "\n"
    print(res)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def count_empty_ground(elves):
    x_bounds = [float('inf'), float('-inf')]
    y_bounds = [float('inf'), float('-inf')]
    for elf in elves:
        x_bounds[0] = min(x_bounds[0], elf[0])
        x_bounds[1] = max(x_bounds[1], elf[0])
        y_bounds[0] = min(y_bounds[0], elf[1])
        y_bounds[1] = max(y_bounds[1], elf[1])
    return (x_bounds[1] - x_bounds[0] + 1) * (y_bounds[1] - y_bounds[0] + 1) - len(elves)

def part1(inp):
    run(inp, n_rounds=10)

def run(inp, n_rounds=float('inf')):
    elves = set()
    for j, line in enumerate(inp):
        for i, c in enumerate(line):
            if c == "#":
                elves.add((i, j))

    bounds = (len(inp[0]), len(inp))
    # render(elves, bounds)

    n = (0, -1)
    s = (0, 1)
    w = (-1, 0)
    e = (1, 0)
    nw, ne = add(n, w), add(n, e)
    sw, se = add(s, w), add(s, e)
    all_directions = [nw, n, ne, e, se, s, sw, w]
    options = [
        (n, [nw, n, ne]),
        (s, [sw, s, se]),
        (w, [nw, w, sw]),
        (e, [ne, e, se]),
    ]
    i = 0
    while True:
        if i >= n_rounds:
            break
        new_locs = defaultdict(set)
        for elf in elves:
            for d in all_directions:
                if add(elf, d) in elves:
                    break
            else:
                continue # no elves around

            for direction, to_check in options:
                for d in to_check:
                    if add(elf, d) in elves:
                        break
                else:
                    new_locs[add(elf, direction)].add(elf)
                    break

        for loc, origins in new_locs.items():
            if len(origins) > 1:
                continue
            elves.remove(next(iter(origins)))
            elves.add(loc)

        if len(new_locs) == 0:
            break

        # render(elves, bounds)
        options += [options.pop(0)]

        i += 1
    print(i + 1)

    empty_ground = count_empty_ground(elves)
    print(f"{empty_ground = }")

def part2(inp):
    run(inp)

if __name__ == "__main__":
    inp = get_input()
    inp = get_input('input23.txt')
    part1(inp)
    print("-"*10)
    part2(inp)
