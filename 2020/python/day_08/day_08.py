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
        if self.sp >= len(self.program):
            print(f"ERROR: Stack overflow at SP = {self.sp}")
            sys.exit(1)

        if not self.started:
            self.started = True
            return

        at_end_of_program = self.sp == len(self.program) - 1

        instruction, action = self.program[self.sp]
        self.previous_sp = self.sp
        self.previous_accumulator = self.accumulator
        self.previous_counts = self.counts
        if instruction == "acc":
            self.accumulator += action

            if at_end_of_program:
                self.finished = True
                raise StopIteration

            # advance the program
            self.counts[self.sp] += 1
            self.sp += 1

        elif instruction == "jmp":
            self.counts[self.sp] += 1
            self.sp += action
            if self.sp >= len(self.program):
                print(
                    f"ERROR: JUMP instruction overflows stack at SP = {self.sp - action}"
                )
                sys.exit(1)
        elif instruction == "nop":
            if at_end_of_program:
                return False
            self.counts[self.sp] += 1
            self.sp += 1
        else:
            print("ERROR: Bad stack!")
            sys.exit(1)
        return True

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
        print(f"Loaded program with {len(self.program)} instructions")


def main(input_path):

    with open(input_path, "r") as ifile:
        program_lines = [line.strip() for line in ifile.readlines() if line != ""]
    program = Program(program_lines)

    # part 1
    # iterate through the program until we hit a repeated instruction
    for _ in program:
        if program.counts[program.sp] >= 1:
            break
    print(
        f"PART 1: Accumulator immediately before any repeated instruction = {program.accumulator}"
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #8")
    parser.add_argument("input", help="Day #8 input file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
