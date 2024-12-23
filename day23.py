# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from tqdm import tqdm

# %%
puz = Puzzle(year=2024, day=23)
puz.view()


# %%
from itertools import combinations

def parse_data(data):
    connections = [line.split('-') for line in data.splitlines()]
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph

def part1(data=None):
    graph = parse_data(data)
    triplets = []
    ttriplets = []
    nodes = list(graph.keys())
    for a, b, c in combinations(nodes, 3):
        if b in graph[a] and c in graph[a] and c in graph[b]:
            triplets.append({a, b, c})
            if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                ttriplets.append({a, b, c})
    print("all triplest:", len(triplets))
    return len(ttriplets)


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 7)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
def is_clique(graph, nodes):
    for a, b in combinations(nodes, 2):
        if b not in graph[a]:
            return False
    return True

def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(R)
        return
    for v in P.copy():
        bron_kerbosch(R | {v}, P & graph[v], X & graph[v], graph, cliques)
        P.remove(v)
        X.add(v)

def find_largest_clique(graph):
    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, cliques)
    max_clique = max(cliques, key=len)
    return max_clique

def part2(data=None):
    graph = parse_data(data)
    result = find_largest_clique(graph)
    return ",".join(sorted(result))


# %%
print("found:", part2(puz.examples[0].input_data))
print("answer:", "co,de,ka,ta")
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
