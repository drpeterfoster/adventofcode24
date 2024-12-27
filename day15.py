# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=15)
# puz.view()


# %%
def parse_data(data: str):
    grid, seq = data.strip().split("\n\n")
    grid = [list(row) for row in grid.strip().split("\n")]
    seq = seq.strip().replace("\n", "")
    return grid, seq


def move(pos, dir, grid):
    stack = []
    query = pos
    while grid[query[0]][query[1]] != ".":
        query_ = (query[0] + dir[0], query[1] + dir[1])
        stack.append((query_, grid[query[0]][query[1]]))
        if grid[query[0]][query[1]] == "#":
            return pos, grid
        query = query_
    stack.append((pos, "."))
    for query, cell in stack:
        grid[query[0]][query[1]] = cell
    return (pos[0] + dir[0], pos[1] + dir[1]), grid


def agg_result(grid):
    return sum(
        [
            y * 100 + x
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell == "O"
        ]
    )


def print_grid(grid):
    [print("".join(row)) for row in grid]


def part1(data=None):
    grid, seq = parse_data(data)
    dirs = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    pos = [
        (x, y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == "@"
    ][0]
    for dir in seq:
        pos, grid = move(pos, dirs[dir], grid)
        # print_grid(grid)
        # continue
    result = agg_result(grid)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 10092)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
from copy import deepcopy

def move_box(bl, br, dir, grid):
    nbl = (bl[0] + dir[0], bl[1] + dir[1])
    nbr = (br[0] + dir[0], br[1] + dir[1])
    
    if dir in [(1, 0), (-1, 0)]:
        if "#" in (grid[nbl[0]][nbl[1]], grid[nbr[0]][nbr[1]]):
            return grid
        if grid[nbl[0]][nbl[1]] == "]":
            grid = move_box((nbl[0], nbl[1] - 1), nbl, dir, grid)
        if grid[nbl[0]][nbl[1]] == "[":
            grid = move_box(nbl, nbr, dir, grid)
        if grid[nbr[0]][nbr[1]] == "[":
            grid = move_box(nbr, (nbr[0], nbr[1] + 1), dir, grid)
        if (".", ".") == (grid[nbl[0]][nbl[1]], grid[nbr[0]][nbr[1]]):
            grid[nbl[0]][nbl[1]] = "["
            grid[nbr[0]][nbr[1]] = "]"
            grid[bl[0]][bl[1]] = "."
            grid[br[0]][br[1]] = "."
            return grid
        
    if dir == (0, -1):
        if grid[nbl[0]][nbl[1]] == "#":
            return grid
        if grid[nbl[0]][nbl[1]] == "]":
            grid = move_box((nbl[0], nbl[1] - 1), nbl, dir, grid)
        if grid[nbl[0]][nbl[1]] == ".":
            grid[nbl[0]][nbl[1]] = "["
            grid[nbr[0]][nbr[1]] = "]"
            grid[br[0]][br[1]] = "."
            return grid

    if dir == (0, 1):
        if grid[nbr[0]][nbr[1]] == "#":
            return grid
        if grid[nbr[0]][nbr[1]] == "[":
            return move_box(nbr, (nbr[0], nbr[1] + 1), dir, grid)
        if grid[nbr[0]][nbr[1]] == ".":
            grid[nbr[0]][nbr[1]] = "]"
            grid[nbl[0]][nbl[1]] = "["
            grid[bl[0]][bl[1]] = "."
            return grid
    return grid

def move2(pos, dir, grid):
    nextpos = (pos[0] + dir[0], pos[1] + dir[1])
    if grid[nextpos[0]][nextpos[1]] == "[":
        grid = move_box(nextpos, (nextpos[0], nextpos[1] + 1), dir, grid)
        pos, grid = move2(pos, dir, grid)
    elif grid[nextpos[0]][nextpos[1]] == "]":
        grid = move_box((nextpos[0], nextpos[1] - 1), nextpos, dir, grid)
        pos, grid = move2(pos, dir, grid)
    elif grid[nextpos[0]][nextpos[1]] == "#":
        return pos, grid
    elif grid[nextpos[0]][nextpos[1]] == ".":
        grid[pos[0]][pos[1]] = "."
        grid[nextpos[0]][nextpos[1]] = "@"
        pos = nextpos
    return pos, grid


def agg_result2(grid):
    return sum(
        [
            y * 100 + x
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell == "["
        ]
    )


def part2(data=None):
    grid, seq = parse_data(data)
    expander = {"#": ["#", "#"], ".": [".", "."], "@": ["@", "."], "O": ["[", "]"]}
    newgrid = []
    for row in grid:
        newrow = []
        for col in row:
            newrow += expander[col]
        newgrid.append(newrow)
    dirs = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    pos = [
        (r, c)
        for r, row in enumerate(newgrid)
        for c, cell in enumerate(row)
        if cell == "@"
    ][0]
    print_grid(newgrid)
    for dir in seq:
        try:
            pos, newgrid_ = move2(pos, dirs[dir], deepcopy(newgrid))
            newgrid = newgrid_
        except RecursionError:
            pass
        # print(dir)
        # print_grid(newgrid)
        # continue
    print_grid(newgrid)
    result = agg_result2(newgrid)
    return result


# %%
# print(
#     "found:",
#     part2(
#         "#######\n#...#.#\n#.....#\n#..OO@#\n#..O..#\n#.....#\n#######\n\n<vv<<^^<<^^"
#     ),
# )
# print("answer:", "dunno")
# print("found:", part2(puz.examples[0].input_data))
# print("answer:", 9021)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
