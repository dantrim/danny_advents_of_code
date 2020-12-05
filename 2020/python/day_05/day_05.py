#!/bin/env python

#
# Advent of Code 2020
# Day 05
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path


def test_example_part1_0():
    assert compute_seat_id("FBFBBFFRLR") == 357


def test_example_part1_1():
    assert compute_seat_id("BFFFBBFRRR") == 567


def test_example_part1_2():
    assert compute_seat_id("FFFBBBFRRR") == 119


def test_example_part1_3():
    assert compute_seat_id("BBFFBBFRLL") == 820


def compute_new_bounds(direction: str, in_lo: int, in_hi: int) -> tuple:

    valid_characters = ["B", "F", "L", "R"]
    if direction not in valid_characters:
        print(
            f"ERROR: Direction character is invalid: got {direction}, expect one of {valid_characters}"
        )
        sys.exit(1)

    is_lower = direction == "F" or direction == "L"
    delta = abs(in_hi - in_lo)
    if delta == 1 and not is_lower:
        return in_hi, in_hi
    elif delta == 1 and is_lower:
        return in_lo, in_lo

    if not is_lower:
        return int(int(in_hi + 1 - in_lo) / 2 + in_lo), int(in_hi)
    else:
        hi = (int(in_hi - in_lo) + 1) / 2 - 1 + in_lo
        lo = in_lo
        return int(lo), int(hi)


def find_unique_axis(direction_list: list, starting_lo: int, starting_hi: int) -> int:

    current_lo = starting_lo
    current_hi = starting_hi
    for idirection, direction in enumerate(direction_list):
        if idirection > len(direction_list) - 1:
            break
        current_lo, current_hi = compute_new_bounds(direction, current_lo, current_hi)
    if current_lo != current_hi:
        print("ERROR: Did not find unique axis (col/row)!")
        sys.exit(1)
    return current_lo


def seat_from_barcode(seat_barcode: str) -> list:

    if len(seat_barcode) != 10:
        print(f"ERROR: Invalid seat barcode provided: {seat_barcode}")
        sys.exit(1)
    final_row = find_unique_axis(list(seat_barcode)[:7], 0, 127)
    final_col = find_unique_axis(list(seat_barcode)[7:], 0, 7)
    return final_row, final_col


def compute_seat_id(seat_barcode: str) -> int:
    row, col = seat_from_barcode(seat_barcode)
    # seat id is (row * 8) + col
    seat_id = (row * 8) + col
    return seat_id


def main(input_path):

    # part1
    # find the highest seat id in from the list of seat barcodes provided in the input
    maximum_seat_id = 0
    seat_ids = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            seat_id = compute_seat_id(line)
            maximum_seat_id = max([maximum_seat_id, seat_id])
            seat_ids.append(seat_id)
    print(f"PART 1: Number of seat barcodes scanned : {len(seat_ids)}")
    print(f"PART 1: maximum seat ID found           : {maximum_seat_id}")

    # part 2
    # the missing boarding pass is the only one missing within the bounds of the seat ids
    # (the seat ids are just the linearized (col,row) addresses of the seats)
    missing_seats = sorted(set(range(min(seat_ids), max(seat_ids))) - set(seat_ids))
    if len(missing_seats) != 1:
        print("ERROR: Found an unexpected number of missing seats: {missing_seats}")
        sys.exit(1)
    print(
        f"PART 2: Missing boarding pass has seat id : {missing_seats[0]}, at (row,col)=({missing_seats[0]//8},{missing_seats[0]%8})"
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #5")
    parser.add_argument("input", help="Day #5 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
