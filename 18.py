import os
import re
from utils import get_input

os.environ['SAMPLE'] = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

regex = re.compile(r"(\d+),(\d+),(\d+)")

def process(inp):
    res = set()
    for line in inp:
        res.add(tuple(int(x) for x in regex.match(line).groups()))
    return res

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

directions = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
]

def part1(cubes):
    print(get_surface_area(cubes))

def get_surface_area(cubes):
    acc = 0
    for cube in surrounding(cubes):
        if cube not in cubes:
            acc += 1
    return acc

def get_bounds(cubes):
    x_bounds = (float('inf'), float('-inf')) # min, max
    y_bounds = (float('inf'), float('-inf')) # min, max
    z_bounds = (float('inf'), float('-inf')) # min, max
    for x, y, z in cubes:
        x_bounds = (min(x_bounds[0], x), max(x_bounds[1], x))
        y_bounds = (min(y_bounds[0], y), max(y_bounds[1], y))
        z_bounds = (min(z_bounds[0], z), max(z_bounds[1], z))
    return x_bounds, y_bounds, z_bounds

def is_outside(cube, bounds):
    x, y, z = cube
    (x0, x1), (y0, y1), (z0, z1) = bounds
    if not (x0 <= x <= x1) or not (y0 <= y <= y1) or not (z0 <= z <= z1):
        return True
    return False

def surrounding_cube(cube):
    for d in directions:
        yield add(cube, d)

def surrounding(arg):
    if isinstance(arg, set):
        cubes = arg
        for cube in cubes:
            yield from surrounding_cube(cube)
    elif isinstance(arg, tuple):
        cube = arg
        yield from surrounding_cube(cube)

def part2(cubes):
    bounds = get_bounds(cubes)
    outside = set()
    unknown = set()
    for cube in surrounding(cubes):
        if cube in cubes:
            continue
        if is_outside(cube, bounds):
            outside.add(cube)
        else:
            unknown.add(cube)

    to_add = set()
    for cube in surrounding(unknown):
        if cube in cubes:
            continue
        if cube in outside:
            continue
        if cube in unknown:
            continue
        if is_outside(cube, bounds):
            outside.add(cube)
            continue
        to_add.add(cube)
    unknown |= to_add

    n_unknown = -1
    while n_unknown != len(unknown):
        n_unknown = len(unknown)

        to_move = set()
        for cube in unknown:
            for p in surrounding(cube):
                if p in outside:
                    to_move.add(cube)
                    break

        unknown -= to_move
        outside |= to_move

    while True:
        to_add = set()
        existing = unknown | cubes
        for cube in surrounding(unknown):
            if cube not in existing:
                if is_outside(cube, bounds):
                    raise ValueError()
                to_add.add(cube)
        if len(to_add) == 0:
            break
        unknown |= to_add

    pocket_sa = get_surface_area(unknown)
    sa = get_surface_area(cubes)
    print(sa - pocket_sa)

if __name__ == "__main__":
    inp = get_input()
    inp = get_input('input18.txt')
    inp = process(inp)
    part1(inp)
    print("-"*10)
    part2(inp)
