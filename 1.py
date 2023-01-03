def part1(lines):
    acc = 0
    mx = 0
    for line in lines:
        if line:
            acc += line
        else:
            if acc > mx:
                mx = acc
            acc = 0
    print(mx)

def part2(lines):
    cals = []
    acc = 0
    for line in lines:
        if line:
            acc += line
        else:
            cals.append(acc)
            acc = 0
    print(sum(sorted(cals, reverse=True)[:3]))

if __name__ == "__main__":
    lines = open("input1.txt").read().split("\n")
    lines = [int(i) if i else None for i in lines]
    part1(lines)
    part2(lines)
