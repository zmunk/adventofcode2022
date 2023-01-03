import os
import re
from collections import defaultdict
from utils import get_input

os.environ['SAMPLE'] = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

regex = re.compile(r'^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$')

def get_bounds(data):
    min_x, max_x, min_y, max_y =  float('inf'), float('-inf'), float('inf'), float('-inf')
    for d in data:
        min_x = min(min_x, d[0])
        max_x = max(max_x, d[0])
        min_y = min(min_y, d[1])
        max_y = max(max_y, d[1])
    return int(min_x), int(max_x), int(min_y), int(max_y)

def display(bounds, sensors, beacons, full_coverage):
    min_x, max_x, min_y, max_y = bounds
    res = ""
    for j in range(min_y, max_y + 1):
        res += f"{j} "
        for i in range(min_x, max_x + 1):
            if (i, j) in sensors:
                res += "S"
            elif (i, j) in beacons:
                res += "B"
            elif (i, j) in full_coverage:
                res += "#"
            else:
                res += "."
        res += "\n"
    print(res[:-1])

def get_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_full_coverage(coverage: dict[tuple, int], bounds):
    x0, x1, y0, y1 = bounds
    full_coverage = set()
    for sensor, dist in coverage.items():
        r = dist
        for j in range(max(y0, sensor[1] - r), min(y1, sensor[1] + r) + 1):
            w = r - abs(j - sensor[1])
            for i in range(max(x0, sensor[0] - w), min(x1, sensor[0] + w) + 1):
                full_coverage.add((i, j))
    return full_coverage

def part1(inp, y):
    beacons = set()
    full_coverage = set()
    for row in inp:
        sx, sy, bx, by = list(map(int, regex.fullmatch(row).groups()))
        dist = get_distance((sx, sy), (bx, by))
        k = dist - abs(y - sy)
        for i in range(sx - k, sx + k + 1):
            full_coverage.add((i, y))
        beacons.add((bx, by))
    acc = 0
    for point in full_coverage:
        if point[1] == y and point not in beacons:
            acc += 1
    print(acc)

def part2(inp, size):
    data = []
    sensors = set()
    beacons = set()
    full_coverage = set()
    distance = defaultdict(int)
    for row in inp:
        sx, sy, bx, by = list(map(int, regex.fullmatch(row).groups()))
        dist = get_distance((sx, sy), (bx, by))
        sensor = (sx, sy)
        distance[sensor] = max(dist, distance[sensor])
        sensors.add((sx, sy))
        beacons.add((bx, by))

    p = [0, 0]
    while True:
        for sensor, dist in distance.items():
            if get_distance(p, sensor) <= dist:
                break
        else:
            break
        sx, sy = sensor
        p[0] = sx + dist - abs(sy - p[1]) + 1
        if p[0] > size:
            p = [0, p[1] + 1]
        continue
    print(int(p[0] * 4e6 + p[1]))

if __name__ == "__main__":
    sample = get_input()
    inp = get_input('input15.txt')
    part1(sample, y=10)
    # part1(inp, y=2_000_000)
    print("-"*10)
    part2(sample, 20)
    part2(inp, 4_000_000) # [3403960, 3289729]
