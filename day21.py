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
    valid_paths = [
        path for path in all_paths if is_valid_path(path) and len(path) == min_len
    ]
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
# DOESN'T WORK ON HUMAN LIFESPANS WITH AVAILABLE MEMORY
# print("found:", part1("029A\n980A\n179A\n456A\n379A\n", level=25))
# print("answer:", "NA")
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
################################
# ok, we gotta start over on this one.  ^ is NOT working.
# this time, let's try to do this more symbolically; using this cool new 
# complext number thing I just learned about to register dx/dy.
# similar to before, caching with recursion is the way to go.
# SO MUCH SIMPLER.  omg i was overthinking this so much at first.

from functools import cache

N = {'7':0, '8':1, '9':2, '4':1j, '5':1+1j, '6':2+1j, 
      '1':2j, '2':1+2j, '3':2+2j, ' ':3j, '0':1+3j, 'A':2+3j}
R = {' ':0, '^':1, 'A':2, '<':1j, 'v':1+1j, '>':2+1j}

@cache
def path(start, end):
    pad = N if (start in N and end in N) else R
    diff = pad[end] - pad[start]
    dx, dy = int(diff.real), int(diff.imag)
    yy = ("^"*-dy) + ("v"*dy)
    xx = ("<"*-dx) + (">"*dx)

    bad = pad[" "] - pad[start]
    prefer_yy_first = (dx>0 or bad==dx) and bad!=dy*1j
    return (yy+xx if prefer_yy_first else xx+yy) + "A"
    
@cache
def length(code, depth, s=0):
    if depth == 0: return len(code)
    for i, c in enumerate(code):
        s += length(path(code[i-1], c), depth-1)
    return s

def part2(data=None, levels=3):
    codes = parse_data(data)
    results = [int(code[:-1]) * length(code, levels) for code in codes]
    return sum(results)

# %%
print(" found:", part2("029A\n980A\n179A\n456A\n379A"))
print("answer:", puz.examples[0].answer_a)
print(" found:", part2("029A\n980A\n179A\n456A\n379A", 26))
# print("answer:", puz.examples[0].answer_a)
resb = part2(puz.input_data, 26)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
