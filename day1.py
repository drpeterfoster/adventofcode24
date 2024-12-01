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
    list1 = []
    list2 = []

    lines = data.strip().split("\n")
    for line in lines:
        num1, num2 = map(int, line.split())
        list1.append(num1)
        list2.append(num2)

    return list1, list2


def part1(data=None):
    a, b = parse_data(data)
    a = list(sorted(a))
    b = list(sorted(b))
    result = 0
    for a, b in zip(a, b):
        result += abs(a - b)
    print(result)
    return result


def part2(data=None):
    a, b = parse_data(data)
    result = 0
    for x in a:
        result += x * len([y for y in b if y == x])
    print(result)
    return result


# %%
print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
print("answer:", puz.examples[0].answer_b)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
