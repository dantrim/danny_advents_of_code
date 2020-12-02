#!/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path
import numpy as np


def unpack_db_entry(db_entry):
    """
    Takes a DB entry and returns the password itself,
    and breaks apart the requirements (the required character,
    and the min/max number of times that character must appear
    in the password).

    Args:
        db_entry [str] : DB entry, format: <min>-<max> <character>: <password>

    Returns:
        <min>[int], <max>[int], <character>[str], <password>[str]
    """
    requirements, password = (
        db_entry.split(":")[0].strip(),
        db_entry.split(":")[1].strip(),
    )
    min_required, max_required, letter_required = (
        int(requirements.split()[0].split("-")[0]),
        int(requirements.split()[0].split("-")[1]),
        requirements.split()[1],
    )
    return min_required, max_required, letter_required, password


def is_good_password_part1(db_entry):
    """
    Classify the DB entry following Part 1.
    The DB entry of the format <min>-<max> <character>: <password>
    describes the requirement that the specific character <character>
    must appear >= <min> or <= <max> times in the <password>.
    """
    min_required, max_required, letter_required, password = unpack_db_entry(db_entry)
    valid_occurrences = np.arange(min_required, max_required + 1, 1)
    if password.count(letter_required) in valid_occurrences:
        return True
    else:
        return False


def is_good_password_part2(db_entry):
    """
    Classify the DB entry following Part 2.
    The DB entry of the format <min>-<max> <character>: <password>
    describes the requirement that the specific character must
    appear at either position <min> OR position <max>, but not BOTH,
    in the <password> string. The string indexing starts at 1, so
    array index 0 is password character position (specified by the positions
    <min> and <max>) 1.
    """
    first_loc, second_loc, character, password = unpack_db_entry(db_entry)
    first_passes = password[first_loc - 1] == character
    second_passes = password[second_loc - 1] == character
    return first_passes ^ second_passes  # xor


def main(input_path):

    good_entries_part1, bad_entries_part1 = [], []
    good_entries_part2, bad_entries_part2 = [], []

    n_entries_total = 0
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            n_entries_total += 1

            # part1 classification
            if is_good_password_part1(line):
                good_entries_part1.append(line)
            else:
                bad_entries_part1.append(line)

            # part2 classification
            if is_good_password_part2(line):
                good_entries_part2.append(line)
            else:
                bad_entries_part2.append(line)

    n_entries_classified = len(good_entries_part1) + len(bad_entries_part1)
    if n_entries_classified != n_entries_total:
        print(
            f"ERROR[PART 1]: Failed to classify {n_entries_total - n_entries_classified} DB entries!"
        )
        sys.exit(1)
    n_entries_classified = len(good_entries_part2) + len(bad_entries_part2)
    if n_entries_classified != n_entries_total:
        print(
            f"ERROR[PART 2]: Failed to classify {n_entries_total - n_entries_classified} DB entries!"
        )
        sys.exit(1)

    print(
        f"PART 1: # of good db entries = {len(good_entries_part1)}, # of bad db entries = {len(bad_entries_part1)}"
    )
    print(
        f"PART 2: # of good db entries = {len(good_entries_part2)}, # of bad db entries = {len(bad_entries_part2)}"
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #2")
    parser.add_argument("input", help="Day #2 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f'ERROR: bad input "{args.input}"')
        sys.exit(1)
    main(input_path)
