#!/bin/env python

#
# Advent of Code 2020
# Day 12
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest
import numpy as np


class Ship:
    """
    A structure to hold the arrays for the ship position and orientation,
    which are in containers. So it is a container ship.
    """

    def __init__(self):
        self.state = np.zeros(3)  # x-position, y-position, heading
        self.waypoint = np.array(
            [10, 1]
        )  # x-position, y-position relative to ship state
        self.previous_positions = []


@pytest.fixture
def example_instructions():
    instructions = """
    F10
    N3
    F7
    R90
    F11
    """
    return [x.strip() for x in instructions.split()]


def test_example_0_heading(example_instructions):

    ship = Ship()
    for instruction in example_instructions:
        advance_ship_part1(ship, instruction)
    assert list(ship.state) == [17, -8, 270]


def test_example_0_distance(example_instructions):
    ship = Ship()
    for instruction in example_instructions:
        advance_ship_part1(ship, instruction)
    assert sum([abs(x) for x in ship.state[:2]]) == 25


def test_example_1_heading(example_instructions):
    ship = Ship()
    print(f"ship: {ship.state}, {ship.waypoint}")
    for instruction in example_instructions:
        advance_ship_part2(ship, instruction)
        print(f"AFTER {instruction} --> ship: {ship.state}, {ship.waypoint}")
    assert list(ship.state) == [214, -72, 0]


def test_example_1_waypoint(example_instructions):
    ship = Ship()
    for instruction in example_instructions:
        advance_ship_part2(ship, instruction)
    assert list(ship.waypoint) == [4, -10]


def test_example_1_distance(example_instructions):
    ship = Ship()
    for instruction in example_instructions:
        advance_ship_part2(ship, instruction)
    assert sum([abs(x) for x in ship.state[:2]]) == 286


def advance_ship_part1(ship: Ship, instruction: str):
    """
    Advances the orientation and/or position of the input ship
    based on the input instruction string `instruction`.
    """

    magnitude = int(instruction[1:])
    # rotation
    if "L" in instruction or "R" in instruction:
        direction = {"L": 1, "R": -1}[instruction[0]]
        advance = [0, 0, magnitude * direction]

    # translation
    elif "F" in instruction:
        orientation = ship.state[2] % 360
        advance = {
            0: [magnitude, 0, 0],
            90: [0, magnitude, 0],
            180: [-1 * magnitude, 0, 0],
            270: [0, -1 * magnitude, 0],
        }[orientation]
    else:
        direction = instruction[0]
        advance = {
            "N": [0, magnitude, 0],
            "S": [0, -1 * magnitude, 0],
            "W": [-1 * magnitude, 0, 0],
            "E": [magnitude, 0, 0],
        }[direction]
    ship.state += advance
    ship.state[2] = (ship.state[2] + 360) % 360


def advance_ship_part2(ship: Ship, instruction: str):
    """
    Advances the ship and waypoint positions based on the input instruction.
    """

    magnitude = int(instruction[1:])
    instruction = instruction[0]

    # move the waypoint
    if instruction in ["N", "S", "E", "W"]:
        advance = {
            "N": [0, magnitude],
            "S": [0, -1 * magnitude],
            "E": [magnitude, 0],
            "W": [-1 * magnitude, 0],
        }[instruction]
        ship.waypoint += advance
    elif instruction in ["L", "R"]:
        degrees = magnitude
        if "R" in instruction:
            degrees *= -1
        degrees = (degrees + 360) % 360
        ship.waypoint = np.array(
            {
                90: [-1 * ship.waypoint[1], ship.waypoint[0]],
                180: [-1 * ship.waypoint[0], -1 * ship.waypoint[1]],
                270: [ship.waypoint[1], -1 * ship.waypoint[0]],
            }[degrees]
        )
    elif instruction == "F":
        unit_x = ship.waypoint[0]
        unit_y = ship.waypoint[1]
        ship.state += [unit_x * magnitude, unit_y * magnitude, 0]


def main(input_path):

    with open(input_path, "r") as ifile:
        instructions = [x.strip() for x in ifile]
    print(f"loaded {len(instructions)} instructions")

    # part 1
    ship = Ship()
    for instruction in instructions:
        advance_ship_part1(ship, instruction)
    print(f"PART 1: Final ship state   : {ship.state}")
    manhattan_distance = int(sum([abs(x) for x in ship.state[:2]]))
    print(f"PART 1: Manhattan distance : {manhattan_distance}")

    # part 2
    ship = Ship()
    for instruction in instructions:
        advance_ship_part2(ship, instruction)
    print(f"PART 2: Final ship state   : {ship.state}")
    print(f"PART 2: Final waypoint     : {ship.waypoint}")
    manhattan_distance = int(sum([abs(x) for x in ship.state[:2]]))
    print(f"PART 2: Manhattan distance : {manhattan_distance}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #12")
    parser.add_argument("input", help="Day #12 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
