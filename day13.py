# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from sympy import symbols, Eq, solve


# %%
puz = Puzzle(year=2024, day=13)
# puz.view()


# %%
def parse_data(data: str):
    pattern1 = r"Button (\w+): X[+=](\d+), Y[+=](\d+)"
    matches = re.findall(pattern1, data)
    parsed_data = {match[0]: {"X": int(match[1]), "Y": int(match[2])} for match in matches}
    pattern2 = r"Prize: X[+=](\d+), Y[+=](\d+)"
    matches = re.findall(pattern2, data)
    parsed_data["Prize"] = {"X": int(matches[0][0]), "Y": int(matches[0][1])}
    return parsed_data


def solve_equation(x, y, z):
    a, b = symbols("a b")
    equation = Eq(x * a + y * b, z)
    solutions = solve(equation, (a, b))
    valids = []
    for solution in solutions:
        for i in range(100):
            a_, b_ = solution[0].subs(b, i), solution[1].subs(b, i)
            if a_.is_integer and b_.is_integer:
                valids.append((a_, b_))
    return valids


def part1(data=None):
    machines = [parse_data(d) for d in data.split("\n\n")]
    totals = []
    for machine in machines:
        valid_x = solve_equation(machine["A"]["X"], machine["B"]["X"], machine["Prize"]["X"])
        valid_y = solve_equation(machine["A"]["Y"], machine["B"]["Y"], machine["Prize"]["Y"])
        valids = set(valid_x).intersection(valid_y)
        if valids:
            scores = [a * 3 + b * 1 for a, b in valids]
            best = min(scores)
            totals.append(best)
    result = sum(totals)
    return result


# %%
# print("found:", part1(puz.examples[0].input_data))
# print("answer:", 480)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = str(resa)

# %%
puz = Puzzle(year=2024, day=13)


def solve_equation2(x, y, z):
    a, b = symbols("a b")
    equation = Eq(x * a + y * b, z)
    solutions = solve(equation, (a, b))
    return solutions[0]


def part2(data=None):
    machines = [parse_data(d) for d in data.split("\n\n")]
    offset = 10000000000000
    totals = []
    for machine in machines:
        valid_x = solve_equation2(machine["A"]["X"], machine["B"]["X"], machine["Prize"]["X"] + offset)
        valid_y = solve_equation2(machine["A"]["Y"], machine["B"]["Y"], machine["Prize"]["Y"] + offset)
        b = symbols("b")
        B = solve(Eq(valid_x[0], valid_y[0]), b)[0]
        A = valid_x[0].subs(b, B)
        if A.is_integer and B.is_integer:
            totals.append(A * 3 + B * 1)
    result = sum(totals)
    return result


# %%
# print("found:", part2(puz.examples[0].input_data))
# print("answer:", 480)
# resb = part2(puz.input_data)
# print(f"solution: {resb}")
# puz.answer_b = str(resb)

# %%
