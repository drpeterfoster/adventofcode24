# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=24)
# puz.view()


# %%
def parse_data(data: str):
    initial_txt, graph_txt = data.strip().split("\n\n")
    initial_states = {}
    for state in initial_txt.split("\n"):
        node, val = state.split(": ")
        initial_states[node] = val == "1"
    graph = []
    for line in graph_txt.split("\n"):
        i1, op, i2, _, o1 = line.split()
        i1_val, i2_val = None, None
        if i1 in initial_states:
            i1_val = initial_states[i1]
        if i2 in initial_states:
            i2_val = initial_states[i2]
        graph.append(
            dict(
                input={i1: i1_val, i2: i2_val}, op=op, output_node=o1, output_value=None
            )
        )
    return graph, initial_states


def part1(data=None):
    graph, _ = parse_data(data)
    return graph_solver(graph)

def graph_solver(graph):
    unresolved = set([node["output_node"] for node in graph])
    while unresolved:
        for node in graph:
            a, b = list(node["input"].values())
            if a is not None and b is not None and node["output_value"] is None:
                if node["op"] == "AND":
                    node["output_value"] = a & b
                elif node["op"] == "OR":
                    node["output_value"] = a | b
                elif node["op"] == "XOR":
                    node["output_value"] = a != b
                for n in graph:
                    if node["output_node"] in n["input"]:
                        n["input"][node["output_node"]] = node["output_value"]
                unresolved.remove(node["output_node"])
    _, zb = list(
        zip(
            *list(
                sorted(
                    [
                        (node["output_node"], node["output_value"])
                        for node in graph
                        if node["output_node"].startswith("z")
                    ],
                    reverse=True,
                )
            )
        )
    )
    binary = "".join(map(str, map(int, zb)))
    return int(binary, 2), binary


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", 4)
resa, resabin = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# %%
def part2(data=None):
    graph, istates = parse_data(data)
    fixes = [
        (("tff", "rrr", "z11"), ("hkc", "tdd", "sps")),
        (("x05", "y05", "z05"), ("pvb", "vtn", "tst")),
        (("x38", "y38", "pmd"), ("x38", "y38", "cgh")),
        (("pjg", "kmg", "frt"), ("pjg", "kmg", "z23")),
    ]
    graph = fixit(graph, fixes)
    resint, resbin = graph_solver(graph)
    xvals, yvals = [], []
    for node, val in sorted(istates.items()):
        if node.startswith("x"):
            xvals.append(val)
        elif node.startswith("y"):
            yvals.append(val)
    xbit = "".join(map(str, map(int, xvals[::-1])))
    ybit = "".join(map(str, map(int, yvals[::-1])))
    xval, yval = int(xbit, 2), int(ybit, 2)
    zval = xval + yval
    zbit = bin(zval)[2:].zfill(len(xbit))
    # print(xbit, ybit, zbit)
    # print(xval, yval, zval)
    print("target:", zbit)
    print(" found:", resbin)
    assert zbit == resbin
    result = []
    for fix in fixes:
        result += [fix[0][2], fix[1][2]]
    return ",".join(sorted(result))

# %%
print("found:", part2(puz.input_data))
# print("answer:", puz.examples[0].answer_b)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(edges, edge_labels={}):
    # Create a graph
    G = nx.Graph()

    # Add edges to the graph
    G.add_edges_from(edges)

    # Define positions for nodes
    pos = {}
    x_nodes = sorted([node for node in G.nodes if node.startswith('x')])
    y_nodes = sorted([node for node in G.nodes if node.startswith('y')])
    z_nodes = sorted([node for node in G.nodes if node.startswith('z')])

    for i, node in enumerate(x_nodes):
        pos[node] = (i*2, 1)
    for i, node in enumerate(y_nodes):
        pos[node] = (i*2 + .75, 1.25)
    for i, node in enumerate(z_nodes):
        pos[node] = (i*2 + 1, -1)


    # Define positions for nodes connected to both x and z nodes
    xz_connected_nodes = []
    for x_node in x_nodes:
        connected_nodes = [n for n in G.neighbors(x_node) if n not in pos and any(m in z_nodes for m in G.neighbors(n))]
        xz_connected_nodes.extend(sorted(connected_nodes))
        for j, node in enumerate(connected_nodes):
            pos[node] = (x_nodes.index(x_node)*2, 0.25)
    
    # Define positions for nodes connected to both y and z nodes
    yz_connected_nodes = []
    for y_node in y_nodes:
        connected_nodes = [n for n in G.neighbors(y_node) if n not in pos and any(m in z_nodes for m in G.neighbors(n))]
        yz_connected_nodes.extend(sorted(connected_nodes))
        for j, node in enumerate(connected_nodes):
            pos[node] = (y_nodes.index(y_node)*2+.15, 0.5)

    # Define positions for nodes connected to both x and y nodes
    xy_connected_nodes = []
    for x_node in x_nodes:
        connected_nodes = [n for n in G.neighbors(x_node) if n not in pos and any(m in y_nodes for m in G.neighbors(n))]
        xy_connected_nodes.extend(sorted(connected_nodes))
        for j, node in enumerate(connected_nodes):
            pos[node] = (x_nodes.index(x_node)*2+.75, 0.75)
    
    # Define positions for nodes connected to z and not in pos
    z_connected_nodes = []
    for z_node in z_nodes:
        connected_nodes = [n for n in G.neighbors(z_node) if n not in pos]
        z_connected_nodes.extend(sorted(connected_nodes))
        for j, node in enumerate(connected_nodes):
            pos[node] = (z_nodes.index(z_node)*2, -0.75)

    # Force-directed layout for other nodes
    other_nodes = [node for node in G.nodes if node not in pos]
    fixed_nodes = x_nodes + y_nodes + z_nodes + xz_connected_nodes + yz_connected_nodes + xy_connected_nodes + z_connected_nodes
    pos.update(nx.spring_layout(G.subgraph(other_nodes + fixed_nodes), pos=pos, fixed=fixed_nodes, k=.0001))

    # Draw the graph
    plt.figure(dpi=300, figsize=(40, 6))  # Set the figure size to be much wider
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=50, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=6)

    plt.show()
    
graph, _ = parse_data(puz.input_data)
edges = [(n, node["output_node"]) for node in graph for n in node["input"]]
visualize_graph(edges)

# %%
def fixit(graph, fixes):
    for ((n11,n12,o1), (n21,n22,o2)) in fixes:
        a, b = [node for node in graph if (n11 in node["input"] and n12 in node["input"] and o1 in node['output_node']) or (n21 in node["input"] and n22 in node["input"] and o2 in node['output_node'])]
        aout, bout = a["output_node"], b["output_node"]
        a["output_node"], b["output_node"] = bout, aout
    return graph
# %%
graph, _ = parse_data(puz.input_data)
fixes = [
        (("tff", "rrr", "z11"), ("hkc", "tdd", "sps")),
        (("x05", "y05", "z05"), ("pvb", "vtn", "tst")),
        (("x38", "y38", "pmd"), ("x38", "y38", "cgh")),
        (("pjg", "kmg", "frt"), ("pjg", "kmg", "z23")),
    ]
graph = fixit(graph, fixes)
edges = [(n, node["output_node"]) for node in graph for n in node["input"]]
edge_labels = {(n, node["output_node"]): node['op'] for node in graph for n in node["input"]}
visualize_graph(edges, edge_labels)


# %%
