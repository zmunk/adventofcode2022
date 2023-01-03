def part1(turns):
    score = 0

    for opp, you in turns:

        if opp == 'A':
            if you == 'Y':
                score += 6  # WIN
            elif you == 'X':
                score += 3  # DRAW
        elif opp == 'B':
            if you == 'Z':
                score += 6  # WIN
            elif you == 'Y':
                score += 3  # DRAW
        else:
            if you == 'X':
                score += 6  # WIN
            if you == 'Z':
                score += 3  # DRAW

        if you == 'X':
            score += 1
        elif you == 'Y':
            score += 2
        else:
            score += 3

    print(score)

def part2(turns):
    score = 0

    """
    A X
    + 0 + 3
    A Y
    + 3 + 1
    A Z
    + 6 + 2

    B X
    + 0 + 1
    B Y
    + 3 + 2
    B Z
    + 6 + 3

    C X
    + 0 + 2
    C Y
    + 3 + 3
    C Z
    + 6 + 1
    """


    for opp, you in turns:
        if opp == 'A':
            if you == 'X':
                score += 3
            elif you == 'Y':
                score += 4
            else:
                score += 8
        elif opp == 'B':
            if you == 'X':
                score += 1
            elif you == 'Y':
                score += 5
            else:
                score += 9
        else:
            if you == 'X':
                score += 2
            elif you == 'Y':
                score += 6
            else:
                score += 7

    print(score)

if __name__ == "__main__":
    lines = open("input2.txt").read().strip().split("\n")
    turns = [a.split() for a in lines]
    part1(turns)
    part2(turns)
