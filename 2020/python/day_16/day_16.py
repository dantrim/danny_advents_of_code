#!/bin/env python

#
# Advent of Code 2020
# Day 16
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np

import pytest


@pytest.fixture
def example_data():
    test_data = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""
    return [x.strip() for x in test_data.split("\n") if x]


def test_example_1(example_data):

    _, ranges, _, tickets = load_input_data(example_data)
    assert part1(ranges, tickets) == 71


def load_input_data(input_data):

    class_names = []
    class_ranges = []
    my_ticket = []
    nearby_tickets = []

    my_ticket_line = -1
    nearby_ticket_line = -1

    for iline, line in enumerate(input_data):
        line = line.strip()
        if not line:
            continue

        if "ticket" not in line and len(line.split(":")) > 1:
            class_name, range_info = line.split(":")

            class_names.append(class_name.strip())

            ranges = [x.strip() for x in range_info.split("or")]

            valid_values = list(
                np.arange(
                    int(ranges[0].split("-")[0]), int(ranges[0].split("-")[1]) + 1, 1
                )
            )
            valid_values += list(
                np.arange(
                    int(ranges[1].split("-")[0]), int(ranges[1].split("-")[1]) + 1, 1
                )
            )
            class_ranges.append(list(map(int, valid_values)))
            continue
        elif "your ticket" in line:
            my_ticket_line = iline + 1
            continue
        elif "nearby tickets" in line:
            nearby_ticket_line = iline + 1
            continue

        if iline == my_ticket_line:
            my_ticket = list(map(int, line.split(",")))
            continue

        elif iline >= nearby_ticket_line:
            nearby_ticket = list(map(int, line.split(",")))
            nearby_tickets.append(nearby_ticket)
            continue
    return class_names, class_ranges, my_ticket, nearby_tickets


def part1(class_ranges, nearby_tickets):

    # flatten
    valid_values_any_field = []
    for class_range in class_ranges:
        for value in class_range:
            valid_values_any_field.append(value)
    valid_values_any_field = set(valid_values_any_field)

    bad_values = []
    for ticket in nearby_tickets:
        ticket = set(ticket)
        bad_values += list(ticket - valid_values_any_field)
    return sum(bad_values)


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    class_names, class_ranges, my_ticket, nearby_tickets = load_input_data(input_data)
    print(f"Loaded {len(class_names)} classes and {len(nearby_tickets)} nearby tickets")

    # part1
    error_rate = part1(class_ranges, nearby_tickets)
    print(f"PART 1: ticket scanning error rate = {error_rate}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #16")
    parser.add_argument("input", help="Day #16 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
