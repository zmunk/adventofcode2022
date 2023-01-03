import os
from utils import get_input

os.environ['SAMPLE'] = """
    30373
    25512
    65332
    33549
    35390
    """

def check(grid, coords, dirs, get_view=False):
    i, j = coords
    val = grid[i][j]
    i, j = (i + dirs[0], j + dirs[1])
    view = 0
    while 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        view += 1
        if grid[i][j] >= val:
            if get_view:
                break
            return False
        i, j = (i + dirs[0], j + dirs[1])
    if get_view:
        return view
    return True

def check_up(grid, coords, get_view=False):
    return check(grid, coords, (-1, 0), get_view)

def check_left(grid, coords, get_view=False):
    return check(grid, coords, (0, -1), get_view)

def check_down(grid, coords, get_view=False):
    return check(grid, coords, (1, 0), get_view)

def check_right(grid, coords, get_view=False):
    return check(grid, coords, (0, 1), get_view)

def check_all(grid, coords):
    for func in [check_up, check_left, check_down, check_right]:
        if func(grid, coords):
            return True
    return False

cyan =    lambda s: f'\033[1;36m{s}\033[0m'

def display(grid, highlight=set()):
    res = ""
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if (i, j) in highlight:
                res += cyan(v)
            else:
                res += str(v)
        res += "\n"
    print(res.strip())

def part1(grid):
    good = set()
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            if check_all(grid, (i, j)):
                good.add((i, j))
    # display(grid, good)
    print(len(good))

def get_score(grid, coords):
    score = 1
    for dir_func in [check_up, check_left, check_down, check_right]:
        score *= dir_func(grid, coords, True)
    return score

def part2(grid):
    max_score = 0
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            score = get_score(grid, (i, j))
            max_score = max(score, max_score)
    print(max_score)

if __name__ == "__main__":
    grid = [[int(x) for x in row] for row in get_input("input8.txt")]
    part1(grid)
    print("-"*10)
    part2(grid)
