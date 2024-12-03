# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=1)
puz.view()


# %%
def parse_data(data: str):
    pass


def part1(data=None):
    x = parse_data(data)
    result = 0
    print(result)
    return result


def part2(data=None):
    x = parse_data(data)
    result = 0
    print(result)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_b)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
