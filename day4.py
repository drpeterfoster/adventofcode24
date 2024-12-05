# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=4)
# puz.view()


# %%
def parse_data(data: str):
    grid = data.split("\n")
    return grid


def valid_xmas(grid, i, j):
    directions = [
        (0, 1),  # right
        (0, -1),  # left
        (1, 0),  # down
        (-1, 0),  # up
        (1, 1),  # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1),  # up-left
    ]
    target = "XMAS"
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for direction in directions:
        di, dj = direction
        valid = True
        for k in range(len(target)):
            ni, nj = i + k * di, j + k * dj
            if ni < 0 or ni >= rows or nj < 0 or nj >= cols or grid[ni][nj] != target[k]:
                valid = False
                break
        if valid:
            count += 1
    return count


def part1(data=None):
    grid = parse_data(data)
    count = 0
    for i, row in enumerate(grid):
        for j, let in enumerate(row):
            if grid[i][j] == "X":
                _count = valid_xmas(grid, i, j)
                count += _count
    return count


# %%
print(
    "found:",
    part1(
        "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX"
    ),
)
print("answer:", 18)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=4)


def valid_x_mas(grid, i, j):
    target = ["MS", "SM"]
    diagonals = [
        ((1, 1), (-1, -1)),
        ((1, -1), (-1, 1)),
    ]
    rows = len(grid)
    cols = len(grid[0])
    itsgood = 0
    for dir1, dir2 in diagonals:
        d1i, d1j = dir1
        d2i, d2j = dir2
        n1i, n1j = i + d1i, j + d1j
        n2i, n2j = i + d2i, j + d2j
        if n1i < 0 or n1i >= rows or n1j < 0 or n1j >= cols or n2i < 0 or n2i >= rows or n2j < 0 or n2j >= cols:
            break
        if grid[n1i][n1j] + grid[n2i][n2j] in target:
            itsgood += 1
    return itsgood == 2


def part2(data=None):
    grid = parse_data(data)
    count = 0
    for i, row in enumerate(grid):
        for j, let in enumerate(row):
            if grid[i][j] == "A":
                _count = valid_x_mas(grid, i, j)
                count += _count
    return count


# %%
print(
    "found:",
    part2(
        "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX"
    ),
)
print("answer:", 9)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
