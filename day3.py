# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=3)
puz.view()


# %%
def parse_data(data: str):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = [[int(x), int(y)] for x, y in re.findall(pattern, data)]
    return matches


def extract_patterns(data: str):
    patterns = [r"mul\(\d{1,3},\d{1,3}\)", r"do\(\)", r"don\'t\(\)"]

    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, data):
            matches.append((match.start(), match.group()))

    # Sort matches by their position in the string
    matches.sort(key=lambda x: x[0])

    # Extract the matched strings
    results = [match[1] for match in matches]
    return results


def part1(data=None):
    input = parse_data(data)
    result = sum([x * y for x, y in input])
    return result


def part2(data=None):
    input = extract_patterns(data)
    result = 0
    active = True
    for val in input:
        if val == "do()":
            active = True
            continue
        if val == "don't()":
            active = False
            continue
        if active:
            x, y = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", val)[0]
            result += int(x) * int(y)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
print("found:", part2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"))
print("answer:", 48)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
