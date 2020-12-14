#!/bin/env python

#
# Advent of Code 2020
# Day 13
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest
import numpy as np


@pytest.fixture
def example_notes():
    test_data = """
    939
    7,13,x,x,59,x,31,19
    """
    return [x.strip() for x in test_data.split()]


def test_find_earliest_bus(example_notes):

    target_time = int(example_notes[0])
    bus_ids = [int(x) for x in example_notes[1].split(",") if x != "x"]
    bus_id, time = get_earliest_bus_arrival(target_time, bus_ids)
    assert (bus_id, time) == (59, 944)


def get_earliest_bus_arrival(target_time: int, bus_ids: list) -> list:

    max_interval = max(bus_ids)

    minimum_time_delta = 1e9
    minimum_stop_time = 1e9
    minimum_bus_id = -1
    for ibus, bus_id in enumerate(bus_ids):

        # just make a wide interval of schedules for this particular bus, and
        # compute all deltas... and then find the closest one arriving nearest
        # (but not before) the target time
        stop_times_to_consider = np.arange(0, target_time + 2 * max_interval, bus_id)
        for stop_time in stop_times_to_consider:
            delta = stop_time - target_time

            # can't take buses whose arrivate time at the port stop is before
            # the time that we can make
            if delta < 0:
                continue

            if delta < minimum_time_delta:
                minimum_time_delta = delta
                minimum_bus_id = bus_id
                minimum_stop_time = stop_time
    return minimum_bus_id, minimum_stop_time


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile]

    target_time = int(input_data[0])
    bus_ids = [int(x.strip()) for x in input_data[1].split(",") if x != "x"]

    # part 1
    bus_id, arrival_time = get_earliest_bus_arrival(target_time, bus_ids)
    print(
        f"PART 1: Earliest bus has ID: {bus_id}, and arrives at timestamp {arrival_time}"
    )
    wait_time = arrival_time - target_time
    print(f"PART 1: wait time = {wait_time}")
    print(f"PART 1: wait_time * bus_id = {wait_time * bus_id}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #13")
    parser.add_argument("input", help="Day #13 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
