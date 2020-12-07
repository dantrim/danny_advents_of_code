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

import pytest


@pytest.fixture
def example_rule():
    return "light red bags contain 1 bright white bag, 2 muted yellow bags."


@pytest.fixture
def example_rules_1():
    test_data = """
   light red bags contain 1 bright white bag, 2 muted yellow bags.
   dark orange bags contain 3 bright white bags, 4 muted yellow bags.
   bright white bags contain 1 shiny gold bag.
   muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
   shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
   dark olive bags contain 3 faded blue bags, 4 dotted black bags.
   vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
   faded blue bags contain no other bags.
   dotted black bags contain no other bags.
   """
    return [x.strip() for x in test_data.split("\n") if x != ""]


@pytest.fixture
def example_rules_2():
    test_data = """
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.
    """
    return [x.strip() for x in test_data.split("\n") if x != ""]


def test_example_1(example_rules_1):
    all_bags = get_bags_from_rules(example_rules_1)
    assert len(trace_up(all_bags, all_bags["shiny gold"])) == 4


def test_example_2(example_rules_2):
    all_bags = get_bags_from_rules(example_rules_2)
    assert trace_down(all_bags, all_bags["shiny gold"]) == 126


class Bag:
    def __init__(self, color=""):
        # something like a linked list element
        self.color = color
        self.can_hold = {}  # name and count of bags it can hold
        self.held_by = set()  # list of bag types that can hold this bag

    def __str__(self):
        return f"Bag[{self.color}]: can hold: {self.can_hold}, held by: {self.held_by}"

    def n_bags_can_hold(self):
        n = 0
        for bag_type, bag_count in self.can_hold.items():
            n += bag_count
        return n

    def holds_nothing(self):
        return not self.can_hold

    def is_held_by_something(self):
        return len(self.held_by) > 0


def get_held_bag_count_and_color(held_bag: str) -> list:
    held_bag = held_bag.strip()

    fields = held_bag.split()
    count = 0
    if fields[0].isdigit():
        count = int(fields[0])
    else:
        return 0, ""

    bag_type = " ".join(fields[1:])
    idx = bag_type.find("bag")
    if idx < 0:
        print(f"ERROR: Bag string is of unexpected format: {held_bag}")
        sys.exit(1)
    bag_color = bag_type[0:idx].strip()
    return count, bag_color


def get_bag_from_rule(rule: str) -> Bag:
    rule = rule.strip()
    holder_bag, contained_bags = (
        rule.split("contain")[0].strip(),
        rule.split("contain")[1].strip(),
    )

    idx = holder_bag.find("bags")
    if idx < 0:
        print(f"ERROR: Holder bag string is of unexpected format: {holder_bag}")
    holder_color = holder_bag[0:idx].strip()

    contained_bags_list = [x.strip() for x in contained_bags.split(",")]
    holder_bag = Bag(holder_color)
    for contained_bag in contained_bags_list:
        count, bag = get_held_bag_count_and_color(contained_bag)
        if bag in holder_bag.can_hold:
            print(f"ERROR: Bag {bag} already appears in holder bag {holder_color}!")
            sys.exit(1)
        if count > 0:
            holder_bag.can_hold[bag] = count
    return holder_bag


def get_bags_from_rules(rules_list: list) -> list:
    all_bags = {}
    for irule, rule in enumerate(rules_list):
        rule = rule.strip()
        if not rule:
            continue
        holder_bag = get_bag_from_rule(rule)
        if holder_bag.color in all_bags:
            print(f"ERROR: Bag {holder_bag.color} already appears in all_bags dict")
            print(
                f"ERROR: --> all_bags[{holder_bag.color}] = {all_bags[holder_bag.color]}"
            )
            print(f"ERROR: --> this bag = {holder_bag}")
            sys.exit(1)
        all_bags[holder_bag.color] = holder_bag

    # could probably  fill the list of "held_by" at the same time as in the above
    # loop, but would have to check for filing up the held_by and can_hold lists/dicts
    # a bit more, and i'm lazy
    for bag_type, holder_bag in all_bags.items():
        for held_bag_type in holder_bag.can_hold:
            if held_bag_type not in all_bags:
                print(
                    f"ERROR: A holder bag of type {bag_type} holds bag of type {held_bag_type} which is not in 'all_bags' dict!"
                )
                sys.exit(1)
            all_bags[held_bag_type].held_by.add(bag_type)
    return all_bags


def trace_up(all_bags, bag):
    """
    For the input bag "bag", trace the path upwards along all of it's parents,
    which are the bags that can  hold it.
    """
    parents = []
    if len(bag.held_by) == 0:
        return parents

    for bag_type in bag.held_by:
        parents.append(bag_type)
        held_bag = all_bags[bag_type]
        for parent in trace_up(all_bags, held_bag):
            parents.append(parent)
    return list(set(parents))


def trace_down(all_bags, bag):
    """
    For the input bag "bag", trace down the path along all of it's bags that it
    can hold and count them.
    """
    n = 0  # number of children seen at this level
    if len(bag.can_hold) == 0:
        return n
    for bag_type, n_can_hold in bag.can_hold.items():
        child_bag = all_bags[bag_type]
        for i in range(n_can_hold):
            n += 1  # count once for the child at this level
            n += trace_down(
                all_bags, child_bag
            )  # counts for all children at lower levels
    return n


def main(input_path):
    with open(input_path, "r") as infile:
        all_rules = infile.readlines()
    all_bags = get_bags_from_rules(all_rules)
    print(f"Found {len(all_bags)} bag types")

    # part 1
    shiny_gold_parents = trace_up(all_bags, all_bags["shiny gold"])
    print(f'PART 1: {len(shiny_gold_parents)} "shiny gold" parents')

    # part 2
    n_shiny_gold_children = trace_down(all_bags, all_bags["shiny gold"])
    print(f"PART 2: Number of shiny gold children: {n_shiny_gold_children}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #7")
    parser.add_argument("input", help="Day #7 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
