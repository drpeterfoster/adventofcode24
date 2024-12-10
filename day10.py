# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=10)
# puz.view()|
EX = "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"
EX2 = "1110111\n1111111\n1112111\n6543456\n7111117\n8111118\n9111119"
EX3 = "1190119\n1111198\n1112117\n6543456\n7651987\n8761111\n9871111"


# %%
def parse_data(data: str):
    return [list(map(int, list(row))) for row in data.split("\n")]


def is_valid_move(grid, x, y, current_value):
    rows = len(grid)
    cols = len(grid[0])
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] == current_value + 1


def dfs(grid, x, y, current_value):
    if current_value == 9:
        return [(x, y)]
    locs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(grid, nx, ny, current_value):
            locs += dfs(grid, nx, ny, current_value + 1)
    return locs


def part1(data):
    grid = parse_data(data)
    total_score = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                nines = []
                nines += dfs(grid, i, j, 0)
                total_score.append(len(set(nines)))
    return sum(total_score)


# %%
# print("found:", part1(EX))
# print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=10)


def dfs(grid, x, y, current_value):
    if current_value == 9:
        return 1
    locs = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(grid, nx, ny, current_value):
            locs += dfs(grid, nx, ny, current_value + 1)
    return locs


def part2(data):
    grid = parse_data(data)
    total_score = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                total_score += dfs(grid, i, j, 0)
    return total_score


# %%
# print("found:", part2(EX))
# print("answer:", 81)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
