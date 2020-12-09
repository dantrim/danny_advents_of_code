#!/bin/env python

#
# Advent of Code 2020
# Day 09
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

from itertools import islice, combinations
import numpy as np


def test_example_0():
    test_data_path = Path("test_input.txt")
    with open(test_data_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    assert find_first_weakness(input_data, preamble_length=5) == 127


def xmas_chunks(input_data: list, length_of_preamble: int) -> list:
    """
    Generator that iterates through the `input_data` by windows
    of length `length_of_preamble`+1, with the start position of
    the window advancing by only 1 position at each step in the
    iteration.
    """
    step = 0
    window_length = length_of_preamble + 1
    chunk = []
    while True:
        chunk = [int(x.strip()) for x in islice(input_data, step, step + window_length)]
        if len(chunk) != window_length:
            break
        yield chunk
        step += 1


def find_pairs_that_sum_to(word, words_to_check):
    return list(filter(lambda x: sum(x) == word, combinations(set(words_to_check), 2)))


def find_first_weakness(input_data: list, preamble_length: int) -> int:

    for ichunk, chunk in enumerate(xmas_chunks(input_data, preamble_length)):
        chunk = np.array(chunk)
        previous_words, current_word = chunk[:preamble_length], chunk[-1]
        words_that_sum = find_pairs_that_sum_to(current_word, previous_words)

        # found the case where there are no previous words that sum to the current one
        if not words_that_sum:
            return current_word
    return None


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    # part 1
    first_weakness = find_first_weakness(input_data, 25)
    print(f"PART 1: First weakness = {first_weakness}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #9")
    parser.add_argument("input", help="Day #9 input file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
