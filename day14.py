# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=14)
puz.view()


# %%
def parse_data(data: str):
    lines = data.strip().split("\n")
    parsed_data = []
    for line in lines:
        numbers = list(map(int, re.findall(r"-?\d+", line)))
        parsed_data.append(numbers)
    return parsed_data


def print_grid(data, dims):
    grid = np.ones(dims, dtype=str)
    for vals in data:
        grid[vals[1], vals[0]] = "-"
    [print("".join(row)) for row in grid]


def part1(data=None, dims=(7, 11), seconds=100):
    input = parse_data(data)
    # print_grid(input, dims)
    ty, tx = dims
    quads = {i: 0 for i in range(1, 5)}
    new_pos = []
    for x, y, dx, dy in input:
        x = (x + dx * seconds) % (tx)
        y = (y + dy * seconds) % (ty)
        new_pos.append((x, y))
        if x < (tx // 2) and y < (ty // 2):
            quads[1] += 1
        elif x < (tx // 2) and y > (ty // 2):
            quads[3] += 1
        elif x > (tx // 2) and y < (ty // 2):
            quads[2] += 1
        elif x > (tx // 2) and y > (ty // 2):
            quads[4] += 1
    # print()
    # print_grid(new_pos, dims)
    result = np.prod(list(quads.values()))
    return result


# %%
# print("found:", part1(puz.examples[0].input_data, seconds=100))
# print("answer:", 12)
# resa = part1(puz.input_data, (103, 101))
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=14)


def check_for_tree(grid):
    def bfs(start_x, start_y):
        queue = [(start_x, start_y)]
        size = 0
        while queue:
            x, y = queue.pop(0)
            if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]) or grid[x][y] != "X":
                continue
            grid[x][y] = None  # Mark as visited
            size += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                queue.append((x + dx, y + dy))
        return size

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                if bfs(i, j) >= 50:
                    return True
    return False


def part2(data=None, dims=(103, 101)):
    input = parse_data(data)
    ty, tx = dims
    seconds = 0
    while True:
        seconds += 1
        new_pos = []
        for x, y, dx, dy in input:
            x = (x + dx * seconds) % (tx)
            y = (y + dy * seconds) % (ty)
            new_pos.append((x, y))
        grid = [["-" for _ in range(tx)] for _ in range(ty)]
        for vals in new_pos:
            grid[vals[1]][vals[0]] = "X"
        if check_for_tree(grid):
            break
        if seconds % 10000 == 0:
            print(f"seconds: {seconds}")
    return seconds


# %%
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
