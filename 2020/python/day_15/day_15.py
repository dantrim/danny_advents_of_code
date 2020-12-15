#!/bin/env python

#
# Advent of Code 2020
# Day 15
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest


@pytest.fixture
def example_data_0():
    return [0, 3, 6]


def test_example_turns(example_data_0):
    spoken_words = []
    for i in range(10):
        spoken_words.append(part1(example_data_0, i + 1))
    assert spoken_words == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]


def test_example_0(example_data_0):
    assert part1(example_data_0, 2020) == 436


def test_example_1():
    assert part1([1, 3, 2], 2020) == 1


def test_example_2():
    assert part1([2, 1, 3], 2020) == 10


def test_example_3():
    assert part1([1, 2, 3], 2020) == 27


def test_example_4():
    assert part1([2, 3, 1], 2020) == 78


def test_example_5():
    assert part1([3, 2, 1], 2020) == 438


def test_example_6():
    assert part1([3, 1, 2], 2020) == 1836


def part1(game_input: list, n_turns_to_take: int) -> int:

    counts_dict = {}
    spoken_words = []

    # start the game
    for ig, g in enumerate(game_input):
        counts_dict[g] = 1
        spoken_words.append(g)
        if n_turns_to_take == len(spoken_words):
            return g

    while len(spoken_words) != n_turns_to_take:

        last_word_spoken = spoken_words[-1]
        # was the last word spoken for the first time?
        last_was_first = counts_dict[last_word_spoken] == 1

        if last_was_first:
            # if the last spoken word was the first time that that word
            # appeared, then the current spoken word for this turn is 0
            spoken_word = 0
        else:
            # if the last word spoken has been spoken previously (in a turn prior to the previous one)
            # then the next spoken word is the difference between the turn number
            # when it was last spoken and the turn number of the turn prior to the previous one

            turn_number_of_previous = len(spoken_words) - 1
            turn_number_of_previous_previous = -1
            for n_back, word in enumerate(spoken_words[:-1][::-1]):
                if word == last_word_spoken:
                    # +1 since counter back starts at 0, and +1 since we removed the very last element before iterating
                    turn_number_of_previous_previous = len(spoken_words) - (n_back + 2)
                    break
            if (
                turn_number_of_previous_previous < 0
                or turn_number_of_previous_previous == turn_number_of_previous
            ):
                print(
                    f"ERROR: Failed to find previous previous turn number for last spoken word (={last_word_spoken})"
                )
                sys.exit(1)

            turn_number_difference = (
                turn_number_of_previous - turn_number_of_previous_previous
            )
            spoken_word = turn_number_difference

        spoken_words.append(spoken_word)
        if spoken_word in counts_dict:
            counts_dict[spoken_word] += 1
        else:
            counts_dict[spoken_word] = 1
        continue

    return spoken_words[-1]


def main(input_path):
    with open(input_path, "r") as ifile:
        input_data = [int(x) for x in ifile.read().strip().split(",")]

    # part 1
    word = part1(input_data, 2020)
    print(f"PART 1: 2020th number spoken: {word}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #15")
    parser.add_argument("input", help="Day #15 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
