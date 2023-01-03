import os
import re
import time
import builtins
from collections import defaultdict
from itertools import permutations, combinations
from utils import get_input

os.environ['SAMPLE'] = """
    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
    Valve CC has flow rate=2; tunnels lead to valves DD, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve FF has flow rate=0; tunnels lead to valves EE, GG
    Valve GG has flow rate=0; tunnels lead to valves FF, HH
    Valve HH has flow rate=22; tunnel leads to valve GG
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve JJ has flow rate=21; tunnel leads to valve II
    """

regex = re.compile(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? ((?:,? ?\w\w)+)$')

class Node:
    def __init__(self, valve, flow_rate, neighbors):
        self.valve = valve
        self.flow_rate = flow_rate
        self.neighbors = neighbors
        self.distances = defaultdict(lambda: float('inf'))

    def __str__(self):
        return self.valve

    def __repr__(self):
        return str(self)

    def get_distance(self, node):
        return self.distances[node.valve]

    def set_distance(self, node, distance):
        if distance >= self.distances[node.valve]:
            return False
        self.distances[node.valve] = distance
        return True

    def connect(self, connections):
        self.neighbors = connections

    def propagate(self):
        self.set_distance(self, 0)
        for node in self.neighbors:
            node.notify(self, 1)

    def notify(self, src, distance):
        if not self.set_distance(src, distance):
            return
        for node in self.neighbors:
            node.notify(src, distance + 1)

def create_graph(inp):
    graph = {}
    for line in inp:
        valve, flow_rate, neighbors = list(regex.match(line).groups())
        graph[valve] = Node(valve, int(flow_rate), neighbors.split(", "))
    nodes = graph.values()
    for node in nodes:
        node.connect([graph[t] for t in node.neighbors])
    for node in nodes:
        node.propagate()
    return graph

def evaluate(perm, t=26):
    node = 'AA'
    res = ""
    for nxt in perm:
        dist = graph[node].distances[nxt]
        t -= dist + 1
        if t <= 0:
            break
        flow = graph[nxt].flow_rate
        res += f"+ {t} * {flow} "
        node = nxt
    res = res[2:-1]
    return eval(res)

def get_best(perms, n=1):
    scores = []
    for perm in perms:
        scores.append(evaluate(perm), t=30)

    if n == 1:
        best_score = max(scores)
        return perms[scores.index(best_score)], best_score

    return sorted(zip(perms, scores), reverse=True, key=lambda x: x[1])[:n]

def part1(inp):
    global graph

    t = time.time()
    graph = create_graph(inp)
    print(f"created graph ({time.time() - t:.4f}s)")

    valves = list(filter(lambda x: graph[x].flow_rate != 0, graph))

    t = time.time()
    print(get_best(list(permutations(valves, 6))))
    print(f"got best permutation ({time.time() - t:.4f}s)")

def part2(valves, perm_size=4):
    global perms

    combo_scores = defaultdict(int)

    perms = list(permutations(valves, perm_size))
    for perm in perms:
        score = evaluate(perm)
        combo = tuple(sorted(perm))
        if score > combo_scores[combo]:
            combo_scores[combo] = score
    combos = {combo: set(combo) for combo in combo_scores.keys()}

    max_score = 0
    for combo, combo_set in combos.items():
        score = combo_scores[combo]
        for other, other_set in combos.items():
            # if combo_set & other_set:
                # continue
            for c in combo:
                if c in other_set:
                    break
            else:
                if (total_score := score + combo_scores[other]) > max_score:
                    max_score = total_score
    print(f"{max_score = }")

if __name__ == "__main__":
    # global graph

    # inp = get_input(); perm_size = 3
    inp = get_input('input16.txt'); perm_size = 6 # 1559
    graph = create_graph(inp)
    valves = list(filter(lambda x: graph[x].flow_rate != 0, graph))

    # part1(inp)
    print("-"*10)
    t = time.time()
    part2(valves, perm_size)
    print(f"part 2 ({time.time() - t:.4f}s)")
    # 2139, 2178 incorrect
