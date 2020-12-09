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


def test_example_0():
    test_data_path = Path("test_input.txt")
    with open(test_data_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    assert find_first_weakness(input_data, preamble_length=5) == 127


def test_find_contiguous_set():
    test_data_path = Path("test_input.txt")
    with open(test_data_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    assert contiguous_set_that_sums_to(127, input_data) == [15, 25, 47, 40]


def test_example_1():
    test_data_path = Path("test_input.txt")
    with open(test_data_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    weakness_set = contiguous_set_that_sums_to(127, input_data)
    if weakness_set is None:
        return False
    lo, hi = min(weakness_set), max(weakness_set)
    summed = sum([lo, hi])
    assert [lo, hi, summed] == [15, 47, 62]


def xmas_chunks(input_data: list, window_length: int, advance: int) -> list:
    """
    Generator that iterates through `input_data` by windows
    of length `window_length`, with the start position of
    the window advancing by `advance` positions at each step in the
    iteration.
    """
    step = 0
    chunk = []
    while True:
        chunk = [int(x.strip()) for x in islice(input_data, step, step + window_length)]
        if len(chunk) != window_length:
            break
        yield chunk
        step += advance


def find_sets_that_sum_to(word: int, words_to_check: list, length_of_sum=2) -> list:
    """
    Return a list of lists whose sum are equal to `word`.
    The size of the sub-lists (from which the sums are derived) are of
    length `length_of_sum`.
    """
    return list(
        filter(
            lambda x: sum(x) == word, combinations(set(words_to_check), length_of_sum)
        )
    )


def find_first_weakness(input_data: list, preamble_length: int) -> int:
    """
    Find the first word in `input_data` that cannot be the result
    of the sum of the previous `preamble_length` words.
    """

    for ichunk, chunk in enumerate(xmas_chunks(input_data, preamble_length + 1, 1)):
        previous_words, current_word = chunk[:preamble_length], chunk[-1]
        words_that_sum = find_sets_that_sum_to(current_word, previous_words)

        # found the case where there are no previous words that sum to the current one
        if not words_that_sum:
            return current_word
    return None


def contiguous_set_that_sums_to(summed_value: int, input_data: list) -> list:

    """
    Find the contiguous set of words in the input data `input_data` list
    that sum to the requested value `summed_value`.

    This function assumes that there is only one such contiguous set,
    and exits once the first such set is found.
    """

    length = 2
    while True:
        if length == len(input_data):
            break
        for ichunk, chunk in enumerate(xmas_chunks(input_data, length, 1)):
            if sum(chunk) == summed_value:
                return chunk
        length += 1
    return None


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]
    # part 1
    first_weakness = find_first_weakness(input_data, 25)
    print(f"PART 1: First weakness = {first_weakness}")

    contiguous_set = contiguous_set_that_sums_to(first_weakness, input_data)
    if contiguous_set is None:
        print(
            f"ERROR: Did not find a contiguous set of data that sum to {first_weakness}!"
        )
        sys.exit(1)
    lo, hi = min(contiguous_set), max(contiguous_set)
    print(f"PART 2: min = {lo}, max = {hi} => sum = {sum([lo,hi])}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #9")
    parser.add_argument("input", help="Day #9 input file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
