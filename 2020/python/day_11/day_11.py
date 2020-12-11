#!/bin/env python

#
# Advent of Code 2020
# Day 11
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest


@pytest.fixture
def example_data_part1():
    test_data = [
        """
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """,
        """
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
    """,
        """
    #.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##
    """,
        """
    #.##.L#.##
    #L###LL.L#
    L.#.#..#..
    #L##.##.L#
    #.##.LL.LL
    #.###L#.##
    ..#.#.....
    #L######L#
    #.LL###L.L
    #.#L###.##
    """,
        """
    #.#L.L#.##
    #LLL#LL.L#
    L.L.L..#..
    #LLL.##.L#
    #.LL.LL.LL
    #.LL#L#.##
    ..L.L.....
    #L#LLLL#L#
    #.LLLLLL.L
    #.#L#L#.##
    """,
        """
    #.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##
    """,
    ]
    return [[x.strip() for x in t.strip().split("\n") if x != ""] for t in test_data]


def test_round_1(example_data_part1):
    assert apply_rules(example_data_part1[0]) == [x for x in example_data_part1[1] if x]


def test_round_2(example_data_part1):
    assert apply_rules(example_data_part1[1]) == [x for x in example_data_part1[2] if x]


def test_round_3(example_data_part1):
    assert apply_rules(example_data_part1[2]) == [x for x in example_data_part1[3] if x]


def test_round_4(example_data_part1):
    assert apply_rules(example_data_part1[3]) == [x for x in example_data_part1[4] if x]


def test_round_5(example_data_part1):
    assert apply_rules(example_data_part1[4]) == [x for x in example_data_part1[5] if x]


def test_detect_stable(example_data_part1):
    n, _ = find_stable_configuration(example_data_part1[0])
    assert n == 5


def test_stable_configuration(example_data_part1):
    _, configuration = find_stable_configuration(example_data_part1[0])
    assert configuration == example_data_part1[-1]


def test_n_occupied_final(example_data_part1):
    _, configuration = find_stable_configuration(example_data_part1[0])
    assert n_occupied_seats_in_configuration(configuration) == 37


def find_stable_configuration(seats: list) -> list:

    n_passes = 0
    previous_configuration = [x for x in seats]
    current_configuration = apply_rules(seats)
    while current_configuration != previous_configuration:
        n_passes += 1
        previous_configuration = current_configuration[:]
        current_configuration = apply_rules(previous_configuration)
    return n_passes, current_configuration


def n_occupied_seats_in_configuration(seats: list) -> int:
    return sum([x.strip().count("#") for x in seats])


def n_adjacent_seats_filled(
    position: list, current_row: list, row_above: list, row_below: list
) -> int:

    col, row = position

    n_filled = 0

    # check the row above
    if row_above:
        if col > 0:
            if row_above[col - 1] == "#":
                n_filled += 1
        if row_above[col] == "#":
            n_filled += 1
        if col < (len(current_row) - 1):
            if row_above[col + 1] == "#":
                n_filled += 1

    # check the current row
    if col > 0:
        if current_row[col - 1] == "#":
            n_filled += 1
    if col < (len(current_row) - 1):
        if current_row[col + 1] == "#":
            n_filled += 1

    # chek the row below
    if row_below:
        if col > 0:
            if row_below[col - 1] == "#":
                n_filled += 1
        if row_below[col] == "#":
            n_filled += 1
        if col < (len(current_row) - 1):
            if row_below[col + 1] == "#":
                n_filled += 1

    return n_filled


def apply_rules(seats):

    input_seats = [x for x in seats]
    final_seat_configuration = []
    for irow, row in enumerate(input_seats):
        columns = list(row)

        new_seats = [x for x in columns]

        at_top = irow == 0
        at_bottom = irow == (len(seats) - 1)
        row_above, row_below = [], []
        if not at_top:
            row_above = seats[irow - 1]
        if not at_bottom:
            row_below = seats[irow + 1]

        for icol, col in enumerate(list(row)):
            current_seat = col

            # never update the floor
            if current_seat == ".":
                continue

            seat_is_empty = current_seat == "L"

            n_adjacent_filled = n_adjacent_seats_filled(
                [icol, irow], row, row_above, row_below
            )
            has_no_adjacent_seats = n_adjacent_filled == 0

            # if a seat is empty and no occupaidd seats adjacent, it becomes occupied
            if seat_is_empty and has_no_adjacent_seats:
                new_seats[icol] = "#"
            elif not seat_is_empty and n_adjacent_filled >= 4:
                new_seats[icol] = "L"

        new_seats = "".join(new_seats)
        final_seat_configuration.append(new_seats)
    return final_seat_configuration


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [
            [x.strip() for x in t.strip().split("\n") if x != ""] for t in ifile
        ]

    # part 1
    n_iterations, stable_configuration = find_stable_configuration(input_data)
    print(f"PART 1: stable configuration found in {n_iterations} iterations")
    n_occupied = n_occupied_seats_in_configuration(stable_configuration)
    print(f"PART 1: number of occupied seats in stable configuration: {n_occupied}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #11")
    parser.add_argument("input", help="Day #11 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
