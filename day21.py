# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from functools import lru_cache
from itertools import product
from tqdm import tqdm


# %%
puz = Puzzle(year=2024, day=21)
# puz.view()


# %%
def parse_data(data: str):
    return data.strip().split("\n")


KEYS = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
ARROWS = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def convert_to_coord(coord, kind):
    return KEYS[coord] if kind == "number" else ARROWS[coord]


def convert_to_arrow(path):
    arrow_code = ""
    for i in range(1, len(path)):
        r1, c1 = path[i - 1]
        r2, c2 = path[i]
        if r2 == r1 + 1:
            arrow_code += "v"
        elif r2 == r1 - 1:
            arrow_code += "^"
        elif c2 == c1 + 1:
            arrow_code += ">"
        elif c2 == c1 - 1:
            arrow_code += "<"
    return arrow_code + "A"


def coordinate_paths(start, end, kind):
    if kind == "number":
        forbidden = (3, 0)
    elif kind == "arrow":
        forbidden = (0, 0)
    else:
        raise ValueError(f"Unknown kind: {kind}")

    def is_valid_path(path):
        return forbidden not in path

    def generate_paths(start, end):
        paths = []
        queue = [(start, [start])]
        while queue:
            (current, path) = queue.pop(0)
            if current == end:
                paths.append(path)
            else:
                r, c = current
                for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    next_step = (r + dr, c + dc)
                    if (
                        min(start[0], end[0]) <= next_step[0] <= max(start[0], end[0])
                        and min(start[1], end[1])
                        <= next_step[1]
                        <= max(start[1], end[1])
                        and next_step not in path
                    ):
                        queue.append((next_step, path + [next_step]))
        return paths

    all_paths = generate_paths(start, end)
    min_len = min(len(path) for path in all_paths)
    valid_paths = [path for path in all_paths if is_valid_path(path) and len(path) == min_len]
    return valid_paths


@lru_cache(maxsize=None)
def compute_input_pair(ab, kind):
    start = convert_to_coord(ab[0], kind)
    end = convert_to_coord(ab[1], kind)
    paths = coordinate_paths(start, end, kind)
    apaths = [convert_to_arrow(path) for path in paths]
    return apaths


def compute_input(code, kind):
    codes = []
    for i in range(0, len(code) - 1):
        codes.append(compute_input_pair(code[i : i + 2], kind))
    flat_codes = ["".join(comb) for comb in product(*codes)]
    return flat_codes

    

def part1(data=None, level=2):
    def compute_robot(codes, level, best):
        if level != 0:
            level -= 1
            for code in codes:
                codes1 = compute_input("A" + code, "arrow")
                best = compute_robot(codes1, level, best)
        else:
            for code in codes:
                if best is None or len(code) < len(best):
                    best = code
        return best

    codes = parse_data(data)
    result = 0
    for code in tqdm(codes):
        codes1 = compute_input("A" + code, "number")
        best = compute_robot(codes1, level, None)
        score = len(best) * int(code[:-1])
        result += score
    return result


# %%
print(" found:", part1("029A\n980A\n179A\n456A\n379A\n"))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
print("found:", part1("029A\n980A\n179A\n456A\n379A\n", level=25))
print("answer:", "NA")
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
