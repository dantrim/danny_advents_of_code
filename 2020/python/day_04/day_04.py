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
import re
import numpy as np


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


def passport_is_valid_part1(passport):
    missing_fields = []
    for field, entry in passport.entries.items():
        if field == "cid":
            continue
        if not entry:
            missing_fields.append(field)
    return len(missing_fields) == 0


def passport_is_valid_part2(passport):

    rules = {
        "byr": lambda x: (
            re.search("^[0-9]{4}$", x) is not None
            and int(x) in np.arange(1920, 2002 + 1, 1)
        ),
        "iyr": lambda x: (
            re.search("^[0-9]{4}$", x) is not None
            and int(x) in np.arange(2010, 2020 + 1, 1)
        ),
        "eyr": lambda x: (
            re.search("^[0-9]{4}$", x) is not None
            and int(x) in np.arange(2020, 2030 + 1, 1)
        ),
        "hgt": lambda x: (
            (
                re.search("^\d{1,3}cm$", x) is not None
                and int(x.replace("cm", "")) in np.arange(150, 193 + 1, 1)
            )
            or (
                re.search("^\d{1,2}in$", x) is not None
                and int(x.replace("in", "")) in np.arange(59, 76 + 1, 1)
            )
        ),
        "hcl": lambda x: re.search("^#[0-9a-f]{6}$", x) is not None,
        "ecl": lambda x: (
            len(x) == 3 and x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        ),
        "pid": lambda x: re.search("^\d{9}$", x) is not None,
        "cid": lambda x: True,
    }

    for field_name, rule in rules.items():
        if field_name == "cid":
            continue
        if field_name in passport.entries and passport.entries[field_name] != "":
            if not rule(passport.entries[field_name]):
                return False
        elif field_name in passport.entries and passport.entries[field_name] == "":
            return False
    return True


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
        if len(passport_lines) != 0:
            passports.append(PassPort(passport_num, passport_lines))
    return passports


def main(input_path):
    passports = load_passports_from_input(input_path)
    print(f"N loaded passports : {len(passports)}")
    valid_passports = list(filter(lambda x: passport_is_valid_part1(x), passports))
    print(f"PART 1: N valid: {len(valid_passports)}")

    # part 2
    valid_passports_2 = list(filter(lambda x: passport_is_valid_part2(x), passports))
    print(f"PART 2: N valid: {len(valid_passports_2)}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #4")
    parser.add_argument("input", help="Day #4 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
