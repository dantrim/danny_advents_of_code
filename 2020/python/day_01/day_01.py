#!/bin/env python

#
# Advent of Code Day 2020
# Day 01
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path
import itertools
from functools import reduce


def day01(input_data, n_for_combination):
    """
    From the input list, find the [n_for_combination] entries that sum to 2020
    and multiply them together.

    Args:
        input_data [list] : python list of integers
        n_for_combination [int] : length of subsequences in combinations of elements in <input_data>
    """
    return reduce(
        lambda x, y: x * y,
        list(
            filter(
                lambda x: sum(x) == 2020,
                itertools.combinations(input_data, n_for_combination),
            )
        )[0],
    )


def main(input_path):
    with open(input_path, "r") as input_file:
        input_data = [int(x.strip()) for x in input_file.readlines()]
    product_part1 = day01(input_data, 2)
    product_part2 = day01(input_data, 3)
    print(f"Product part1: {product_part1}")
    print(f"Product part2: {product_part2}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #1")
    parser.add_argument("input", help="Day #1 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f'ERROR: bad input "{args.input}"')
        sys.exit(1)
    main(input_path)
