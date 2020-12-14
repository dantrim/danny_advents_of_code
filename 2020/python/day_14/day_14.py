#!/bin/env python

#
# Advent of Code 2020
# Day 14
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path


def test_0():
    mask_string = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    memory_value = 11
    assert apply_mask(mask_string, memory_value) == 73


def test_1():
    mask_string = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    memory_value = 101
    assert apply_mask(mask_string, memory_value) == 101


def test_2():
    mask_string = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    memory_value = 0
    assert apply_mask(mask_string, memory_value) == 64


def apply_mask(mask_string: str, memory_val: int) -> int:

    """
    Sets the active positions in the bit mask in the bit-representation
    of `memory_val` to the value in the input mask string.
    """

    mask = "".join([{"1": "1", "0": "0", "X": "0"}[x] for x in list(mask_string)])
    mask_index = "".join([{"1": "1", "0": "1", "X": "0"}[x] for x in list(mask_string)])

    b_val = bin(memory_val)[2:]
    # pad to 36 bits
    b_val = f"{b_val:0>36}"
    b_val = list(b_val)

    for mask_pos, pos_is_set in enumerate(mask_index):
        for mask_pos, pos_is_set in enumerate(mask_index):
            if pos_is_set == "1":
                b_val[mask_pos] = mask[mask_pos]
    b_val = "".join(b_val)
    return int(b_val, 2)


def main(input_path):

    # part 1
    memory = {}
    mask_string = ""
    with open(input_path, "r") as ifile:
        for line in ifile:
            line = line.strip()
            if "mask" in line:
                mask_string = line.split("=")[1].strip()
                continue
            memory_location, memory_value = [x.strip() for x in line.split("=")]
            memory_value = int(memory_value, 10)
            memory[memory_location] = apply_mask(mask_string, memory_value)
    sum_nonzero = sum(
        memory.values()
    )  # by definition our memory dict holds the (potentially) nonzero memories
    # for memory_location, memory_value in memory.items() :
    print(f"PART 1: Sum of nonzero memory locations: {sum_nonzero}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #14")
    parser.add_argument("input", help="Day #14 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
