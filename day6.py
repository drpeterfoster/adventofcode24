# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=6)
puz.view()


# %%
def parse_data(data: str):
    grid = [list(row) for row in data.split("\n")]
    return grid


def check_step(grid, directions, x, y, current_direction):
    x_, y_ = x + directions[current_direction][0], y + directions[current_direction][1]
    if x_ < 0 or x_ >= len(grid) or y_ < 0 or y_ >= len(grid[0]):
        return None
    if grid[x_][y_] == "#":
        current_direction = (current_direction + 1) % 4
    return current_direction


def part1(data=None):
    grid = parse_data(data)
    nrows, ncols = len(grid), len(grid[0])
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    current_direction = 0
    x, y = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    grid[x][y] = "X"
    steps = 0
    while x < nrows and y < ncols:
        current_direction = check_step(grid, directions, x, y, current_direction)
        if current_direction is None:
            break
        x, y = x + directions[current_direction][0], y + directions[current_direction][1]
        grid[x][y] = "X"
        steps += 1
    result = sum([1 for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "X"])
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=6)


def check_step2(grid, directions, x, y, current_direction):
    x_, y_ = x + directions[current_direction][0], y + directions[current_direction][1]
    if x_ < 0 or x_ >= len(grid) or y_ < 0 or y_ >= len(grid[0]):
        candidate = False
        return None, (None, None), None
    if grid[x_][y_] == "#":
        candidate = False
        current_direction = (current_direction + 1) % 4
        x_, y_ = x + directions[current_direction][0], y + directions[current_direction][1]
    elif grid[x_][y_] != "X":
        candidate = True
    else:
        candidate = False
    return current_direction, (x_, y_), candidate


def solver(grid, directions, current_direction, current_position, recurse=False):
    x, y = current_position
    nrows, ncols = len(grid), len(grid[0])
    steps = 0
    blocks = 0
    while x < nrows and y < ncols:
        current_direction, (x, y), candidate = check_step2(grid, directions, x, y, current_direction)
        if current_direction is None:
            break
        if candidate and recurse:
            grid_ = grid.copy()
            grid_[x][y] = "#"
            steps_, grid_, _ = solver(grid_, directions, current_direction, current_position, False)
            if steps_ == 20000:
                blocks += 1
        grid[x][y] = "X"
        steps += 1
        if steps > 20000:
            return steps, grid, blocks
    return steps, grid, blocks


def part2(data=None):
    grid = parse_data(data)
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    current_direction = 0
    current_position = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    grid[current_position[0]][current_position[1]] = "X"
    steps, grid, blocks = solver(grid, directions, current_direction, current_position, True)
    return blocks


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 6)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%

# get next forward step.
# get next direction.
# if next step is not blocked and is not guard visted, look right until next block.
# if is in corner, +1 to block count.
# if next step is blocked, update direction, continue loop.
