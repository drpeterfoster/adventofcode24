# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=22)
puz.view()


# %%
def parse_data(data: str):
    return list(map(int, data.splitlines()))


def part1(data=None, steps=2000):
    starts = parse_data(data)
    results = []
    for start in starts:
        x = start
        for _ in range(steps):
            x = ((x * 64) ^ x) % 16777216
            x = ((x // 32) ^ x) % 16777216
            x = ((x * 2048) ^ x) % 16777216
            # print(x)
        results.append(x)
    result = sum(results)
    return result


# %%
# print("found:", part1("123", 10))
print("found:", part1("1\n10\n100\n2024"))
print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
def part2(data=None, steps=2000):
    starts = parse_data(data)
    results = []
    for start in starts:
        codes = {}
        x = start
        prices = [None,None,None,int(str(x)[-1])]
        diffs = [None,None,None,None]
        for _ in range(steps):
            x = ((x * 64) ^ x) % 16777216
            x = ((x // 32) ^ x) % 16777216
            x = ((x * 2048) ^ x) % 16777216
            prices.pop(0)
            prices.append(int(str(x)[-1]))
            diffs.pop(0)
            diffs.append(prices[-1] - prices[-2])
            if None not in diffs and tuple(diffs) not in codes:
                codes[tuple(diffs)] = int(str(x)[-1])
        results.append(codes)
    scores = {code: 0 for codes in results for code in codes.keys()}
    for codes in results:
        for code, score in codes.items():
            scores[code] += score
    result = max(scores.values())
    for code, score in scores.items():
        if score == result:
            print("found seq:", ",".join(map(str,code)))
            break
    return result


# %%
# print("found:", part2("123"))
print("found:", part2("1\n2\n3\n2024"))
print("target seq:", "-2,1,-1,3")
print("answer:", 23)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
