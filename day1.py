# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


def tester(func, example):
    assert func(example.input_data) == (example.answer_a if example.answer_a is not None else example.answer_b)
    print("tests pass")
    return True


# %%
puz = Puzzle(year=2024, day=1)
puz.view()
print(puz.input_data)


# %%
def parse_data(data):
    pass


def part1(data=None):
    result = None
    print(result)
    return result


def part2(data=None):
    result = None
    print(result)
    return result


# %%
if tester(part1, puz.examples[0]):
    resa = part1(puz.input_data)
    print(f"solution: {resa}")
    puz.answer_a = resa

# %%
if tester(part2, puz.examples[1]):
    resb = part2(puz.input_data)
    print(f"solution: {resb}")
    puz.answer_b = resb
