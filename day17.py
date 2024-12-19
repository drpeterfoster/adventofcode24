# %%
import re
import numpy as np
import pandas as pd
from aocd.models import Puzzle


# %%
puz = Puzzle(year=2024, day=17)
# puz.view()


# %%
def parse_data(data: str):
    pattern = r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([\d\,]+)"
    match = re.match(pattern, data)
    return {
        "A": int(match.group(1)),
        "B": int(match.group(2)),
        "C": int(match.group(3)),
    }, list(map(int, match.group(4).split(",")))


def get_operand_value(operand, registers):
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise ValueError("Invalid operand")


def run_program(registers, program):
    output = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        if opcode == 0:  # adv
            registers["A"] //= 2 ** get_operand_value(operand, registers)
        elif opcode == 1:  # bxl
            registers["B"] ^= operand
        elif opcode == 2:  # bst
            registers["B"] = get_operand_value(operand, registers) % 8
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            registers["B"] ^= registers["C"]
        elif opcode == 5:  # out
            output.append(get_operand_value(operand, registers) % 8)
        elif opcode == 6:  # bdv
            registers["B"] = registers["A"] // 2 ** get_operand_value(operand, registers)
        elif opcode == 7:  # cdv
            registers["C"] = registers["A"] // 2 ** get_operand_value(operand, registers)
        else:
            raise ValueError("Invalid opcode")
        ip += 2
    return output


def part1(data=None):
    registers, program = parse_data(data)
    result = run_program(registers, program)
    return ",".join(map(str, result))


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa


# %%
# you sneaky buggers...
def oneliner(o):
    registers, program = parse_data(puz.input_data)
    registers["A"] = vali = int(o, 8)
    result = run_program(registers, program)
    print(vali, o)
    print(result)
    print(program[-len(result) :])


def part2(data=None):
    registers, program = parse_data(data)
    stems = ["0o"]
    vals_checked = set()
    while True:
        newstems = []
        for stem in stems:
            for i in range(8):
                valo = stem + str(i)
                vali = int(valo, 8)
                if vali not in vals_checked:
                    vals_checked.add(vali)
                    reg = {k: v for k, v in registers.items()}
                    reg["A"] = vali
                    result = run_program(reg, program)
                    if result == program[-len(result) :]:
                        newstems.append(valo)
        stems = newstems
        if len(result) == len(program):
            break
    result = min([int(x, 8) for x in stems])
    return result


# %%
EX2 = "Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,3,5,4,3,0"
print("found:", part2(EX2))
print("answer:", 117440)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
