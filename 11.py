import re
import os
import time
import builtins
from math import lcm
from collections import deque
from utils import get_input

os.environ['SAMPLE'] = """
    Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

    Monkey 1:
    Starting items: 54, 65, 75, 74
    Operation: new = old + 6
    Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0

    Monkey 2:
    Starting items: 79, 60, 97
    Operation: new = old * old
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3

    Monkey 3:
    Starting items: 74
    Operation: new = old + 3
    Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1
    """

def no_print(*args, **kwargs):
    pass

def split_list(arr, delim):
    res = []
    grp = []
    for val in arr:
        if val == delim:
            res.append(grp)
            grp = []
        else:
            grp.append(val)
    res.append(grp)
    return res

def create_operation(op, val, div):
    if op == "*":
        op = lambda a, b: a * b
    elif op == "+":
        op = lambda a, b: a + b
    else:
        raise ValueError()

    operator = lambda a, b: op(a, b) // div

    def operation(old):
        if val == "old":
            res = operator(old, old)
        else:
            res = operator(old, int(val))
        if BASE != -1:
            res = res % BASE
        return res

    return operation

starting_items_regex = re.compile(r'(\d+)')
operation_regex      = re.compile(r'.*old (.) (old|\d+)')
test_value_regex     = re.compile(r'.*by (\d+)')
on_true_regex        = re.compile(r'.*monkey (\d+)')
on_false_regex       = re.compile(r'.*monkey (\d+)')

def create_monkeys(inp, divisor=1):
    monkeys = []
    for details in split_list(inp, ""):
        monkeys.append([
            deque(int(x) for x in starting_items_regex.findall(details[1])),
            create_operation(*operation_regex.match(details[2]).groups(), divisor),
            int(test_value_regex.match(details[3]).groups()[0]),
            int(on_true_regex.match(details[4]).groups()[0]),
            int(on_false_regex.match(details[5]).groups()[0]),
        ])
    return monkeys

def get_monkey_business(inspection_counts):
    a, b = sorted(inspection_counts, reverse=True)[:2]
    return a * b

def part1(inp):
    global BASE

    monkeys = create_monkeys(inp, divisor=3)
    BASE = -1
    inspection_counts = perform_rounds(20, monkeys)
    return get_monkey_business(inspection_counts)

def perform_rounds(n_rounds, monkeys):
    inspection_counts = [0] * len(monkeys)
    t = time.time()
    for round_num in range(n_rounds):
        for i, (items, operation, val, on_true, on_false) in enumerate(monkeys):
            inspection_counts[i] += len(items)
            while items:
                item = operation(items.popleft())
                next_monkey = on_true if item % val == 0 else on_false
                monkeys[next_monkey][0].append(item)
    return inspection_counts

def part2(inp, verbose=True):
    global BASE

    monkeys = create_monkeys(inp)
    BASE = lcm(*(m[2] for m in monkeys))
    inspection_counts = perform_rounds(10_000, monkeys)
    return get_monkey_business(inspection_counts)

red = lambda s: f'\033[1;31m{s}\033[0m'
green = lambda s: f'\033[1;32m{s}\033[0m'

def check(actual, expected):
    if actual != expected:
        print(red(f"{actual}") + f" != {expected}")
    else:
        print(green(f"{actual}"))

if __name__ == "__main__":
    check(part1(get_input('input11.txt')), 58786)
    print("-"*10)
    inp = get_input('input11.txt')
    check(part2(get_input('input11.txt')), 14952185856)
