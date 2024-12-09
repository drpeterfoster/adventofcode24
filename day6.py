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


def check_step2(grid, directions, x, y, current_direction, next_direction):
    x_, y_ = x + directions[current_direction][0], y + directions[current_direction][1]
    if x_ < 0 or x_ >= len(grid) or y_ < 0 or y_ >= len(grid[0]):
        return None
    if grid[x_][y_] == "#":
        return next_direction
    return current_direction


def check_blocker(grid, directions, corners, current_direction, next_direction, x, y):
    ahead_step = x + directions[current_direction][0], y + directions[current_direction][1]
    if ahead_step == "#" or ahead_step == "X":
        return None
    curr_pos = x, y
    while True:
        next_pos = curr_pos[0] + directions[next_direction][0], curr_pos[1] + directions[next_direction][1]
        try:
            if grid[next_pos[0]][next_pos[1]] == "#" and (curr_pos[0], curr_pos[1]) in corners:
                return ahead_step
            curr_pos = next_pos
        except IndexError:
            break
    return None


def part2(data=None):
    grid = parse_data(data)
    nrows, ncols = len(grid), len(grid[0])
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    current_direction = 0
    x, y = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == "^"][0]
    grid[x][y] = "X"
    corners = []
    blocks = []
    while x < nrows and y < ncols:
        next_direction = (current_direction + 1) % 4
        blocker = check_blocker(grid, directions, corners, current_direction, next_direction, x, y)
        if blocker is not None:
            blocks.append(blocker)
        new_direction = check_step2(grid, directions, x, y, current_direction, next_direction)
        if new_direction is None:
            break
        if new_direction != current_direction:
            corners.append((x, y))
        x, y = x + directions[new_direction][0], y + directions[new_direction][1]
        current_direction = new_direction
        grid[x][y] = "X"
    return len(blocks)


# i think this needs to be reworked to treat turns and steps as separate things.
# i.e. the while loop checks the next step and decides to step forward or turrn, then jumps to the next loop.
# this allows for a similar "look ahead" for the blocker check, and should capture the "double turn" case.

# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 6)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%

# get next forward step.
# get next direction.
# if next step is not blocked and is not guard visted, look right until next block.
# if is in corner, +1 to block count.
# if next step is blocked, update direction, continue loop.
