# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=8)
# puz.view()


# %%
def parse_data(data: str):
    return [list(row) for row in data.split("\n")]


from collections import defaultdict
from itertools import combinations


def part1(data=None):
    grid = parse_data(data)
    nrows = len(grid)
    ncols = len(grid[0])
    nodes = defaultdict(list)
    antinodes = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != ".":
                nodes[c].append((i, j))
    for node, locs in nodes.items():
        for a, b in combinations(locs, 2):
            delta = a[0] - b[0], a[1] - b[1]
            antinodes.append((a[0] + delta[0], a[1] + delta[1]))
            antinodes.append((b[0] - delta[0], b[1] - delta[1]))
    antinodes = [n for n in antinodes if 0 <= n[0] < nrows and 0 <= n[1] < ncols]
    result = len(set(antinodes))
    return result


# %%
# print("found:", part1(puz.examples[0].input_data))
# print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=8)


def part2(data=None):
    grid = parse_data(data)
    nrows = len(grid)
    ncols = len(grid[0])
    nodes = defaultdict(list)
    antinodes = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != ".":
                nodes[c].append((i, j))
    for node, locs in nodes.items():
        for a, b in combinations(locs, 2):
            delta = a[0] - b[0], a[1] - b[1]
            sx = 1
            antinodes.append(a)
            while True:
                an = a[0] + sx * delta[0], a[1] + sx * delta[1]
                if not (0 <= an[0] < nrows and 0 <= an[1] < ncols):
                    break
                antinodes.append(an)
                sx += 1
            sx = 1
            while True:
                an = a[0] - sx * delta[0], a[1] - sx * delta[1]
                if not (0 <= an[0] < nrows and 0 <= an[1] < ncols):
                    break
                antinodes.append(an)
                sx += 1
    result = len(set(antinodes))
    return result


# %%
# print("found:", part2(puz.examples[0].input_data))
# print("answer:", 34)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
