import os
from utils import get_input

os.environ['SAMPLE'] = """
    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2
    """

# os.environ['SAMPLE'] = """
    # R 5
    # U 8
    # L 8
    # D 3
    # R 17
    # D 10
    # L 25
    # U 20
    # """

class Position:
    def __init__(self):
        self._x = 0
        self._y = 0

    def __str__(self):
        return f"Pos ({self._x}, {self._y})"

    def __repr__(self):
        return str(self)

    def tuple(self):
        return (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def update(self, pos):
        self._x, self._y = pos

    def move(self, dir_):
        if dir_ == 'R':
            self._x += 1
        elif dir_ == 'D':
            self._y += 1
        elif dir_ == 'L':
            self._x -= 1
        elif dir_ == 'U':
            self._y -= 1
        else:
            raise ValueError(f'invalid direction: {dir_}')
def sign(v):
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0

def move_tail(head, tail):
    """Return new tail position as tuple"""
    x_diff = abs(head.x - tail.x)
    y_diff = abs(head.y - tail.y)
    x, y = tail.x, tail.y
    if head.x == tail.x:
        if y_diff > 1:
            # move 1 step in y direction
            y = tail.y + sign(head.y - tail.y)
    elif head.y == tail.y:
        if x_diff > 1:
            # move 1 step in x direction
            x = tail.x + sign(head.x - tail.x)
    else:
        if x_diff + y_diff > 2:
            # move 1 step diagonally
            x = tail.x + sign(head.x - tail.x)
            y = tail.y + sign(head.y - tail.y)
    return (x, y)

def part1(inp):
    head = Position()
    tail = Position()
    tail_history = {tail.tuple()}
    for line in inp:
        for _ in range(line[1]):
            head.move(line[0])
            tail.update(move_tail(head, tail))
            tail_history.add(tail.tuple())
    print(len(tail_history))

def part2(inp):
    head = Position()
    knots = [Position() for _ in range(9)]
    tail = knots[-1]
    tail_history = {tail.tuple()}
    for line in inp:
        for _ in range(line[1]):
            head.move(line[0])
            leading = head
            for trailing in knots:
                new_pos = move_tail(leading, trailing)
                trailing.update(new_pos)
                leading = trailing
            tail_history.add(tail.tuple())
    print(len(tail_history))

if __name__ == "__main__":
    inp = [(x.split()[0], int(x.split()[1])) for x in get_input('input9.txt')]
    part1(inp)
    print("-"*10)
    part2(inp)
