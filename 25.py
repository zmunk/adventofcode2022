import os
from utils import get_input

os.environ['SAMPLE'] = """
    1=-0-2
    12111
    2=0=
    21
    2=01
    111
    20012
    112
    1=-1=
    1-12
    12
    1=
    122
    """

def snafu(n: int) -> str:
    if n == 0:
        return ""
    c = n % 5
    if c == 3:
        v = '='
        n += 2
    elif c == 4:
        v = '-'
        n += 1
    else:
        v = str(c)
    return snafu(n // 5) + v

def desnafu(s: str) -> int:
    if len(s) == 0:
        return 0
    if (c := s[-1]) in ['0', '1', '2']:
        v = int(c)
    elif c == '-':
        v = -1
    else:
        assert c == '='
        v = -2
    return v + 5 * desnafu(s[:-1])

if __name__ == "__main__":
    inp = get_input('input25.txt')
    acc = 0
    for line in inp:
        acc += desnafu(line)
