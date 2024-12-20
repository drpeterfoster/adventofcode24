# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from tqdm import tqdm


# %%
puz = Puzzle(year=2024, day=20)
# puz.view()


# %%
def parse_data(data: str):
    grid = [list(row) for row in data.strip().split("\n")]
    start, end = None, None
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start = (i, j)
            if char == "E":
                end = (i, j)
    return grid, start, end


def solver(grid, start, end):
    path = []
    r, c = start
    while (r, c) != end:
        path.append((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if grid[nr][nc] in (".", "E") and (nr, nc) not in path:
                r, c = nr, nc
                break
    path.append(end)
    return path


from itertools import combinations


def find_jumps(grid, path):
    jumps = []
    for a, b in combinations(path, r=2):
        if a[0] == b[0] and abs(a[1] - b[1]) == 2 and grid[a[0]][(a[1] + b[1]) // 2] == "#":
            jumps.append((a, b))
        if a[1] == b[1] and abs(a[0] - b[0]) == 2 and grid[(a[0] + b[0]) // 2][a[1]] == "#":
            jumps.append((a, b))
    return jumps


def assess_jumps(path, jumps):
    cheats = []
    for a, b in jumps:
        i = path.index(a)
        j = path.index(b)
        cheats.append(abs(i - j) - 2)
    return cheats


def part1(data=None, over=99):
    grid, start, end = parse_data(data)
    path = solver(grid, start, end)
    jumps = find_jumps(grid, path)
    cheats = assess_jumps(path, jumps)
    result = sum([1 for c in cheats if c > over])
    return result


# %%
print("found:", part1(puz.examples[0].input_data, 30))
print("answer:", 4)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
from scipy.spatial.distance import cdist


def find_cheats(path, n):
    # man arr
    arr = np.array(path)
    man = cdist(arr, arr, metric="cityblock")
    # lin arr
    s = len(path)
    lin = np.zeros((s, s), dtype=int)
    for i in range(s):
        for j in range(s):
            lin[i, j] = abs(i - j)
    com = lin - man
    cheats = com[np.logical_and(man <= 20, np.triu(lin))]
    cheats = cheats[cheats >= n]
    # print(np.unique(cheats, return_counts=True))
    return len(cheats)


def part2(data=None, n=10):
    grid, start, end = parse_data(data)
    path = solver(grid, start, end)
    result = find_cheats(path, n)
    return result


# %%
print("found:", part2(puz.examples[0].input_data, 70))
print("answer:", 29)
resb = part2(puz.input_data, 100)
print(f"solution: {resb}")
puz.answer_b = resb


# %%
