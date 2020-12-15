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


def test_3():
    mask_string = "000000000000000000000000000000X1001X"
    address_value = 42
    assert sorted(part2_apply_address_mask(mask_string, address_value)) == [
        26,
        27,
        58,
        59,
    ]


def test_4():
    mask_string = "00000000000000000000000000000000X0XX"
    address_value = 26
    assert sorted(part2_apply_address_mask(mask_string, address_value)) == [
        16,
        17,
        18,
        19,
        24,
        25,
        26,
        27,
    ]


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
    return int("".join(b_val), 2)


def part2_apply_address_mask(mask_string: str, address_value: int) -> list:

    mask = list(mask_string)
    mask_idx_map = {}
    float_number = 0
    for i, c in enumerate(mask[::-1]):
        if c == "X":
            mask_idx_map[float_number] = len(mask) - 1 - i
            float_number += 1

    address_binary_str = bin(address_value)[2:]
    # pad to 36 bits
    address_binary_str = f"{address_binary_str:0>36}"

    n_different_addresses = mask.count("X") ** 2

    addresses = []
    for iaddress in range(n_different_addresses):
        b_address = bin(iaddress)[2:]
        b_address = f"{b_address:0>36}"

        float_number = 0
        new_address = list(address_binary_str)

        # floating indices
        for float_index, is_set in enumerate(list(b_address)[::-1]):
            if float_index not in mask_idx_map:
                break
            if is_set == "1":
                new_address[mask_idx_map[float_index]] = "1"
            else:
                new_address[mask_idx_map[float_index]] = "0"

        # apply the other rules
        for imask, mask_val in enumerate(mask):
            if mask_val == "1":
                new_address[imask] = "1"

        addresses.append("".join(new_address))
    addresses = [int(x, 2) for x in addresses]
    addresses = list(set(addresses))
    return addresses


def main(input_path):

    # mask_string = "00000000000000000000000000000000X0XX"
    # address_value = 26
    # anew =  part2_apply_address_mask(mask_string, address_value)
    # for i, a in enumerate(anew) :
    #    print(f"[{i}] {a}")
    # sys.exit()

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

    # part 2
    memory = {}
    mask_string = ""
    with open(input_path, "r") as ifile:
        for line in ifile:
            line = line.strip()
            if "mask" in line:
                mask_string = line.split("=")[1].strip()
                continue
            memory_location, memory_value = [x.strip() for x in line.split("=")]
            memory_location = int(memory_location.replace("mem[", "").replace("]", ""))

            addresses_after_masking = part2_apply_address_mask(
                mask_string, memory_location
            )
            # now update with the value to be written all of the post-masked addresses
            for address in addresses_after_masking:
                # memory[address] = apply_mask(mask_string, int(memory_value, 10))
                memory[address] = int(memory_value, 10)

    sum_nonzero = sum(memory.values())
    print(f"PART 2: Sum of nonzero memory locations: {sum_nonzero}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #14")
    parser.add_argument("input", help="Day #14 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
