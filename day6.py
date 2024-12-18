# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=6)
# puz.view()


# %%
def parse_data(data: str):
    grid = [list(row) for row in data.split("\n")]
    return grid


def part1(data=None):
    grid = parse_data(data)
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    currdir = 0
    currpos = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    visited = set([currpos])
    grid = navigate_map(grid, directions, currdir, currpos, visited)
    result = len(visited)
    return result


def navigate_map(grid, directions, startdir, startpos, visited):
    currpos = startpos
    currdir = startdir
    nrows, ncols = len(grid), len(grid[0])
    on_grid = True
    steps = 0
    while on_grid:
        nextpos = (currpos[0] + directions[currdir][0], currpos[1] + directions[currdir][1])
        if not (0 <= nextpos[0] < nrows and 0 <= nextpos[1] < ncols):
            on_grid = False
        elif grid[nextpos[0]][nextpos[1]] == "#":
            currdir = (currdir + 1) % 4
        elif grid[nextpos[0]][nextpos[1]] in (".", "^"):
            currpos = nextpos
            visited.add(currpos)
        if currpos[0] == startpos[0] and currpos[1] == startpos[1] and currdir == startdir:
            return "loop!"
        steps += 1
        if steps > 10000:
            return "loop!"
    return grid


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
from copy import deepcopy


def part2(data=None):
    grid = parse_data(data)
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    currdir = 0
    currpos = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    visited = set([currpos])
    grid, blocks = navigate_mapb(grid, directions, currdir, currpos, visited)
    return blocks


def navigate_mapb(grid, directions, startdir, startpos, visited):
    currpos = startpos
    currdir = startdir
    nrows, ncols = len(grid), len(grid[0])
    blocks = 0
    on_grid = True
    while on_grid:
        nextpos = (currpos[0] + directions[currdir][0], currpos[1] + directions[currdir][1])
        if not (0 <= nextpos[0] < nrows and 0 <= nextpos[1] < ncols):
            on_grid = False
        elif grid[nextpos[0]][nextpos[1]] == "#":
            currdir = (currdir + 1) % 4
        elif grid[nextpos[0]][nextpos[1]] in (".", "^"):
            if nextpos not in visited:
                grid_ = deepcopy(grid)
                grid_[nextpos[0]][nextpos[1]] = "#"
                test = navigate_map(grid_, directions, currdir, currpos, set())
                if test == "loop!":
                    blocks += 1
            currpos = nextpos
            visited.add(currpos)
    result = len(visited)
    print(result)
    return grid, blocks


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 6)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
