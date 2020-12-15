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
    for i in range(3, 10):
        spoken_words.append(play_game(example_data_0, i + 1))
    assert spoken_words == [0, 3, 3, 1, 0, 4, 0]


def test_example_0(example_data_0):
    assert play_game(example_data_0, 2020) == 436


def test_example_1():
    assert play_game([1, 3, 2], 2020) == 1


def test_example_2():
    assert play_game([2, 1, 3], 2020) == 10


def test_example_3():
    assert play_game([1, 2, 3], 2020) == 27


def test_example_4():
    assert play_game([2, 3, 1], 2020) == 78


def test_example_5():
    assert play_game([3, 2, 1], 2020) == 438


def test_example_6():
    assert play_game([3, 1, 2], 2020) == 1836


def test_part2_0():
    assert play_game([0, 3, 6], 30000000) == 175594


def play_game(game_input: list, n_turns_to_take: int) -> int:

    if n_turns_to_take < len(game_input):
        print("ERROR: n_turns_to_take < len(game_input)!")
        sys.exit(1)

    # dict of previous turns in which a word has appeared (we only ever care about the previous)
    spoken_word_history = {}

    # Automatically, the next spoken word after loading in the input will be 0 since all input words are unique.
    # So we load it prior to starting the iterations.
    word_to_be_spoken = 0

    # start the game -- all input is unique
    for turn_num, val in enumerate(game_input):
        spoken_word_history[val] = turn_num

    # start iterating now, once we have loaded in the game input.
    # start the turn number counts to starting with the count of turns
    # after loading the input.
    for turn_num in range(len(game_input), n_turns_to_take):

        # word to speak this turn
        word_to_speak = word_to_be_spoken

        # what word to speak in the next turn?

        # The next turn's previous turn number is currently "turn_num".
        # If "word_to_speak" appears in "spoken_word_history", the turn number appearing in
        # "spoken_word_history" corresponds to a turn earlier than "turn_num".
        # That is: "turn_num" is the next turn's "previous turn", and "spoken_word_history"
        # holds information about the next turn's "previous, previous turn".
        # So if "word_to_speak" appears in "spoken_word_history", it is because it's appearance
        # during turn "turn_num" was not the first appearance of this "word_to_speak" value.
        if word_to_speak in spoken_word_history:
            word_to_be_spoken = turn_num - spoken_word_history[word_to_speak]
        else:
            word_to_be_spoken = 0
        spoken_word_history[word_to_speak] = turn_num
    return word_to_speak


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [int(x) for x in ifile.read().strip().split(",")]

    # part 1
    word = play_game(input_data, 2020)
    print(f"PART 1: 2020th number spoken: {word}")

    # part 2
    word = play_game(input_data, 30000000)
    print(f"PART 2: 30 millioonth spoken word: {word}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #15")
    parser.add_argument("input", help="Day #15 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
