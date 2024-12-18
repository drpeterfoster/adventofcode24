# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=15)
puz.view()


# %%
def parse_data(data: str):
    grid, seq = data.strip().split("\n\n")
    grid = [list(row) for row in grid.strip().split("\n")]
    seq = seq.strip().replace("\n", "")
    return grid, seq


def move(pos, dir, grid):
    stack = []
    query = pos
    while grid[query[1]][query[0]] != ".":
        query_ = (query[0] + dir[0], query[1] + dir[1])
        stack.append((query_, grid[query[1]][query[0]]))
        if grid[query[1]][query[0]] == "#":
            return pos, grid
        query = query_
    stack.append((pos, "."))
    for query, cell in stack:
        grid[query[1]][query[0]] = cell
    return (pos[0] + dir[0], pos[1] + dir[1]), grid


def agg_result(grid):
    return sum([y * 100 + x for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "O"])


def print_grid(grid):
    [print("".join(row)) for row in grid]


def part1(data=None):
    grid, seq = parse_data(data)
    dirs = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    pos = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "@"][0]
    for dir in seq:
        pos, grid = move(pos, dirs[dir], grid)
        # print_grid(grid)
        # continue
    result = agg_result(grid)
    return result


# %%
# print("found:", part1(puz.examples[0].input_data))
# print("answer:", 10092)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=15)


def part2(data=None):
    input = parse_data(data)
    result = 0
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_b)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
