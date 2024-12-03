# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=2)
puz.view()


# %%
def parse_data(data: str):
    return [[int(x) for x in line.split()] for line in data.split("\n")]


def part1(data=None):
    input = parse_data(data)
    result = []
    for r in input:
        _sorted = list(sorted(r))
        sort_f = _sorted == r
        if not sort_f:
            sort_r = _sorted[::-1] == r
        ediff = np.abs(np.ediff1d(np.array(r)))
        grad = min(ediff) >= 1 and max(ediff) <= 3
        val = (sort_f or sort_r) and grad
        result.append(val)
    result = sum(result)
    return result


def part2(data=None):
    input = parse_data(data)
    result = []
    for _, r in enumerate(input):
        ediff = np.ediff1d(np.array(r))
        sort_ = np.all(ediff > 0) or np.all(ediff < 0)
        grad = max(np.abs(ediff)) <= 3
        val = sort_ and grad
        if not val:
            for i in range(len(r)):
                r_ = r.copy()
                r_.pop(i)
                ediff = np.ediff1d(np.array(r_))
                sort_ = np.all(ediff > 0) or np.all(ediff < 0)
                grad = max(np.abs(ediff)) <= 3
                val = sort_ and grad
                if val:
                    break
        result.append(val)
    result = sum(result)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_b)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
