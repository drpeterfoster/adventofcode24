# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=7)
puz.view()


# %%
def parse_data(data: str):
    eqs = [[int(x.split(": ")[0]), list(map(int, x.split(": ")[1].split()))] for x in data.split("\n")]
    return eqs


from itertools import product


def part1(data=None):
    eqs = parse_data(data)
    operators = [np.add, np.multiply]
    result = 0
    for tot, vals in eqs:
        n_ops = len(vals) - 1
        for ops in product(operators, repeat=n_ops):
            res = vals[0]
            for i in range(n_ops):
                res = ops[i](res, vals[i + 1])
            if res == tot:
                result += tot
                break
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=7)


def concat_digits(a, b):
    return int(str(a) + str(b))


def part2(data=None):
    eqs = parse_data(data)
    operators = [np.add, np.multiply, concat_digits]
    result = 0
    for tot, vals in eqs:
        n_ops = len(vals) - 1
        for ops in product(operators[:-1], repeat=n_ops):
            res = vals[0]
            for i in range(n_ops):
                res = ops[i](res, vals[i + 1])
            if res == tot:
                result += tot
                break
        if res != tot:
            for ops in product(operators, repeat=n_ops):
                res = vals[0]
                for i in range(n_ops):
                    res = ops[i](res, vals[i + 1])
                if res == tot:
                    result += tot
                    break
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 11387)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = resb

# %%
