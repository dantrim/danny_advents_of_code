#!/bin/env python

#
# Advent of Code 2020
# Day 04
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path


class PassPort:
    def __init__(self, num, lines):
        self.num = num
        self.entries = {
            "byr": "",
            "iyr": "",
            "eyr": "",
            "hgt": "",
            "hcl": "",
            "ecl": "",
            "pid": "",
            "cid": "",
        }
        self._fields = sorted(self.entries.keys())
        self._lines = lines
        self._load(lines)

    def __str__(self):
        return f"PassPort[{self.num:03d}] {self.entries}"

    def _load(self, lines):
        for line in lines:
            data = line.split()
            input_fields = dict(
                zip(
                    [x.split(":")[0].strip() for x in data],
                    [x.split(":")[1].strip() for x in data],
                )
            )
            for expected_field in self._fields:
                if expected_field in input_fields:
                    self.entries[expected_field] = input_fields[expected_field]


def passport_is_valid(passport):
    missing_fields = []
    for field, entry in passport.entries.items():
        if not entry:
            missing_fields.append(field)
    if "cid" in missing_fields:
        missing_fields.remove("cid")
    return len(missing_fields) == 0


def load_passports_from_input(input_path):

    passports = []
    passport_num = 0
    with open(input_path, "r") as infile:
        passport_lines = []
        for iline, line in enumerate(infile):
            if line.strip():
                passport_lines.append(line.strip())
            else:
                passports.append(PassPort(passport_num, passport_lines))
                passport_num += 1
                passport_lines = []
    return passports


def main(input_path):
    passports = load_passports_from_input(input_path)
    print(f"N loaded passports : {len(passports)}")
    valid_passports = list(filter(lambda x: passport_is_valid(x), passports))
    print(f"PART 1: N valid: {len(valid_passports)}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #4")
    parser.add_argument("input", help="Day #4 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
