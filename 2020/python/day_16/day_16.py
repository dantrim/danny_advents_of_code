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
from scipy.optimize import linear_sum_assignment

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


@pytest.fixture
def example_data_part2():
    test_data = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""
    return [x.strip() for x in test_data.split("\n") if x]


def test_example_1(example_data):

    _, ranges, _, tickets = load_input_data(example_data)
    error_rate, _ = part1(ranges, tickets)
    assert error_rate == 71


def test_example_2(example_data_part2):
    names, ranges, _, tickets = load_input_data(example_data_part2)
    _, tickets = part1(ranges, tickets)
    class_ordering = determine_class_assignment(names, ranges, tickets)
    assert class_ordering == {0: "row", 1: "class", 2: "seat"}


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
    ok_tickets = []
    for iticket, ticket in enumerate(nearby_tickets):
        ticket_set = set(ticket)
        invalid_field_data = list(ticket_set - valid_values_any_field)
        bad_values += invalid_field_data
        if len(invalid_field_data) == 0:
            ok_tickets.append(ticket)
    return sum(bad_values), ok_tickets


def determine_class_assignment(class_names, class_ranges, input_tickets):

    # make the arrays the same shape by padding with a repeated value
    max_len_class_range = -1
    max_len_tickets = -1
    for class_range in class_ranges:
        max_len_class_range = max([max_len_class_range, len(class_range)])
    for ticket in input_tickets:
        max_len_tickets = max([max_len_tickets, len(ticket)])

    ranges = []
    for class_range in class_ranges:
        while len(class_range) != max_len_class_range:
            class_range.append(class_range[-1])
        ranges.append(class_range)
    tickets = []
    for ticket in input_tickets:
        while len(ticket) != max_len_tickets:
            ticket.append(ticket[-1])
        tickets.append(ticket)

    # these arrays will now have the same dimension that we care about
    ranges = np.array(
        ranges
    ).T  # take transpose to associate range rows to all tickets in a specific column
    tickets = np.array(tickets)
    n_classes_from_tickets = tickets.shape[1]
    n_classes_from_ranges = ranges.shape[1]
    if n_classes_from_ranges != n_classes_from_tickets:
        print(
            f"ERROR different classes from ranges vs tickets (ranges: {n_classes_from_ranges}, tickets: {n_classes_from_tickets})"
        )
        sys.exit(1)

    # use the hungarian algorithm (https://en.wikipedia.org/wiki/Hungarian_algorithm)
    # to define a cost matrix for assigning ticket columns to class columns
    n_classes = n_classes_from_ranges
    cost_matrix = np.zeros(shape=(n_classes, n_classes))
    for i in range(0, n_classes):
        ticket_col = set(tickets[:, i])
        for j in range(0, n_classes):
            range_col = set(ranges[:, j])
            diff = ticket_col - range_col

            # for valid assignments, the cost should be minimal -- set it to zero
            if not diff:
                pass  # cost matrix is intially all zeros
            else:
                cost_matrix[i, j] = 1

    row_assignments, col_assignments = linear_sum_assignment(cost_matrix)
    assignments = list(
        zip(*linear_sum_assignment(cost_matrix))
    )  # contains tuples of ticket column/index <--> class mappings
    # create a mapping between the ticket index and the names of the associated class/rule
    col_to_class_map = {}
    for assignment in assignments:
        tickets_col, class_index = assignment
        col_to_class_map[tickets_col] = class_names[class_index]
    return col_to_class_map


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]

    class_names, class_ranges, my_ticket, nearby_tickets = load_input_data(input_data)
    print(f"Loaded {len(class_names)} classes and {len(nearby_tickets)} nearby tickets")

    # part1
    error_rate, ok_nearby_tickets = part1(class_ranges, nearby_tickets)
    print(f"PART 1: ticket scanning error rate = {error_rate}")

    # part 2
    class_assignment = determine_class_assignment(
        class_names, class_ranges, ok_nearby_tickets
    )
    departure_vals = []
    for ticket_col, class_name in class_assignment.items():
        if class_name.startswith("departure"):
            departure_vals.append(my_ticket[ticket_col])
    print(f"PART 2: departure vals = {departure_vals}")
    print(f"PART 2: departure vals product = {np.prod(departure_vals)}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #16")
    parser.add_argument("input", help="Day #16 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
