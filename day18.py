# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from heapq import heappop, heappush


# %%
puz = Puzzle(year=2024, day=18)
# puz.view()


# %%
def parse_data(data: str):
    return [tuple(map(int, row.split(","))) for row in data.strip().split("\n")]


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solver(grid, start, end):
    open_set = []
    heappush(open_set, (0, start))  # (priority, current)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heappop(open_set)
        if current == end:
            total_path = []
            while current in came_from:
                total_path.append(current)
                current = came_from[current]
            return total_path[::-1]

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if (
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                and grid[neighbor[0]][neighbor[1]] != "#"
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heappush(open_set, (f_score[neighbor], neighbor))
    return None


def part1(data=None, dim=7, n=12):
    coords = parse_data(data)
    start = (0, 0)
    end = (dim - 1, dim - 1)
    grid = [["." for _ in range(dim)] for _ in range(dim)]
    for c, r in coords[:n]:
        grid[r][c] = "#"
    path = solver(grid, start, end)
    result = len(path)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 22)
resa = part1(puz.input_data, 71, 1024)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
def part2(data=None, dim=7, n=12):
    coords = parse_data(data)
    start = (0, 0)
    end = (dim - 1, dim - 1)
    grid = [["." for _ in range(dim)] for _ in range(dim)]
    for c, r in coords[:n]:
        grid[r][c] = "#"
    path = solver(grid, start, end)
    i = n
    while True:
        c, r = coords[i]
        grid[r][c] = "#"
        if (r, c) in path:
            newpath = solver(grid, start, end)
            if newpath is None:
                break
        i += 1
    result = f"{c},{r}"
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", "6,1")
resb = part2(puz.input_data, 71, 1024)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
