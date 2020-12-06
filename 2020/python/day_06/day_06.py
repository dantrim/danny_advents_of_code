#!/bin/env python

#
# Advent of Cdoe 2020
# Day 06
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path
import pytest


@pytest.fixture
def customs_data():
    test_data = """
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b


    """
    with open("test_input.txt", "w") as tfile:
        tfile.write(test_data)
    return Path("test_input.txt")


def test_n_per_group(customs_data):
    assert [len(x) for x in load_groups(customs_data)] == [1, 3, 2, 4, 1]


def test_unique_responses_per_group(customs_data):
    assert unique_responses(load_groups(customs_data)) == [
        ["a", "b", "c"],
        ["a", "b", "c"],
        ["a", "b", "c"],
        ["a"],
        ["b"],
    ]


def test_n_unique_responses_per_group(customs_data):
    assert [len(x) for x in unique_responses(load_groups(customs_data))] == [
        3,
        3,
        3,
        1,
        1,
    ]


def test_sum_unique_responses(customs_data):
    assert sum(len(x) for x in unique_responses(load_groups(customs_data))) == 11


def unique_responses(group_responses: list) -> list:
    """
    From the list of group responses, pick out the unique responses.

    Args:
        group_responses [list] : A list of of lists. Each sub-list contains each
            groups' person's responses.

    Returns:
        list [str] : A list of lists, with duplicate responses removed from the input.

    """

    out = [sorted(list(set(list("".join(g))))) for g in group_responses]
    return out


def load_groups(input_path: Path) -> list:
    """
    Load in the customs quesetionarre response data into a buffer and group
    together the responses that are associated with a single group.
    Responses belonging to a single group are on contiguous lines,
    and groups are separated by a blank line. Splitting by "\n\n" will
    break apart the responses from separate groups, and then removing
    the "\n" characters from in-group responses should then just give
    us the specific responses void of whitespace characters.

    Remove empty characters per line and also empty groups.

    Args:
        input_path [pathlib.Path]: path to input data

    Returns:
        list of lists: [ [group-responses] ]
    """
    with open(input_path, "r") as infile:
        groups = list(
            filter(
                None,
                [
                    list(
                        filter(
                            None,
                            [line.strip() for line in group.split("\n") if line != ""],
                        )
                    )
                    for group in infile.read().split("\n\n")
                ],
            )
        )
        return groups


def main(input_path):

    # part 1
    sum_of_unique_responses = sum(
        len(x) for x in unique_responses(load_groups(input_path))
    )
    print(f"PART 1: Sum of unique responses    : {sum_of_unique_responses}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #6")
    parser.add_argument("input", help="Day #6 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERORR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
