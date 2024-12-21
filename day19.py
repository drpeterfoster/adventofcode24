# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from tqdm import tqdm


# %%
puz = Puzzle(year=2024, day=19)
# puz.view()


# %%
def parse_data(data: str):
    towels, patterns = data.strip().split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.split("\n")
    return towels, patterns


# %%
# recursive DFS
from collections import defaultdict
from functools import lru_cache


def find_combinations(substrings, target):
    @lru_cache(None)
    def backtrack(start):
        if start == len(target):
            return True
        for substring in substrings.get(target[start], []):
            if target.startswith(substring, start):
                out = backtrack(start + len(substring))
                if out:
                    return True
        return False

    result = backtrack(0)
    return result


def index_towels(towels, pattern):
    towels_ = [t for t in towels if t in pattern]
    i2t = defaultdict(list)
    for t in towels_:
        i2t[t[0]].append(t)
    return i2t


def part1(data=None):
    towels, patterns = parse_data(data)
    result = 0
    for pattern in patterns:
        towels_ = index_towels(towels, pattern)
        makeable = find_combinations(towels_, pattern)
        if makeable:
            result += 1
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
def find_combinations2(substrings, target):
    @lru_cache(None)
    def backtrack(target):
        cando = 0
        if target == "":
            return 1
        for substring in substrings.get(target[0], []):
            if target.startswith(substring):
                cando += backtrack(target[len(substring) :])
        return cando

    result = backtrack(target)
    return result


def part2(data=None):
    towels, patterns = parse_data(data)
    result = 0
    for pattern in patterns:
        towels_ = index_towels(towels, pattern)
        pat_result = find_combinations2(towels_, pattern)
        # print(pat_result)
        result += pat_result
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 16)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
