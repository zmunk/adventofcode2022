import os
import re
import time
from copy import deepcopy, copy
from utils import get_input

os.environ['SAMPLE'] = """
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
"""

regex = re.compile(" ".join([
    r"Blueprint (\d+):",
    r"Each ore robot costs (\d+) ore.",
    r"Each clay robot costs (\d+) ore.",
    r"Each obsidian robot costs (\d+) ore and (\d+) clay.",
    r"Each geode robot costs (\d+) ore and (\d+) obsidian.",
]))

RESOURCE_TYPES = ["Ore", "Clay", "Obsidian", "Geode"]

def process_sample(inp):
    inp = iter(inp)
    res = []
    while True:
        res.append(" ".join(next(inp).strip() for j in range(5)))
        try:
            next(inp)
        except StopIteration:
            break
    return res

def get_blueprint(s):
    n, ore, c, ob1, ob2, g1, g3 = [int(x) for x in regex.match(s).groups()]
    blueprint = {
        "Ore": (ore, 0, 0),
        "Clay": (c, 0, 0),
        "Obsidian": (ob1, ob2, 0),
        "Geode": (g1, 0, g3),
    }
    return n, blueprint

class Branch:
    def __init__(self, state=None, time=0, history=None):
        self.state = state or {
            "Ore": [1, 0],
            "Clay": [0, 0],
            "Obsidian": [0, 0],
            "Geode": [0, 0],
        }
        self.time = time
        costs = blueprint.values()
        self.max = {
            "Ore": max(b[0] for b in costs),
            "Clay": max(b[1] for b in costs),
            "Obsidian": max(b[2] for b in costs),
            "Geode": float('inf'),
        }
        self.history = history or []

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self)

    def get_n_bots(self, res):
        return self.state[res][0]

    def get_n_res(self, res):
        return self.state[res][1]

    def get_n_req(self, res, req):
        i = {"Ore": 0, "Clay": 1, "Obsidian": 2}[req]
        return blueprint[res][i]

    def copy(self):
        return Branch(
            state=deepcopy(self.state),
            time=self.time,
            history=copy(self.history),
        )

    def split(self):
        goals = self.get_goal_options()
        new_branches = []
        for goal in goals:
            new_branch = self.copy()
            new_branch.goal = goal
            new_branches.append(new_branch)
        return new_branches

    def get_goal_options(self):
        goals = []
        n_ore_bots = self.get_n_bots("Ore")
        n_clay_bots = self.get_n_bots("Clay")
        n_obs_bots = self.get_n_bots("Obsidian")
        if n_ore_bots >= self.get_n_req("Geode", "Ore") and\
                n_obs_bots >= self.get_n_req("Geode", "Obsidian"):
            return ["Geode"]
        for res, (n_bots, _) in self.state.items():
            if n_bots >= self.max[res]:
                continue
            if res in ["Ore", "Clay"] or \
                    (res == "Obsidian" and n_clay_bots > 0) or \
                    (res == "Geode" and n_obs_bots > 0):
                goals.append(res)
        return goals

    def reach_goal(self, goal=None):
        goal = goal or self.goal
        if not self.check_goal_feasible(goal):
            raise ValueError(f"can't obtain {goal}, {self.state = }")
        while not self.can_buy(goal):
            self.update()
            if self.time == time_limit:
                return False
        self.buy(goal)
        return True

    def check_goal_feasible(self, goal):
        if goal in ["Ore", "Clay"]:
            return True
        if goal == "Obsidian":
            return self.state["Clay"][0] > 0
        if goal == "Geode":
            return self.state["Obsidian"][0] > 0

    def can_buy(self, robot_type):
        sufficient_ore = self.get_n_res("Ore") >= self.get_n_req(robot_type, "Ore")
        if not sufficient_ore:
            return False
        if robot_type in ["Ore", "Clay"]:
            return True

        sufficient_clay =\
            self.get_n_res("Clay") >= self.get_n_req(robot_type, "Clay")
        if robot_type == "Obsidian":
            return sufficient_clay

        sufficient_obsidian =\
            self.get_n_res("Obsidian") >= self.get_n_req(robot_type, "Obsidian")
        if robot_type == "Geode":
            return sufficient_obsidian

        raise ValueError(f"invalid robot type: {robot_type!r}")

    def max_possible_geodes(self):
        t_rem = time_limit - self.time
        n_geodes = self.get_n_res("Geode")
        n_bots = self.get_n_bots("Geode")
        return n_geodes + n_bots * t_rem + t_rem * (t_rem - 1) // 2

    def buy(self, resource):
        for res, amt in zip(self.state.values(), blueprint[resource]):
            res[1] -= amt
        self.update()
        self.state[resource][0] += 1
        self.history.append(resource)

    def update(self):
        for amt in self.state.values():
            amt[1] += amt[0]
        self.time += 1

def get_baseline():
    def achieve_goals(goals, branch=None):
        if branch is None:
            branch = Branch(blueprint)
        for goal in goals:
            try:
                branch.reach_goal(goal)
            except ValueError:
                return False
        if branch.time > time_limit:
            return False
        return True

    def calc_geodes(goals) -> int:
        branch = Branch()
        if not achieve_goals(goals, branch):
            return -1
        while branch.time < time_limit:
            branch.update()
        return branch.state["Geode"][1]

    def max_handler(val, obj):
        nonlocal max_val, max_objects

        if val > max_val:
            max_val = val
            max_objects = [obj]
        elif val == max_val:
            max_objects.append(obj)

    max_val = float('-inf')
    max_objects = []

    max_ore = max(blueprint[res][0] for res in RESOURCE_TYPES)
    max_clay = blueprint["Obsidian"][1]
    max_obs = blueprint["Geode"][2]

    for n_ore in range(max_ore + 1):
        for n_clay in range(max_clay + 1):
            for n_obs in range(max_obs + 1):
                n_geode = 1
                last_c = 0
                while True:
                    goals = ["Ore"] * n_ore
                    goals += ["Clay"] * n_clay
                    goals += ["Obsidian"] * n_obs
                    goals += ["Geode"] * n_geode
                    c = calc_geodes(goals)
                    if c < 0:
                        break
                    max_handler(c, [n_ore, n_clay, n_obs, n_geode])
                    if c <= last_c:
                        break
                    last_c = c
                    n_geode += 1
    return max_val

def part1(blueprints):
    global time_limit, blueprint

    time_limit = 24
    acc = 0
    for n, b in blueprints:
        blueprint = b
        acc += n * get_max_geodes()
    print(f"{acc = }")

def part2(blueprints):
    global time_limit, blueprint

    time_limit = 32
    acc = 1
    for b in blueprints:
        blueprint = b
        acc *= get_max_geodes()
    print(f"{acc = }")

def get_max_geodes():
    def max_handler(val):
        nonlocal max_geodes
        if val > max_geodes:
            max_geodes = val
            print(f"{max_geodes = }")

    def progress_handler(l):
        nonlocal last_l
        inc = 100 * (l - last_l) / last_l
        direction = "increase" if inc > 0 else "decrease"
        print(f"{len(branches) = }, ({abs(inc):.2f}% {direction}) ")
        last_l = l

    max_geodes = get_baseline()
    print(f"{max_geodes = }")
    while True:
        branches = Branch().split()
        last_l = 1
        try_again = False
        while len(branches) > 0:
            progress_handler(len(branches))
            to_remove, to_add = [], []
            for branch in branches:
                to_remove.append(branch)
                if branch.max_possible_geodes() <= max_geodes:
                    continue
                if not branch.reach_goal():
                    max_handler(branch.get_n_res("Geode"))
                    continue
                new_branches = branch.split()
                to_add.extend(new_branches)
            for branch in to_remove:
                branches.remove(branch)
            branches.extend(to_add)
        if not try_again:
            break

    print(f"{max_geodes = }")
    return max_geodes

if __name__ == "__main__":
    inp = process_sample(get_input())
    # inp = get_input('input19.txt')

    blueprints = []
    for line in inp:
        blueprints.append(get_blueprint(line))
    part1(blueprints)
    print("-"*10)
    blueprints = []
    for line in inp[:3]:
        blueprints.append(get_blueprint(line)[1])
    # part2(blueprints) # 16 * 20 * 7 = 2240
    print("-"*10)


