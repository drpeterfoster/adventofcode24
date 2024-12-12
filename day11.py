# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from tqdm import tqdm
from functools import lru_cache


# %%
puz = Puzzle(year=2024, day=11)
# puz.view()


# %%
def parse_data(data: str):
    return list(map(int, data.strip().split()))


@lru_cache(maxsize=None)
def rules(val):
    if val == 0:
        return [1]
    if len(str(val)) % 2 == 0:
        x = len(str(val)) // 2
        return [int(str(val)[:x]), int(str(val)[x:])]
    return [val * 2024]


def part1(data, blinks):
    stones = parse_data(data)
    for _ in tqdm(range(blinks)):
        new_stones = []
        for stone in stones:
            new_stones += rules(stone)
        stones = new_stones
    return len(stones)


# %%
# print("found:", part1("125 17", 25))
# print("answer:", 55312)
# resa = part1(puz.input_data, 25)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
from collections import defaultdict


def part1_mini(stones, blinks):
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            new_stones += rules(stone)
        stones = new_stones
    return stones


@lru_cache(maxsize=None)
def rules_25(val):
    res = part1_mini([val], 25)
    return res, len(res)


def part2(data):
    stones = parse_data(data)
    print("wave 1...")
    new_stones = []
    for stone in tqdm(stones):
        new_stones_, _ = rules_25(stone)
        new_stones += new_stones_
    stones = new_stones
    a, b = np.unique(stones, return_counts=True)
    stones2count1 = dict(zip(a.tolist(), b.tolist()))
    print("wave 2...")
    stones2count2 = defaultdict(int)
    for stone, count in tqdm(list(stones2count1.items())):
        new_stones, n_stones = rules_25(stone)
        for s in new_stones:
            stones2count2[s] += count
    print("wave 3...")
    stones2count3 = defaultdict(int)
    for stone, count in tqdm(list(stones2count2.items())):
        new_stones, n_stones = rules_25(stone)
        for s in new_stones:
            stones2count3[s] += count
    total_stones = sum(stones2count3.values())
    return total_stones


# %%
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
