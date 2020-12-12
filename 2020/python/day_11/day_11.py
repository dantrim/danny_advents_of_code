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
    assert apply_rules(example_data_part1[0], True) == [
        x for x in example_data_part1[1] if x
    ]


def test_round_2(example_data_part1):
    assert apply_rules(example_data_part1[1], True) == [
        x for x in example_data_part1[2] if x
    ]


def test_round_3(example_data_part1):
    assert apply_rules(example_data_part1[2], True) == [
        x for x in example_data_part1[3] if x
    ]


def test_round_4(example_data_part1):
    assert apply_rules(example_data_part1[3], True) == [
        x for x in example_data_part1[4] if x
    ]


def test_round_5(example_data_part1):
    assert apply_rules(example_data_part1[4], True) == [
        x for x in example_data_part1[5] if x
    ]


def test_detect_stable(example_data_part1):
    n, _ = find_stable_configuration(example_data_part1[0], True)
    assert n == 5


def test_stable_configuration(example_data_part1):
    _, configuration = find_stable_configuration(example_data_part1[0], True)
    assert configuration == example_data_part1[-1]


def test_n_occupied_final(example_data_part1):
    _, configuration = find_stable_configuration(example_data_part1[0], True)
    assert n_occupied_seats_in_configuration(configuration) == 37


@pytest.fixture
def example_data_part2():
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
    #.LL.LL.L#
    #LLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLLL.L
    #.LLLLL.L#
    """,
        """
    #.L#.##.L#
    #L#####.LL
    L.#.#..#..
    ##L#.##.##
    #.##.#L.##
    #.#####.#L
    ..#.#.....
    LLL####LL#
    #.L#####.L
    #.L####.L#
    """,
        """
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##LL.LL.L#
    L.LL.LL.L#
    #.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLL#.L
    #.L#LL#.L#
    """,
        """
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.#L.L#
    #.L####.LL
    ..#.#.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#
    """,
        """
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.LL.L#
    #.LLLL#.LL
    ..#.L.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#
    """,
    ]
    return [[x.strip() for x in t.strip().split("\n") if x != ""] for t in test_data]


def test_n_visible():
    test_data = """
    .......#.
    ...#.....
    .#.......
    .........
    ..#L....#
    ....#....
    .........
    #........
    ...#.....
    """
    test_data = [x.strip() for x in test_data.strip().split("\n") if x != ""]
    assert n_visible_seats_filled([3, 4], test_data) == 8


def test_round_1_part2(example_data_part2):
    assert apply_rules(example_data_part2[0], False) == [
        x for x in example_data_part2[1] if x
    ]


def test_round_2_part2(example_data_part2):
    assert apply_rules(example_data_part2[1], False) == [
        x for x in example_data_part2[2] if x
    ]


def test_stable_configuration_part2(example_data_part2):
    _, configuration = find_stable_configuration(example_data_part2[0], False)
    assert configuration == example_data_part2[-1]


def test_n_occupied_part2(example_data_part2):
    _, configuration = find_stable_configuration(example_data_part2[0], False)
    assert n_occupied_seats_in_configuration(configuration) == 26


def find_stable_configuration(seats: list, is_part1: bool) -> list:

    n_passes = 0
    previous_configuration = [x for x in seats]
    current_configuration = apply_rules(seats, is_part1)
    while current_configuration != previous_configuration:
        n_passes += 1
        previous_configuration = current_configuration[:]
        current_configuration = apply_rules(previous_configuration, is_part1)
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


def seat_is_at_side(col: int, row: int, seat_configuration: list) -> bool:

    n_columns = len(seat_configuration[0])
    at_left = col == 0
    at_right = col == (n_columns - 1)
    return at_left or at_right


def seat_is_bottom_or_top(col: int, row: int, seat_configuration: list) -> bool:

    n_rows = len(seat_configuration)
    at_top = row == 0
    at_bottom = row == (n_rows - 1)
    return at_top or at_bottom


def n_visible_seats_filled(position: list, seat_configuration: list) -> int:

    # just crank out each case separately, perhaps go back and remove
    # repeated logic... gotta go to work

    n_columns = len(seat_configuration[0])
    n_rows = len(seat_configuration)

    col, row = position

    at_top = row == 0
    at_bottom = row == (n_rows - 1)
    at_left = col == 0
    at_right = col == (n_columns - 1)

    n_filled = 0
    # trace left until first seat is seen
    if not at_left:
        col_to_check = col
        while True:
            col_to_check = col_to_check - 1
            seat_to_check = seat_configuration[row][col_to_check]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if col_to_check == 0:
                break

    # trace right
    if not at_right:
        col_to_check = col
        while True:
            col_to_check = col_to_check + 1
            seat_to_check = seat_configuration[row][col_to_check]
            # print(f"TRACING RIGHT: col = {col_to_check}, row = {row}: seat = {seat_to_check}")
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if col_to_check == (n_columns - 1):
                break

    # trace up
    if not at_top:
        row_to_check = row
        while True:
            row_to_check = row_to_check - 1
            seat_to_check = seat_configuration[row_to_check][col]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == 0:
                break

    # trace down
    if not at_bottom:
        row_to_check = row
        while True:
            row_to_check = row_to_check + 1
            seat_to_check = seat_configuration[row_to_check][col]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == (n_rows - 1):
                break

    # trace diagonals
    at_top_right_corner = at_top or at_right
    at_top_left_corner = at_top or at_left
    at_bottom_right_corner = at_bottom or at_right
    at_bottom_left_corner = at_bottom or at_left

    # up right
    if not at_top_right_corner:
        row_to_check = row
        col_to_check = col
        while True:
            row_to_check = row_to_check - 1
            col_to_check = col_to_check + 1
            seat_to_check = seat_configuration[row_to_check][col_to_check]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == 0 or col_to_check == (n_columns - 1):
                break

    # up left
    if not at_top_left_corner:
        row_to_check = row
        col_to_check = col
        while True:
            row_to_check = row_to_check - 1
            col_to_check = col_to_check - 1
            seat_to_check = seat_configuration[row_to_check][col_to_check]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == 0 or col_to_check == 0:
                break

    # down left
    if not at_bottom_left_corner:
        row_to_check = row
        col_to_check = col
        while True:
            row_to_check = row_to_check + 1
            col_to_check = col_to_check - 1
            seat_to_check = seat_configuration[row_to_check][col_to_check]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == (n_rows - 1) or col_to_check == 0:
                break

    # down right
    if not at_bottom_right_corner:
        row_to_check = row
        col_to_check = col
        while True:
            row_to_check = row_to_check + 1
            col_to_check = col_to_check + 1
            seat_to_check = seat_configuration[row_to_check][col_to_check]
            if seat_to_check == "L":
                break
            elif seat_to_check == "#":
                n_filled += 1
                break
            if row_to_check == (n_rows - 1) or col_to_check == (n_columns - 1):
                break

    return n_filled


def apply_rules(seats: list, is_part1: bool) -> list:

    input_seats = [x for x in seats]
    final_seat_configuration = []
    for irow, row in enumerate(input_seats):
        columns = list(row)

        new_seats = columns[:]

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

            n_adjacent_filled = -1
            if is_part1:
                n_adjacent_filled = n_adjacent_seats_filled(
                    [icol, irow], row, row_above, row_below
                )
            else:
                n_adjacent_filled = n_visible_seats_filled([icol, irow], seats)
            has_no_adjacent_seats = n_adjacent_filled == 0

            # if a seat is empty and no occupaidd seats adjacent, it becomes occupied
            if seat_is_empty and has_no_adjacent_seats:
                new_seats[icol] = "#"
            elif (
                not seat_is_empty and n_adjacent_filled >= {True: 4, False: 5}[is_part1]
            ):
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
    n_iterations, stable_configuration_part1 = find_stable_configuration(
        input_data, True
    )
    print(f"PART 1: stable configuration found in {n_iterations} iterations")
    n_occupied = n_occupied_seats_in_configuration(stable_configuration_part1)
    print(f"PART 1: number of occupied seats in stable configuration: {n_occupied}")

    n_iterations_2, stable_configuration_part2 = find_stable_configuration(
        input_data, False
    )
    n_occupied = n_occupied_seats_in_configuration(stable_configuration_part2)
    print(f"PART 2: number of occupied seats in stable configuration: {n_occupied}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #11")
    parser.add_argument("input", help="Day #11 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
