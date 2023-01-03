import os
from itertools import zip_longest
from functools import cmp_to_key
from utils import get_input

os.environ['SAMPLE'] = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def compare(a, b):
    """
    -1 if a < b
    0 if a == b
    1 if a > b
    """
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)

    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])

    if isinstance(a, list) and isinstance(b, list):
        for aa, bb in zip_longest(a, b):
            if aa is None:
                return -1
            if bb is None:
                return 1
            if (cmp := compare(aa, bb)) == 0:
                continue
            return cmp
        return 0

def part1(inp):
    inp = iter(inp)
    acc = 0
    i = 1
    while True:
        a = eval(next(inp))
        b = eval(next(inp))
        if compare(a, b) == -1:
            acc += i
        try:
            next(inp)
        except StopIteration:
            break
        i += 1
    print(acc)


def part2(inp):
    dividers = [[[2]], [[6]]]
    lists = [eval(x) for x in inp if x != ""] + dividers
    res = 1
    for v in dividers:
        srt = sorted(lists, key=cmp_to_key(compare))
        res *= srt.index(v) + 1
    return res

if __name__ == "__main__":
    inp = get_input('input13.txt')
    part1(inp)
    print("-"*10)
    # inp = get_input()
    inp = get_input('input13.txt')
    print(part2(inp))
