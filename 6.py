import os
from utils import get_input

os.environ['SAMPLE'] = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

def get_marker(line, n_dist=4):
    """n_dist: number of distinct characters"""
    for i in range(n_dist-1, len(line)):
        if len(set(line[i-n_dist+1 : i+1])) == n_dist:
            return i + 1

def part1():
    # for line in get_input():
        # print(get_marker(line))
    print(get_marker(get_input('input6.txt')[0]))

def part2():
    # for line in get_input():
        # print(get_marker(line, n_dist=14))
    print(get_marker(get_input('input6.txt')[0], n_dist=14))

if __name__ == "__main__":
    part1()
    print("-"*10)
    part2()

