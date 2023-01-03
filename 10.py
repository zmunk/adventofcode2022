import os
from utils import get_input

os.environ['SAMPLE'] = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

def part1(inp):
    cycles = [None]
    x = 1
    for line in inp:
        if line == "noop":
            cycles.append(x)
        else:
            cycles.append(x)
            cycles.append(x)
            val = int(line.split()[-1])
            x += val
    cycles.append(x)

    acc = 0
    for i in [20, 60, 100, 140, 180, 220]:
        acc += i * cycles[i]
    print(acc)

def part2(inp):
    inp = iter(inp)
    x = 1
    val = None
    for i in range(240):
        if val is None:
            try:
                line = next(inp)
            except StopIteration:
                break
            if line == "noop":
                new_val = None
            else:
                new_val = int(line.split()[-1])

        end = ""
        if abs(i % 40 - x) <= 1:
            print("#", end=end)
        else:
            print(".", end=end)

        if val is None:
            val = new_val
        else:
            x += val
            val = None

        if (i + 1) % 40 == 0:
            print()

if __name__ == "__main__":
    inp = get_input('input10.txt')
    part1(inp)
    print("-"*10)
    part2(inp)
