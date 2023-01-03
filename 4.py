import textwrap
import re

def get_input(file=None):
    sample = """\
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8
    """
    if file:
        inp = open(file).read().split("\n")[:-1]
    else:
        inp = textwrap.dedent(sample).split("\n")[:-1]
    return inp

def part1():
    inp = get_input('input4.txt')
    count = 0
    rgx = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    for line in inp:
        a, b, c, d = [int(x) for x in re.match(rgx, line).groups()]
        if a <= c and b >= d or a >= c and b <= d:
            count += 1
    print(count)

def part2():
    inp = get_input('input4.txt')
    count = 0
    rgx = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    for line in inp:
        a, b, c, d = [int(x) for x in re.match(rgx, line).groups()]
        if c <= a <= d or c <= b <= d or a <= c <= b:
            count += 1
    print(count)

if __name__ == "__main__":
    part1()
    print("-"*10)
    part2()

