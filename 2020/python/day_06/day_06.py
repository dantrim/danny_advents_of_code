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


def test_n_each_response_in_group(customs_data):
    assert counts_for_each_response(load_groups(customs_data)) == [
        {"a": 1, "b": 1, "c": 1},
        {"a": 1, "b": 1, "c": 1},
        {"a": 2, "b": 1, "c": 1},
        {"a": 4},
        {"b": 1},
    ]


def test_n_unanimous_in_group(customs_data):
    assert [len(x) for x in unanimous_responses(load_groups(customs_data))] == [
        3,
        0,
        1,
        1,
        1,
    ]


def test_sum_n_unanimous(customs_data):
    assert sum([len(x) for x in unanimous_responses(load_groups(customs_data))]) == 6


def unanimous_responses(group_responses: list) -> list:
    """
    For each of the unique responses in a group's response, find out if
    it was given by ALL members of a given group, or just some.
    Return the list, per group, of those responses for which everyone in the
    group responded to with YES.
    """

    group_unanimous_responses = []
    group_counts_dict = counts_for_each_response(group_responses)
    for group_idx, counts_dict in enumerate(group_counts_dict):
        unanimous_responses = []
        n_people_in_group = len(group_responses[group_idx])
        for response, n_appearances_of_response in counts_dict.items():
            if n_appearances_of_response == n_people_in_group:
                unanimous_responses.append(response)
        group_unanimous_responses.append(unanimous_responses)
    return group_unanimous_responses


def counts_for_each_response(group_responses: list) -> list:
    """
    Count the number of occurrences of each of the unique responses within a group.

    Args:
        group_responses [list] : A list of of lists. Each sub-list contains each
            groups' person's responses.

    Returns:
        list of dict
    """

    group_counts = []
    uniques = unique_responses(group_responses)
    for igroup, group in enumerate(group_responses):
        counts = {}
        for unique in uniques[igroup]:
            counts[unique] = "".join(group).count(unique)
        group_counts.append(counts)
    return group_counts


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

    # part 2
    sum_unanimous_responses = sum(
        [len(x) for x in unanimous_responses(load_groups(input_path))]
    )
    print(f"PART 2: Sum of unanimous responses : {sum_unanimous_responses}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #6")
    parser.add_argument("input", help="Day #6 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERORR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
