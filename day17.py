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
            output.append(str(get_operand_value(operand, registers) % 8))
        elif opcode == 6:  # bdv
            registers["B"] = registers["A"] // 2 ** get_operand_value(operand, registers)
        elif opcode == 7:  # cdv
            registers["C"] = registers["A"] // 2 ** get_operand_value(operand, registers)
        else:
            raise ValueError("Invalid opcode")
        ip += 2
    return ",".join(output)


def part1(data=None):
    registers, program = parse_data(data)
    result = run_program(registers, program)
    return result


# %%
print("found:", part1(puz.examples[0].input_data))
print("answer:", puz.examples[0].answer_a)
resa = part1(puz.input_data)
print(f"solution: {resa}")
# puz.answer_a = resa

# %%
puz = Puzzle(year=2024, day=17)


def run_symbolic_program(registers, program):
    registers["A"] = "a"  # Set A to symbolic variable 'a'
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        if opcode == 0:  # adv
            registers["A"] = f"({registers['A']}) // 2 ** {get_operand_value(operand, registers)}"
        elif opcode == 1:  # bxl
            registers["B"] ^= operand
        elif opcode == 2:  # bst
            registers["B"] = f"{get_operand_value(operand, registers)} % 8"
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            registers["B"] ^= registers["C"]
        elif opcode == 5:  # out
            # No change needed for output
            pass
        elif opcode == 6:  # bdv
            registers["B"] = f"({registers['A']}) // 2 ** {get_operand_value(operand, registers)}"
        elif opcode == 7:  # cdv
            registers["C"] = f"({registers['A']}) // 2 ** {get_operand_value(operand, registers)}"
        else:
            raise ValueError("Invalid opcode")
        ip += 2
    return registers


def reverse_engineer(registers, program):
    symbolic_registers = run_symbolic_program(registers.copy(), program)
    # Here you would solve the symbolic equation for 'a' to match the desired output
    # This is a placeholder for the actual symbolic solving logic
    return symbolic_registers


def part2(data=None):
    registers, program = parse_data(data)
    result = reverse_engineer(registers, program)
    return result


# %%
EX2 = "Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,3,5,4,3,0"
print("found:", part2(EX2))
print("answer:", 117440)
resb = part2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb

# %%
