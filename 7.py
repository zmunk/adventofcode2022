import os
from utils import get_input

os.environ['SAMPLE'] = """
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    """


class Tree:
    def __init__(self, name):
        self.name = name
        self.children = []

    def __str__(self):
        return f"{self.name} [{self.size}]"

    def __repr__(self):
        r = str(self) + "\n"
        for child in self.children:
            if isinstance(child, int):
                r += f"  {child}\n"
            else:
                for line in repr(child).split("\n"):
                    r += f"  {line}\n"
        return r.strip()

    def resolve_size(self):
        acc = 0
        for child in self.children:
            if isinstance(child, Tree):
                child.resolve_size()
                acc += child.size
            else:
                acc += child
        self.size = acc


class TreeDict:
    def __init__(self):
        self.dict = {}
        self.root = self['/']

    def __getitem__(self, key):
        if tree := self.dict.get(key):
            return tree
        tree = Tree(key)
        self.dict[key] = tree
        return tree

    def __len__(self):
        return len(self.dict)

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

def combine(path_arr):
    return "/" + "/".join(path_arr[1:])

def get_trees(inp):
    trees = TreeDict()
    path_arr = []

    for line in inp:
        if (line[0], line[1]) == ("$", "cd"):
            dest = line[2]
            if dest == "..":
                path_arr.pop()
            else:
                path_arr.append(dest)
            continue

        if line[0] == "$":
            continue

        pwd = combine(path_arr)
        tree = trees[pwd]
        if line[0] == 'dir':
            child_path = combine(path_arr + [line[1]])
            tree.children.append(trees[child_path])
        else:
            tree.children.append(int(line[0]))

    trees.root.resolve_size()
    return trees

def part1():
    inp = [x.split(" ") for x in get_input('input7.txt')]
    trees = get_trees(inp)

    acc = 0
    for tree in trees.values():
        if tree.size < 100_000:
            acc += tree.size

    print(acc)

def part2():
    inp = [x.split(" ") for x in get_input('input7.txt')]
    trees = get_trees(inp)
    min_size = trees.root.size - 40_000_000
    smallest = float('inf')
    for tree in trees.values():
        if tree.size > min_size and tree.size < smallest:
            smallest = tree.size
    print(smallest)

if __name__ == "__main__":
    part1()
    print("-"*10)
    part2()
