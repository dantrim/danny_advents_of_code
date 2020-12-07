#!/bin/env python

#
# Advent of Code 2020
# Day 07
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

# import pytest

if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #7")
    parser.add_argument("input", help="Day #7 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    pass
