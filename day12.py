# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=12)
puz.view()


# %%
def parse_data(data: str):
    return [list(row) for row in data.strip().split("\n")]


def flood_fill(map):
    rows, cols = len(map), len(map[0])
    visited = [[False] * cols for _ in range(rows)]
    plots, areas, perims, locs = [], [], [], []

    def dfs(r, c, char):
        stack = [(r, c)]
        area = []
        perimeter = 0
        while stack:
            x, y = stack.pop()
            if visited[x][y]:
                continue
            visited[x][y] = True
            area += [(x, y)]
            local_perimeter = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if map[nx][ny] == char and not visited[nx][ny]:
                        stack.append((nx, ny))
                    elif map[nx][ny] != char:
                        local_perimeter += 1
                else:
                    local_perimeter += 1
            perimeter += local_perimeter
        return area, perimeter

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                char = map[r][c]
                area, perimeter = dfs(r, c, char)
                plots.append(char)
                areas.append(len(area))
                perims.append(perimeter)
                locs.append(area)
    return plots, areas, perims, locs


def part1(data):
    map = parse_data(data)
    plots, areas, perims, locs = flood_fill(map)
    result = sum([a * p for a, p in zip(areas, perims)])
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 140)
print(
    "found:",
    part1(
        "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"
    ),
)
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=12)


from collections import defaultdict


def count_sides(shape):
    def find_edges(coords):
        edges_l, edges_r = set(), set()
        coord_set = set(coords)
        for x in coords:
            if x - 1 not in coord_set:
                edges_l.add(x - 1)  # Left edge
            if x + 1 not in coord_set:
                edges_r.add(x)  # Right edge
        return edges_l, edges_r

    sides = 0
    dx, dy = defaultdict(list), defaultdict(list)
    for x, y in shape:
        dx[x].append(y)
        dy[y].append(x)
    prior_el, prior_er = set(), set()
    for x, ys_ in dx.items():
        ys = list(sorted(ys_))
        el, er = find_edges(ys)
        sides += len(el.difference(prior_el))
        sides += len(er.difference(prior_er))
        prior_el, prior_er = el, er
    prior_el, prior_er = set(), set()
    for x, ys_ in list(sorted(dy.items())):
        ys = list(sorted(ys_))
        el, er = find_edges(ys)
        sides += len(el.difference(prior_el))
        sides += len(er.difference(prior_er))
        prior_el, prior_er = el, er
    return sides


def part2(data):
    map = parse_data(data)
    plots, areas, perims, locs = flood_fill(map)
    sides = [count_sides(c) for c in locs]
    result = sum([a * s for a, s in zip(areas, sides)])
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 80)
print(
    "found:",
    part2(
        "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"
    ),
)
print("answer:", 1206)
print("found:", part2("AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA"))
print("answer:", 368)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%
