import os
from utils import get_input

os.environ['SAMPLE'] = """
        ...#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

def get_start(open_tiles):
    i = 0
    while (i, 0) not in open_tiles:
        i += 1
    return (i, 0)

def process_path(path) -> list[int | str]:
    res = []
    curr = ""
    for c in path:
        if c in ['R', 'L']:
            res.extend([int(curr), c])
            curr = ""
        else:
            curr += c
    res.append(int(curr))
    return res

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + -other

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def get_component(self, other):
        if other.x != 0:
            return Point(self.x * other.x, 0)
        if other.y != 0:
            return Point(0, self.y * other.y)

class Delta(Point):
    @classmethod
    def from_direction(cls, direction):
        if direction == "right":
            return cls(1, 0)
        if direction == "left":
            return cls(-1, 0)
        if direction == "up":
            return cls(0, -1)
        if direction == "down":
            return cls(0, 1)
        raise ValueError(f"invalid direction: {direction!r}")

    def __rmul__(self, other):
        return Delta(self.x * other, self.y * other)

    def rotate_cw(self):
        return Delta(-self.y, self.x)

    def rotate_ccw(self):
        return Delta(self.y, -self.x)

def out_of_bounds(pos, bounds):
    if pos.x < 0 or pos.y < 0:
        return True
    if pos.x >= bounds.x or pos.y >= bounds.y:
        return True
    return False

def calibrate(pos, d, bounds, cube=False):
    if cube:
        e = 4 if sample else 50
        nx = pos.x // e
        rx = pos.x % e
        ny = pos.y // e
        ry = pos.y % e

        if sample:

            if pos.x == 16 and 4 <= pos.y <= 7:
                return Point(19 - pos.y, 8), d.rotate_cw()

            if 8 <= pos.x < 12 and pos.y == 12:
                return Point(11 - pos.x, 7), Delta(0, -1)

            if 4 <= pos.x < 8 and pos.y == -1:
                return Point(8, pos.x - 4), Delta(1, 0)

        else:
            new = {
                (1, -1): (0, 3 * e + rx, 'right'),
                (1, 4): (e - 1, 3 * e + rx, 'left'),
                (3, 3): (e + ry, 3 * e - 1, 'up'),
                (0, -1): (e, e + rx, 'right'),
                (-1, 1): (ry, 2 * e, 'down'),
                (0, 4): (2 * e + rx, 0, 'down'),
                (3, 0): (2 * e - 1, 3 * e - 1 - ry, 'left'),
                (3, 1): (2 * e + ry, e - 1, 'up'),
                (2, 4): (2 * e - 1, e + rx, 'left'),
                (-1, 2): (e, e - 1 - ry, 'right'),
                (-1, 0): (0, 3 * e - 1 - ry, 'right'),
                (3, 2): (3 * e - 1, e - 1 - ry, 'left'),
                (2, -1): (rx, 4 * e - 1, 'up'),
                (-1, 3): (e + ry, 0, 'down'),
            }.get((nx, ny))

            if new is None:
                raise ValueError(f"{nx}, {ny}")

            x, y, direction = new

            return Point(x, y), Delta.from_direction(direction)

    else:
        if d.x > 0 or d.y > 0:
            return pos - pos.get_component(d), d
        else:
            return pos - bounds.get_component(d), d

def step(pos, d, tiles, bounds, cube=False):
    pos += d
    while pos not in tiles:
        if out_of_bounds(pos, bounds):
            pos, d = calibrate(pos, d, bounds, cube)
        else:
            pos += d
    return pos, d

def process(inp):
    bounds = Point(len(inp[0]), len(inp) - 2)
    open_tiles = set()
    walls = set()
    for j, line in enumerate(inp):
        if line == "":
            break
        for i, c in enumerate(line):
            if c == ".":
                open_tiles.add((i, j))
            elif c == "#":
                walls.add((i, j))
    path = process_path(inp[-1]) # [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]
    return open_tiles, walls, bounds, path

def get_facing(d):
    if d == (1, 0):
        return 0
    if d == (0, 1):
        return 1
    if d == (-1, 0):
        return 2
    if d == (0, -1):
        return 3

def render(open_tiles, walls, bounds, history):
    res = ""
    for j in range(bounds.y):
        for i in range(bounds.x):
            if (i, j) in history:
                res += history[(i, j)]
            elif (i, j) in open_tiles:
                res += "."
            elif (i, j) in walls:
                res += "#"
            else:
                res += " "
        res += "\n"
    print(res)

def get_symbol(d):
    if d == (1, 0):
        return ">"
    if d == (0, 1):
        return "v"
    if d == (-1, 0):
        return "<"
    if d == (0, -1):
        return "^"

def traverse(pos, d, path, open_tiles, walls, bounds, cube=False):
    history = {}
    for p in path:
        if isinstance(p, int):
            for _ in range(p):
                # print(f"{pos = }")
                try:
                    next_tile, next_d = step(pos, d, open_tiles | walls, bounds, cube)
                except ValueError:
                    import traceback; traceback.print_exc()
                    return pos, d, history
                if next_tile in walls:
                    break
                pos = next_tile
                d = next_d
                history[pos] = get_symbol(d)
        elif p == 'R':
            d = d.rotate_cw()
        elif p == 'L':
            d = d.rotate_ccw()
        else:
            raise ValueError()
        history[pos] = get_symbol(d)
    return pos, d, history

def part1(inp):
    open_tiles, walls, bounds, path = process(inp)
    start = get_start(open_tiles)

    pos = Point(*start)
    d = Delta(1, 0)

    pos, d, history = traverse(pos, d, path, open_tiles, walls, bounds)

    render(open_tiles, walls, bounds, history)
    facing = get_facing(d)
    print(1000 * (pos.y + 1) + 4 * (pos.x + 1) + facing)

def part2(inp):
    open_tiles, walls, bounds, path = process(inp)
    print(f"{bounds = }")
    start = get_start(open_tiles)

    pos = Point(*start)
    d = Delta(1, 0)

    pos, d, history = traverse(pos, d, path, open_tiles, walls, bounds, cube=True)
    # render(open_tiles, walls, bounds, history)
    facing = get_facing(d)
    print(1000 * (pos.y + 1) + 4 * (pos.x + 1) + facing)

if __name__ == "__main__":
    inp = get_input(); sample = True
    inp = get_input('input22.txt'); sample = False
    # part1(inp)
    print("-"*10)
    part2(inp)
