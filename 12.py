import os
from itertools import zip_longest, cycle
from collections import deque
from utils import get_input

os.environ['SAMPLE'] = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

cyan = lambda s: f'\033[1;36m{s}\033[0m'

class Grid:
    def __init__(self, grid):
        self._grid = grid
        self.n_rows = len(self._grid)
        self.n_cols = len(self._grid[0])

    def __str__(self):
        res = ""
        for line in self._grid:
            for val in line:
                val = val or "."
                res += f"{val:^3}"
            res += "\n"
        return res[:-1]

    def print_simplified(self, highlight=(-1, -1), ret=False):

        # determine non-empty rows and columns
        rows: set[int] = set()
        cols: set[int] = set()
        for i, row in enumerate(self._grid):
            for j, el in enumerate(row):
                if el is not None:
                    rows.add(i)
                    cols.add(j)

        # render
        res = ""
        el_size = 3
        empty_row = False
        for i, row in enumerate(self._grid):

            if i not in rows:
                if not empty_row:
                    res += "\n"
                    empty_row = True
                continue
            empty_row = False

            empty_col = False
            for j, el in enumerate(row):

                if j in cols:
                    empty_col = False
                else:
                    if empty_col:
                        continue
                    empty_col = True
                    el = " "
                    continue

                el = el or " "
                el = f"{el:^{el_size}}"
                if (i, j) == highlight:
                    el = cyan(el)
                res += el
            res += "|\n"
        res = res[:-1] + "\n" + "-" * el_size * len(cols)
        if ret:
            return res
        print(res)

    def get_dimensions(self):
        return self.n_rows, self.n_cols

    def empty_clone(self, default_value=None):
        return Grid([[default_value] * self.n_cols for _ in range(self.n_rows)])

    def find(self, c):
        for i, row in enumerate(self._grid):
            for j, val in enumerate(row):
                if val == c:
                    return i, j

    def replace(self, old, new):
        i, j = self.find(old)
        self._grid[i][j] = new

    def get(self, i, j):
        return self._grid[i][j]

    def get_region(self, i, j, n_surr=1):
        rows = []
        for row in self._grid[max(0, i - 1): i + 2]:
            rows.append(row[max(0, j - 1): j + 2])
        return rows

    def set(self, i, j, new):
        self._grid[i][j] = new

def print_together(a, b):
    a = a.split("\n")
    b = b.split("\n")
    for aa, bb in zip_longest(a, b):
        aa = aa or " " * len(a[-1])
        bb = bb or ""
        print(aa + "  " + bb)

def print_region(height_map, i, j):
    for row in height_map.get_region(i, j, n_surr=1):
        print(" ".join(map(str, row)))

def get_neighbor(c, dir_):
    return chr(ord(c) + dir_)

def decrement(c):
    return chr(ord(c) - 1)

def find(height_map, letter):
    for i, row in enumerate(height_map):
        for j, val in enumerate(row):
            if val == letter:
                return i, j

def part1(inp):
    height_map = Grid([list(row) for row in inp])
    n_rows, n_cols = height_map.get_dimensions()

    si, sj = height_map.find('S')
    height_map.replace('S', 'a')
    ei, ej = height_map.find('E')
    height_map.replace('E', 'z')

    steps = {
        "fwd": height_map.empty_clone(),
        "back": height_map.empty_clone(),
    }

    steps["fwd"].set(si, sj, 0)
    steps["back"].set(ei, ej, 0)

    to_check = {"fwd": deque(), "back": deque()}
    to_check_set = {"fwd": set(), "back": set()}

    def add_to_check(i, j, direction):
        if (i, j) not in to_check_set[direction]:
            to_check[direction].append((i, j))
            to_check_set[direction].add((i, j))

    def get_to_check(direction):
            i, j = to_check[direction].popleft()
            to_check_set[direction].remove((i, j))
            return i, j

    add_to_check(si, sj, "fwd")
    add_to_check(ei, ej, "back")

    checked = {"fwd": set(), "back": set()}

    to_highlight = {"fwd": None, "back": None}

    def out_of_bounds(i, j):
        return i < 0 or j < 0 or i >= n_rows or j >= n_cols

    for direction in cycle(["fwd", "back"]):
        other_steps = steps["back" if direction == "fwd" else "fwd"]
        i, j = get_to_check(direction)
        checked[direction].add((i, j))
        step_val = steps[direction].get(i, j)

        height = height_map.get(i, j)
        diff = 1 if direction == "fwd" else -1
        elevation = chr(ord(height) + diff)

        def is_steppable(ii, jj):
            if direction == "fwd":
                return height_map.get(ii, jj) <= elevation
            else:
                return height_map.get(ii, jj) >= elevation

        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            ii, jj = i + dx, j + dy
            if (ii, jj) in checked[direction] \
                    or out_of_bounds(ii, jj) \
                    or not is_steppable(ii, jj):
                continue
            if (ex := steps[direction].get(ii, jj)) is None:
                ex = float('inf')
            v = min(ex, step_val + 1)
            if (o := other_steps.get(ii, jj)) is not None:
                return v + o
            steps[direction].set(ii, jj, v)
            add_to_check(ii, jj, direction)

        to_highlight[direction] = (i, j)

def part2(inp):
    height_map = Grid([list(row) for row in inp])
    n_rows, n_cols = height_map.get_dimensions()

    si, sj = height_map.find('S')
    height_map.replace('S', 'a')
    ei, ej = height_map.find('E')
    height_map.replace('E', 'z')

    steps = height_map.empty_clone()
    steps.set(ei, ej, 0)

    checked = set()
    to_check = deque()
    to_check_set = set()

    def add_to_check(i, j):
        if (i, j) not in to_check_set:
            to_check.append((i, j))
            to_check_set.add((i, j))

    def get_to_check():
        i, j = to_check.popleft()
        to_check_set.remove((i, j))
        return i, j

    add_to_check(ei, ej)

    def out_of_bounds(i, j):
        return i < 0 or j < 0 or i >= n_rows or j >= n_cols

    while True:
        i, j = get_to_check()
        checked.add((i, j))
        step_val = steps.get(i, j)
        height = height_map.get(i, j)
        if height == 'a':
            return step_val
        diff = -1
        elevation = chr(ord(height) + diff)

        def is_steppable(ii, jj):
            return height_map.get(ii, jj) >= elevation

        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            ii, jj = i + dx, j + dy
            if (ii, jj) in checked \
                    or out_of_bounds(ii, jj) \
                    or not is_steppable(ii, jj):
                continue
            if (ex := steps.get(ii, jj)) is None:
                ex = float('inf')
            v = min(ex, step_val + 1)
            steps.set(ii, jj, v)
            add_to_check(ii, jj)


if __name__ == "__main__":
    assert part1(get_input()) == 31
    assert part1(get_input('input12.txt')) == 520
    assert part2(get_input()) == 29
    assert part2(get_input('input12.txt')) == 508
