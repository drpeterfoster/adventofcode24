# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=25)
# puz.view()


# %%
def parse_data(data: str):
    keys, locks = [], []
    for block in data.strip().split("\n\n"):
        grid = [list(line.replace(".", "0").replace("#", "1")) for line in block.split("\n")]
        arr = np.array(grid, dtype=int)
        if arr[0, :].sum() == 0:
            keys.append(arr)
        elif arr[0, :].sum() == 5:
            locks.append(arr)
    return keys, locks


def part1(data=None):
    keys, locks = parse_data(data)
    result = 0
    for key in keys:
        for lock in locks:
            if (key + lock).max() == 1:
                result += 1
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=25)


def part2(data=None):
    input = parse_data(data)
    result = 0
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_b)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
