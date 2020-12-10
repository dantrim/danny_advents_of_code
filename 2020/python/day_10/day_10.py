#!/bin/env python

#
# Advent of Code 2020
# Day 10
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path
import functools

import pytest
import numpy as np
import collections
from itertools import groupby


@pytest.fixture
def example_data_0():
    test_data = """
    16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4
    """
    return [int(x.strip()) for x in test_data.split()]


@pytest.fixture
def example_data_1():
    test_data = """
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3
    """
    return [int(x.strip()) for x in test_data.split()]


def test_example_0(example_data_0):
    assert find_diff_distribution(example_data_0) == {1: 7, 3: 5}


def test_example_1(example_data_1):
    assert find_diff_distribution(example_data_1) == {1: 22, 3: 10}


def test_n_all_configurations_0(example_data_0):
    assert find_n_valid_ways(example_data_0) == 8


def test_n_all_configurations_1(example_data_1):
    assert find_n_valid_ways(example_data_1) == 19208


def find_diff_distribution(input_data: list) -> dict:
    """
    Take the input data and compute the element-wise diff.
    Return the count of each of the uniquely appearing difference values.
    """
    input_data = collections.deque(sorted(input_data))
    input_data.appendleft(0)  # the wall plug
    input_data.append(
        input_data[-1] + 3
    )  # the device is +3 joltage rating relative to last element
    input_data = np.array(input_data)
    diffs = list(np.diff(input_data))

    unique_diffs = list(set(diffs))
    counts = [diffs.count(x) for x in unique_diffs]
    counts = dict(zip(unique_diffs, counts))
    return counts


def find_runs(diffs):
    """
    Find all continuous runs of elements of value 1, that are longer than 1.
    """
    return [
        x
        for x in [list(run) for run_value, run in groupby(diffs) if run_value == 1]
        if len(x) > 1
    ]


@functools.lru_cache(maxsize=100)
def find_n_inclusive(run_length: int) -> int:

    """
    This function takes in an array `run` of a fixed length,
    and creates all possible arrays of the same length
    where valid elements are populated.

    An element can be filled as long it satisfies the following requirements:
       - If after adding that element, there will be no run of filled elements
            that is of size 3 or greater
       - We have not wrapped around the whole length of the array

    Element filling starts at the first column (where a column ranges from
    [0,len(run)). Once element filling has wrapped around, the column is
    advanced by one and the process begins again.

    The filling process follows a "growth" and "pop" process.
    We fill an array of 0's of length len(run), and create a seed
    element at index 0. Then the "growth" and "pop" process begins, starting
    with "growth" and moving to "pop", alternating:
        "growth": in this stage, an element immediately to the right (with wrap-around)
                   of the previous filled element is filled
        "pop":    the previous filled element is advanced by one position in the array,
                    thus making this position now filled (and it's previous position
                    no longer being filled)
    Once a wrap-around of the array has been detected, the "growth" and "pop"
    stage re-starts, but advancing the initial seed element (row) by one position.

    For example, for a `run` of length 4:
    --------------------------------
    [1,0,0,0] # SEED 0
    [1,1,0,0] # growth
    [1,0,1,0] # pop
    [1,0,1,1] # growth // WRAP AROUND DETECTED
    [0,1,0,0] # SEED 1
    [0,1,1,0] # growth
    [0,1,0,1] # pop
    [1,1,0,1] # growth // the "next" position wraps around
              #    -> at this point, a *pop* would result in a run of 3,
              #       and it is skipped
    [0,0,1,0] # SEED 2
    [0,0,1,1] # growth
    [1,0,1,0] # pop
    ...
    ...
    ---------------------------------
    What is returned is the number of unique arrays,
    representing the number of ways that the adapters in the
    input run can be removed/shifted.
    """

    possibilities = []
    for start_idx in range(run_length):
        start_field = [int(x) for x in np.zeros(run_length)]
        start_field[start_idx] = 1
        possibilities.append(list(start_field))

        stage = 0
        current_idx = start_idx
        while True:
            last_field = list(possibilities[-1])

            if stage % 2 == 0:  # grow stage
                # this is the growth stage, where the element just to the right
                # of the last-tagged element is tagged
                field = last_field
                current_idx = (current_idx + 1) % run_length
                field[current_idx] = 1
                field = list(field)
                if field not in possibilities:
                    possibilities.append(field)
            else:
                # in this stage we "pop" the last element that was grown
                # off and advance it to the right by one
                field = last_field
                field[current_idx] = 0
                current_idx = (current_idx + 1) % run_length
                field[current_idx] = 1
                if current_idx == start_idx:
                    break
                field = list(field)
                if field not in possibilities:
                    possibilities.append(field)

            # if the current_idx == start_idx, then we have definitely wrapped around
            if current_idx == start_idx:
                break
            stage += 1
    return len(possibilities)


def find_n_valid_ways(input_data: list) -> int:
    """
    Find all possible adapter configurations that satisfy the
    rules of not having a ∆ of joltage rating greater than 3.

    Adapters can be removed from the list, so long as the list after
    the removal still satisfies the rules.
    """

    input_data = collections.deque(sorted(input_data))
    input_data.appendleft(0)  # the wall plug
    input_data.append(
        input_data[-1] + 3
    )  # the device is +3 joltage rating relative to last element
    input_data = np.array(input_data)
    diffs = np.diff(input_data)
    runs_of_ones = find_runs(diffs)
    adapter_configurations = []
    for irun, run in enumerate(runs_of_ones):
        # we cannot remove the last element, since the next element beyond it
        # is a ∆ of 3, so remove it from elements that can be considered
        # to be removed/permuted
        run = run[:-1]
        n_adapter_combinations_for_run = find_n_inclusive(int(len(run)))

        # add 1 for the configuration where no adapters are removed and/or shifted
        adapter_configurations.append(n_adapter_combinations_for_run + 1)
    return np.prod(adapter_configurations)


def main(input_path):

    # load
    with open(input_path, "r") as ifile:
        input_data = [int(x.strip()) for x in ifile.readlines() if x != ""]

    # part 1
    diff_dist = find_diff_distribution(input_data)
    differences = np.array(list(diff_dist.keys()))
    if (differences > 3).any():
        print("ERROR: Invalid differences (>3) found!")
        sys.exit(1)
    print(f"PART 1: Difference distribution: {diff_dist}")
    part1 = diff_dist[1] * diff_dist[3]
    print(f"PART 1: 1-jolt diffs x 3-jolt diffs = {part1}")

    # part 2
    n_valid_adapter_configurations = find_n_valid_ways(input_data)
    print(
        f"PART 2: Number of valid adapter configurations: {n_valid_adapter_configurations}"
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #10")
    parser.add_argument("input", help="Day #10 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
