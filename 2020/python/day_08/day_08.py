#!/bin/env python

#
# Advent of Code 2020
# Day 08
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest


@pytest.fixture
def example_instructions_infinite_loop():
    instructions = """
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """
    return [x.strip() for x in instructions.split("\n") if x != ""]


def test_find_main(example_instructions_infinite_loop):
    program = Program(example_instructions_infinite_loop)
    assert program.main == 1


def test_acc():
    instructions = """
    acc +1
    acc +9
    acc +10
    acc -5
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    program = Program(program_lines)
    # run the program
    [s for s in program]
    assert program.accumulator == 15


def test_jmp():
    instructions = """
    jmp +4
    acc +1
    acc +1
    acc +1
    acc +1
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    program = Program(program_lines)
    # run the program
    [s for s in program]
    assert program.accumulator == 1


def test_nop():
    instructions = """
    nop +100
    nop -49
    nop +42
    acc +1
    acc +5
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    program = Program(program_lines)
    # run the program
    [s for s in program]
    assert program.accumulator == 6


def test_detect_repeated_instruction():
    instructions = """
    nop +1
    acc +1
    acc +9
    jmp -2
    acc +42
    acc -20
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    program = Program(program_lines)
    for istep, _ in enumerate(program):
        if program.counts[program.sp] >= 1:
            break
    assert istep == 4


def test_unwind():
    instructions = """
    nop +1
    acc +1
    acc +9
    jmp -3
    acc +42
    acc -20
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    program = Program(program_lines)
    for istep, _ in enumerate(program):
        if program.counts[program.sp] >= 1:
            break
    assert True


def test_example_0(example_instructions_infinite_loop):
    program = Program(example_instructions_infinite_loop)
    for istep, _ in enumerate(program):
        if program.counts[program.sp] >= 1:
            break
    assert program.accumulator == 5


def test_corrupted_location():
    instructions = """
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    corrupted_instruction = find_corrupted_instruction(program_lines)
    assert corrupted_instruction == ["jmp", 7]


def test_corruption_fix():
    instructions = """
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """
    program_lines = [x.strip() for x in instructions.split("\n") if x != ""]
    corrupted_instruction = find_corrupted_instruction(program_lines)
    if corrupted_instruction is None:
        assert False
    pos = corrupted_instruction[1]
    program = Program(program_lines)
    new_instruction = {"jmp": "nop", "nop": "jmp"}[corrupted_instruction[0]]
    program.program[pos] = [new_instruction, program.program[pos][1]]
    for _ in program:
        pass
    assert program.finished


def find_corrupted_instruction(program_lines):

    # brute force!
    jmp_locations = []
    nop_locations = []
    program = Program(program_lines)
    for istep, instruction in enumerate(program.program):
        instruction, action = instruction
        if instruction == "jmp":
            jmp_locations.append(istep)
        elif instruction == "nop":
            nop_locations.append(istep)

    program_finished = False
    max_step = 0
    max_sp = 0
    max_sp_at = ["", 0]

    for iop, op_locations in enumerate([jmp_locations, nop_locations]):
        for location in op_locations:
            program = Program(program_lines)
            current_instruction = program.program[location]
            new_instruction = {0: "nop", 1: "jmp"}[iop]
            new_instruction = [new_instruction, current_instruction[1]]
            program.program[location] = new_instruction
            for istep, _ in enumerate(program):
                max_step = max([istep, max_step])
                if program.sp > max_sp:
                    max_sp = max([max_sp, program.sp])
                    max_sp_at = [{0: "jmp", 1: "nop"}[iop], location]
                max_sp = max([max_sp, program.sp])
                if program.counts[program.sp] >= 1:
                    break
            if program.finished:
                program_finished = True
    if program_finished:
        return max_sp_at
    else:
        return None


class Program:
    def __init__(self, program_lines):
        self.accumulator = 0
        self.main = -1
        self.sp = 0
        self.counts = []

        self.previous_sp = 0
        self.previous_accumulator = 0
        self.previous_counts = []

        self.program = []
        self.started = False
        self.finished = False
        self.load_program(program_lines)

    def unwind(self):
        self.sp = self.previous_sp
        self.accumulator = self.previous_accumulator
        self.counts = self.previous_counts

    def __str__(self):
        if self.sp >= len(self.program):
            return f"PROGRAM: SP=END, ACC={self.accumulator}, PROGRAM FINISHED: {self.finished}"
        return f"PROGRAM: SP={self.sp}, ACC={self.accumulator}, INSTR={self.program[self.sp]}, COUNTS={self.counts[self.sp]}, PROGRAM FINISHED: {self.finished}"

    def __iter__(self):
        return self

    def __next__(self):
        if not self.started:
            self.started = True
            return

        instruction, action = self.program[self.sp]
        self.previous_sp = self.sp
        self.previous_accumulator = self.accumulator
        self.previous_counts = self.counts
        if instruction == "acc":
            self.accumulator += action

            # advance the program
            self.counts[self.sp] += 1
            self.sp += 1

        elif instruction == "jmp":
            self.counts[self.sp] += 1
            self.sp += action
        elif instruction == "nop":
            self.counts[self.sp] += 1
            self.sp += 1
        else:
            print("ERROR: Bad stack!")
            sys.exit(1)

        # program termination is defined as: attempting to execute an
        # instruction immediately after the last instruction in the file.
        # what this means is this:
        #   * acc: if the last instruction is an acc, then the SP is (N-instructions + 1)
        #   * jmp: if the last instruction is jmp, with positive offset, then SP >= N-instructions
        #   * nop: if the last instruction is nop, then the SP is (N-instructions + 1)
        #
        at_end_of_program = self.sp >= len(self.program)
        if at_end_of_program:
            self.finished = True
            raise StopIteration

    def load_program(self, program_lines):
        expected_instructions = ["nop", "acc", "jmp"]
        program_line = 0
        for iline, line in enumerate(program_lines):
            line = line.strip()
            if not line:
                continue
            instruction = line.split()[0].strip()
            if instruction != "nop" and self.main < 0:
                self.main = program_line
            if instruction not in expected_instructions:
                print(f"ERROR: Unexpected instruction encountered: {instruction}")
                sys.exit(1)
            action = line.split()[1].strip()
            is_up = "+" in action
            is_down = "-" in action
            is_ok = is_up or is_down
            if not is_ok:
                print(f"ERROR: Invalid formed instruction: {line}")
                sys.exit(1)
            self.program.append([instruction, int(action)])
            self.counts.append(0)
            program_line += 1


def main(input_path):

    with open(input_path, "r") as ifile:
        program_lines = [line.strip() for line in ifile.readlines() if line != ""]
    program = Program(program_lines)

    # part 1
    # iterate through the program until we hit a repeated instruction
    for istep, _ in enumerate(program):
        if program.counts[program.sp] >= 1:
            break
    print(
        f"PART 1: Accumulator immediately before any repeated instruction = {program.accumulator}"
    )

    # part 2
    # find the location in the program that is corrupted
    corrupted_instruction = find_corrupted_instruction(program_lines)
    if corrupted_instruction is None:
        print("ERROR: Did not find a corrupted instruction in input program!")
    corrupted_instruction, corrupted_line = (
        corrupted_instruction[0],
        corrupted_instruction[1],
    )
    print(
        f'PART 2: Corrupted instruction is "{corrupted_instruction}" at program line {corrupted_line}'
    )
    program = Program(program_lines)

    # update the corrupted line
    program.program[corrupted_line] = [
        {"jmp": "nop", "nop": "jmp"}[corrupted_instruction],
        program.program[corrupted_line][1],
    ]

    # run the program (assume that the infinite loop issue is gone)
    [s for s in program]
    if not program.finished:
        print("PART 2: ERROR program did not finish!")
        sys.exit(1)
    print(f"PART 2: Program accumulator after corruption fix: {program.accumulator}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #8")
    parser.add_argument("input", help="Day #8 input file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
