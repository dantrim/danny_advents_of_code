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


def test_part2(example_notes):
    assert part2_shenanigans(example_notes) == 1068781


def part2_shenanigans(input_data):

    busses = ["x" if x == "x" else int(x) for x in input_data[1].split(",")]

    # What we want to do is compare the busses in turn:
    #   STEP 0: 0             <---> 1,
    #   STEP 1: [0,1]         <---> 2,
    #   STEP 2: [0,1,2]       <---> 3,
    #   STEP 3: [0,1,2,...,N] <---> N+1
    #   ...
    #   ...
    # At each step of considering buses [a] <---> b, we advance in time by the
    # interval that defines the bus group [a] since by advancing in time by
    # this amount we know that the relative offset between the busses
    # in [a] will no longer change (i.e. the relationship between their offsets
    # will be unchanged).
    #
    # So in STEP 0, with bus 0 having time step t_0, we continously advance in timesteps
    # t_0 until we arrive at the point where (t_0 + idx_1) is a multiple of t_1,
    # where idx_1 is the relative offset (in timestamps) of bus 1. This is the
    # requirement of part 2.
    #
    # Moving on to STEP 1, we again advance in timesteps until we find a timestamp
    # at which point the (timestamp + idx_2) is a multiple of t_2. Since we do
    # not want to disrupt the bus 0 and bus 1 alignment that we found in STEP 0,
    # we must then advance in time steps that are multiples of their own two times, which
    # will mean that the timetamp that we find for the bus 2 condition is a common
    # multiple of both bus 0 and bus 1, and that at that timestamp bus 1 is still
    # idx_1 timestamps ahead of bus 0.
    #
    # So, generally after each STEP i we advance in time increments of t_i, and stop
    # once we have met the defined condition that the (timetamp + relative offset
    # idx_{i+1}) is a multiple of t_{i+1}. For subsequent STEPs, we then advance
    # in steps of t_{i} * t_{i+1} since this guarantees the requirements are held
    # for the previous steps.

    # the initial time is kind of meaningless -- what matters is the relative offset of the
    # times, so we can call the initial time to be t = 0 and associate that with
    # the bus at index = 0
    timestamp = 0

    # starting at 0 with an increment of the bus at index 0
    # (this quantity is our timestep of the [0,..,N] on the LHS above):
    t_step = busses[0]  # t_0
    for idx_bus, t_bus in enumerate(busses):

        # we don't need to do anything for bus 0, since everything is relative to it
        if idx_bus == 0:
            continue

        # we include the x's to encode the offset/index numbers in the input data
        if t_bus == "x":
            continue

        # advance in time until the offset condition is met (the timestamp + idx
        # is a multiple of the current bus's time step)
        while (timestamp + idx_bus) % t_bus != 0:
            timestamp += t_step
        # at this point we have advanced in time for [i] bus group to match
        # the condition of meeiting the offset of [i+1] bus, so we update the
        # advance rate to be a common multiple of the [i] and [i+1] bus groups
        t_step *= t_bus

    # we have gon through all busses
    return timestamp


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

    # part2
    timestamp = part2_shenanigans(input_data)
    print(f"PART 2: Timestamp satisfying part 2 requirements: {timestamp}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #13")
    parser.add_argument("input", help="Day #13 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
