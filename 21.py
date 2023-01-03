import os
import re
from utils import get_input

os.environ['SAMPLE'] = """
    root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32
    """

regex = re.compile(r'(\w+): (?:(\w+) ([\+\-\*/]) (\w+)|(\d+))')

def create_nodes(inp):
    nodes = {}
    for line in inp:
        name, a, op, b, val = regex.match(line).groups()
        if val is not None:
            nodes[name] = int(val)
        else:
            nodes[name] = [a, op, b]
    return nodes

def part1(inp):
    nodes = create_nodes(inp)
    print(resolve(nodes, "root"))

def resolve(nodes, key):
    val = nodes[key]
    if isinstance(val, int):
        return val
    a = resolve(nodes, val[0])
    op = val[1]
    b = resolve(nodes, val[2])
    res = int(eval(f"{a} {val[1]} {b}"))
    nodes[key] = res
    return res

def find_human(nodes, key) -> set:
    val = nodes[key]
    if isinstance(val, int):
        return set()
    a, _, b = val
    if 'humn' in [a, b]:
        return {'humn', key}
    if len(s := find_human(nodes, a) | find_human(nodes, b)) > 0:
        s |= {key}
    return s

def part2(inp):
    nodes = create_nodes(inp)
    path_to_human = find_human(nodes, 'root')
    node = nodes['root']
    a, _, b = node
    if a in path_to_human:
        val = resolve(nodes, b)
        key = a
    else:
        val = resolve(nodes, a)
        key = b

    print(equate(nodes, key, val, path_to_human))

def equate(nodes, key, val, path_to_human):
    if key == 'humn':
        return int(val)

    a, op, b = nodes[key]
    invert = False
    if a in path_to_human:
        a_in_path = True
        key = a
        other = resolve(nodes, b)
    else:
        a_in_path = False
        key = b
        other = resolve(nodes, a)
        if op in ["-", "/"]:
            invert = True

    if invert:
        val, other = other, val
    else:
        op = {"+": "-", "-": "+", "*": "/", "/": "*"}[op]

    val = eval(f"{val} {op} {other}")
    return equate(nodes, key, val, path_to_human)

if __name__ == "__main__":
    inp = get_input()
    inp = get_input('input21.txt')
    part1(inp)
    print("-"*10)
    part2(inp)
