# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from heapq import heappop, heappush
from collections import deque


# %%
puz = Puzzle(year=2024, day=16)
# puz.view()


# %%
def parse_data(data: str):
    grid = [list(row) for row in data.strip().split("\n")]
    start = None
    end = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)
            elif val == "E":
                end = (r, c)
    return grid, start, end


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solver(grid, start, end, directions):
    open_set = []
    heappush(open_set, (0, start, (start[0], start[1] - 1), 0))  # (priority, current, previous, direction)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current, previous, prev_direction = heappop(open_set)

        if current == end:
            score = g_score[current]
            total_path = []
            while current in came_from:
                total_path.append(current)
                current = came_from[current]
            return total_path[::-1], score

        for direction, (dr, dc) in enumerate(directions):
            neighbor = (current[0] + dr, current[1] + dc)
            if (
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                and grid[neighbor[0]][neighbor[1]] != "#"
            ):
                tentative_g_score = g_score[current] + 1
                if direction != prev_direction:
                    tentative_g_score += 1000

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heappush(open_set, (f_score[neighbor], neighbor, current, direction))

    return None, None


def solver_all_paths(grid, start, end, directions, target_score):
    open_set = deque([(start, [start], (start[0], start[1] - 1), 0, 0)])  # (current, path, previous, direction, score)
    visited = {}
    all_paths = []
    i = 0
    while open_set:
        i += 1
        if i % 10000 == 0:
            print(len(open_set))
        current, path, previous, prev_direction, score = open_set.popleft()

        if current == end and score == target_score:
            all_paths.append(path)
            continue

        for direction, (dr, dc) in enumerate(directions):
            neighbor = (current[0] + dr, current[1] + dc)
            if (
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                and grid[neighbor[0]][neighbor[1]] != "#"
                and neighbor not in path
            ):
                score_ = score + 1
                if direction != prev_direction:
                    score_ += 1000
                visited_score = visited.get((neighbor[0], neighbor[1], direction), float("inf"))
                if score_ <= target_score and score_ <= visited_score:
                    visited[(neighbor[0], neighbor[1], direction)] = score_
                    open_set.append((neighbor, path + [neighbor], current, direction, score_))

    return all_paths


def part1(data=None):
    grid, start, end = parse_data(data)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    _, score = solver(grid, start, end, directions)
    return score


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 7036)
print(
    "found:",
    part1(
        "#################\n#...#...#...#..E#\n#.#.#.#.#.#.#.#.#\n#.#.#.#...#...#.#\n#.#.#.#.###.#.#.#\n#...#.#.#.....#.#\n#.#.#.#.#.#####.#\n#.#...#.#.#.....#\n#.#.#####.#.###.#\n#.#.#.......#...#\n#.#.###.#####.###\n#.#.#...#.....#.#\n#.#.#.#####.###.#\n#.#.#.........#.#\n#.#.#.#########.#\n#S#.............#\n#################"
    ),
)
print("answer:", 11048)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%


def part2(data=None):
    grid, start, end = parse_data(data)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    target_score = part1(data)
    paths = solver_all_paths(grid, start, end, directions, target_score)
    positions = {pos for path in paths for pos in path}
    return len(positions)


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 45)
print(
    "found:",
    part2(
        "#################\n#...#...#...#..E#\n#.#.#.#.#.#.#.#.#\n#.#.#.#...#...#.#\n#.#.#.#.###.#.#.#\n#...#.#.#.....#.#\n#.#.#.#.#.#####.#\n#.#...#.#.#.....#\n#.#.#####.#.###.#\n#.#.#.......#...#\n#.#.###.#####.###\n#.#.#...#.....#.#\n#.#.#.#####.###.#\n#.#.#.........#.#\n#.#.#.#########.#\n#S#.............#\n#################"
    ),
)
print("answer:", 64)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
