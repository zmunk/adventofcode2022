import textwrap

def priority(c):
    if c >= 'a':
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27

def get_input(file=None):
    sample = """\
    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw\
    """
    if file:
        inp = open(file).read().split("\n")[:-1]
    else:
        inp = textwrap.dedent(sample).split("\n")[:-1]
    return inp

def part1():
    assert priority('a') == 1
    assert priority('z') == 26
    assert priority('A') == 27
    assert priority('Z') == 52

    inp = get_input('input3.txt')
    acc = 0
    for rucksack in inp:
        mid = len(rucksack) // 2
        common = list(set(rucksack[:mid]) & set(rucksack[mid:]))[0]
        acc += priority(common)
    print(acc)

def part2():
    inp = get_input('input3.txt')
    acc = 0
    for a, b, c in zip(*[iter(inp)]*3):
        acc += priority(list(set(a) & set(b) & set(c))[0])
    print(acc)

if __name__ == "__main__":
    part2()

