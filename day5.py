# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=5)
puz.view()


# %%
def parse_data(data: str):
    orders, updates = data.split("\n\n")
    orders = [tuple(x.split("|")) for x in orders.split("\n")]
    updates = [x.split(",") for x in updates.split("\n")]
    return orders, updates


def part1(data=None):
    orders, updates = parse_data(data)
    valid_updates = []
    for update in updates:
        orders_ = [x for x in orders if x[0] in update and x[1] in update]
        valid = True
        for order in orders_:
            if update.index(order[1]) < update.index(order[0]):
                valid = False
                break
        if valid:
            valid_updates.append(update)
    result = sum(list(map(int, [x[len(x) // 2] for x in valid_updates])))
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa
# %%
puz = Puzzle(year=2024, day=5)


from functools import cmp_to_key


def compare(x, y, order_dict):
    if x == y:
        return 0
    if (x, y) in order_dict:
        return -1
    if (y, x) in order_dict:
        return 1
    return 0


def reorder_list(strings, pairs):
    order_dict = set(pairs)
    sorted_strings = sorted(strings, key=cmp_to_key(lambda x, y: compare(x, y, order_dict)))
    return sorted_strings


def part2(data=None):
    orders, updates = parse_data(data)
    valid_updates = []
    for update in updates:
        orders_ = [x for x in orders if x[0] in update and x[1] in update]
        valid = True
        for order in orders_:
            if update.index(order[1]) < update.index(order[0]):
                valid = False
                break
        if not valid:
            fixedit = reorder_list(update, orders)
            valid_updates.append(fixedit)
    result = sum(list(map(int, [x[len(x) // 2] for x in valid_updates])))
    return result


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", 123)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
