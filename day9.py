# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=9)
# puz.view()


# %%
from itertools import cycle


def parse_data(data: str):
    types = cycle(["file", "gap"])
    disk = []
    index = 0
    for val in data:
        type = next(types)
        if type == "file":
            disk += [index] * int(val)
            index += 1
        if type == "gap":
            disk += ["."] * int(val)
    return disk


def part1(data=None):
    disk = parse_data(data)
    while "." in disk:
        last = disk.pop(-1)
        if last == ".":
            continue
        disk[disk.index(".")] = last
    result = sum([i * val for i, val in enumerate(disk)])
    return result


# %%
# print("found:", part1(puz.examples[0].input_data))
# print("answer:", puz.examples[0].answer_a)
# resa = part1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=9)


def parse_data2(data: str):
    if len(data) % 2 == 1:
        data += "0"
    types = cycle(["file", "gap"])
    dsk, itr, spc = [], [], []
    index = 0
    for val in data:
        type = next(types)
        if type == "file":
            dsk += [index]
            itr += [int(val)]
            index += 1
        if type == "gap":
            spc += [int(val)]
    return dsk, itr, spc


def part2(data=None):
    dsk, itr, spc = parse_data2(data)
    for val in dsk.copy()[::-1]:
        i = dsk.index(val)
        space_idx = None
        for j, space in enumerate(spc[:i]):
            if space >= itr[i]:
                space_idx = j
                break
        if space_idx is None:
            continue
        dsk_, itr_, spc_ = dsk.pop(i), itr.pop(i), spc.pop(i)
        spc[space_idx] = 0
        dsk.insert(space_idx + 1, dsk_)
        itr.insert(space_idx + 1, itr_)
        spc.insert(space_idx + 1, space - itr_)
        spc[i] += itr_ + spc_
    register = 0
    result = 0
    for dsk_, itr_, spc_ in zip(dsk, itr, spc):
        for _ in range(itr_):
            result += dsk_ * register
            register += 1
        register += spc_
    return str(result)


# %%
# 0...1...2......33333
# 0...1...233333......
# 0...1...233333......
# 02..1....33333......
# 021......33333......
# 021......33333......

# print("found:", part2("1313165"))
# print("answer:", 169)
print("found:", part2(puz.examples[0].input_data))
print("answer:", 2858)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb  # wtf man, why doesn't this work?

# %%
