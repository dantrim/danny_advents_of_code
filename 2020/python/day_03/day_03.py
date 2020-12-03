#!/bin/env python

#
# Advent of Code 2020
# Day 03
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path
import numpy as np


def load_forest(input_path):
    """
    Just load in the full thing all at once.
    """

    forest_list = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            forest_list.append(list(line))
    return np.array(forest_list)


def is_tree(character):
    """ A tree character is defined as "#" """
    return character == "#"


def traverse_slope(full_forest, right_step, down_step):
    """
    Traverse the full forest, moving right <right_step>
    number of steps and down <down_step> number of steps,
    starting at the upper left corner and count how many
    trees ("#") are encountered on the way down.

    The forest pattern on a given "height" (row) repeats
    indefinitely.

    Args:
        full_forest [numpy array, 2D]: 2D array of the forest
        right_step [int]: the amount to move across a forest row (to the right) in each step
        down_step [int]: the number of rows to traverse downward in each step
    """

    n_trees = 0
    forest_row_width = -1
    for istep, forest_row in enumerate(full_forest[::down_step]):
        if forest_row_width < 0:
            forest_row_width = len(forest_row)
        else:
            # just being careful in case I c&p'd incorrectly :)
            if len(forest_row) != forest_row_width:
                print(f"ERROR: Abnormal forest row shape encountered at row {istep}!")
                sys.exit(1)
        right_pos = (right_step * istep) % forest_row_width
        if is_tree(forest_row[right_pos]):
            n_trees += 1
    return n_trees


def main(input_path):

    full_forest = load_forest(input_path)
    # part 1
    n_trees_encountered = traverse_slope(full_forest, right_step=3, down_step=1)
    print(f"PART 1: Number of trees encountered = {n_trees_encountered}")

    # part 2
    slopes_to_consider = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    encountered_trees = []
    for islope, slope_to_consider in enumerate(slopes_to_consider):
        right_step, down_step = slope_to_consider
        n_trees = traverse_slope(
            full_forest, right_step=right_step, down_step=down_step
        )
        encountered_trees.append(n_trees)
    print(f"PART 2: Encountered trees            = {encountered_trees}")
    print(f"PART 2: Product of encountered trees = {np.prod(encountered_trees)}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #3")
    parser.add_argument("input", help="Day #3 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
