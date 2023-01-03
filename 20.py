import os
from copy import copy, deepcopy
from utils import get_input

os.environ['SAMPLE'] = """
1
2
-3
3
-2
0
4
"""

def process(inp):
    return list(map(int, inp))

class Node:
    def __init__(self, val, mod=None):
        self.actual_val = val
        if mod:
            self.val = val % mod
        else:
            self.val = val

def mix(inp, n=1):
    l = len(inp) - 1
    c = inp
    for _ in range(n):
        for v in inp:
            i = c.index(v)
            new_i = (i + v.val % l) % l
            if new_i == 0:
                new_i = len(c) - 1
            c = move(c, i, new_i)
    return c

def part1(inp):
    inp = [Node(x) for x in inp]
    c = mix(inp)
    print(f"{c = }")

    acc = 0
    # start = c.index(0)
    start = [x.val for x in c].index(0)
    for i in [1000, 2000, 3000]:
        ind = (start + i) % len(c)
        acc += c[ind].val
    print(f"{acc = }")

def move(arr, i, new_i):
    if new_i > i:
        arr = arr[:i] + arr[i + 1:new_i + 1] + [arr[i]] + arr[new_i + 1:]
    elif new_i < i:
        arr = arr[:new_i] + [arr[i]] + arr[new_i:i] + arr[i + 1:]
    return arr

dec = 811589153

def part2(inp):
    # inp = [Node((x * dec) % (len(inp) - 1)) for x in inp]
    inp = [Node(x * dec, len(inp) - 1) for x in inp]
    c = mix(inp, 10)
    print(f"{c = }")
    acc = 0
    # start = c.index(0)
    start = [x.val for x in c].index(0)
    for i in [1000, 2000, 3000]:
        ind = (start + i) % len(c)
        acc += c[ind].actual_val
    print(f"{acc = }")

if __name__ == "__main__":
    inp = process(get_input())
    inp = process(get_input('input20.txt'))
    part1(inp)
    print("-"*10)
    part2(inp)  # not 5516
