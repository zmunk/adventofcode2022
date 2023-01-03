import re
import textwrap

def get_input(file=None):
    if file:
        inp = open(file).read().split("\n")[:-1]
    else:
        inp = textwrap.dedent(SAMPLE).split("\n")[:-1]
    return inp

SAMPLE = """\
        [D]    
    [N] [C]    
    [Z] [M] [P]
    1   2   3 

    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
    """

def part1():
    inp = get_input('input5.txt')
    n_stacks = (len(inp[0]) + 1) // 4
    regex = re.compile(" ".join([r"( {3}|\[\w\])"] * n_stacks))
    inp = iter(inp)
    stacks = [None] + [[] for _ in range(n_stacks)]
    for line in inp:
        m = regex.match(line)
        if not m:
            break
        for ind, crate in enumerate(m.groups(), start=1):
            if crate.strip() == "":
                continue
            stacks[ind].insert(0, crate[1])

    next(inp)

    regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in inp:
        m = regex.match(line)
        n, src, dest = [int(x) for x in m.groups()]
        for _ in range(n):
            stacks[dest].append(stacks[src].pop())

    print("".join(x[-1] for x in stacks[1:]))

def part2():
    inp = get_input('input5.txt')
    n_stacks = (len(inp[0]) + 1) // 4
    regex = re.compile(" ".join([r"( {3}|\[\w\])"] * n_stacks))
    inp = iter(inp)
    stacks = [None] + [[] for _ in range(n_stacks)]
    for line in inp:
        m = regex.match(line)
        if not m:
            break
        for ind, crate in enumerate(m.groups(), start=1):
            if crate.strip() == "":
                continue
            stacks[ind].insert(0, crate[1])

    next(inp)

    regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in inp:
        m = regex.match(line)
        n, src, dest = [int(x) for x in m.groups()]
        stacks[dest] += stacks[src][-n:]
        del stacks[src][-n:]

    print("".join(x[-1] for x in stacks[1:]))

if __name__ == "__main__":
    part1()
    print("-"*10)
    part2()
