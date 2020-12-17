#!/bin/env python

#
# Advent of Code 2020
# Day 17
#
# author: Daniel Joseph Antrim
# e-mail: dantrim1023 AT gmail DOT com
#

import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np


def pos2num(cube_char):
    return {"#": 1, ".": 0}[cube_char]


def find_active_neighbors(point, space):

    x, y, z = point
    position_indices = np.arange(-1, 2, 1)
    active_count = 0
    for dz in position_indices:
        for dx in position_indices:
            for dy in position_indices:
                if (dx, dy, dz) == (0, 0, 0):
                    continue
                try:
                    x_pos = x + dx
                    y_pos = y + dy
                    z_pos = z + dz
                    if x_pos < 0 or y_pos < 0 or z_pos < 0:
                        continue
                    neighbor = int(space[x_pos, y_pos, z_pos])
                    if neighbor == 1:
                        active_count += 1
                except IndexError:
                    continue
    return active_count


def apply_rules(space, width):

    updates = []
    for z in range(0, width):
        for y in range(0, width):
            for x in range(0, width):
                n_active_neighbors = find_active_neighbors([x, y, z], space)
                if n_active_neighbors > 0:
                    current_is_active = int(space[x, y, z]) == 1
                    if current_is_active:
                        if n_active_neighbors in [2, 3]:
                            pass
                        else:
                            updates.append([(x, y, z), 0])
                    else:
                        if n_active_neighbors == 3:
                            updates.append([(x, y, z), 1])
                else:
                    updates.append([(x, y, z), 0])
    for update in updates:
        x, y, z = update[0]
        space[x, y, z] = update[1]


def find_active_neighbors_4d(point, space):

    x, y, z, t = point
    position_indices = np.arange(-1, 2, 1)
    active_count = 0
    for dz in position_indices:
        for dx in position_indices:
            for dy in position_indices:
                for dt in position_indices:
                    if (dx, dy, dz, dt) == (0, 0, 0, 0):
                        continue
                    try:
                        x_pos = x + dx
                        y_pos = y + dy
                        z_pos = z + dz
                        t_pos = t + dt
                        if x_pos < 0 or y_pos < 0 or z_pos < 0 or t_pos < 0:
                            continue
                        neighbor = int(space[x_pos, y_pos, z_pos, t_pos])
                        if neighbor == 1:
                            active_count += 1
                    except IndexError:
                        continue
    return active_count


def apply_rules_4d(space, width_x_y, width_z_t):

    updates = []
    for z in range(0, width_z_t):
        for y in range(0, width_x_y):
            for x in range(0, width_x_y):
                for t in range(0, width_z_t):
                    n_active_neighbors = find_active_neighbors_4d([x, y, z, t], space)
                    if n_active_neighbors > 0:
                        current_is_active = int(space[x, y, z, t]) == 1
                        if current_is_active:
                            if n_active_neighbors in [2, 3]:
                                pass
                            else:
                                updates.append([(x, y, z, t), 0])
                        else:
                            if n_active_neighbors == 3:
                                updates.append([(x, y, z, t), 1])
                    else:
                        updates.append([(x, y, z, t), 0])
    for update in updates:
        x, y, z, t = update[0]
        space[x, y, z, t] = update[1]


def main(input_path):

    with open(input_path, "r") as ifile:
        input_data = [x.strip() for x in ifile.readlines()]

    # This is HORRIBLY HORRIBLY inefficient.. BUUUT it's easy and i can let it run during a meeting :)
    # I should probably serialize out (by coordinate) only those elements I care about, and
    # keep track of coordinates only (rather than an entire 3/4D very large and very sparse space). That
    # would reduce the memory footprint at least an order of magnitude.

    width = 25
    x0, y0, z0 = width // 2, width // 2, width // 2
    space = np.zeros((width, width, width), dtype=int)
    for i, row in enumerate(input_data):
        for y, col in enumerate(row):
            space[x0 + i, y0 + y, z0] = int(pos2num(col))
    for _ in range(0, 6):
        apply_rules(space, width)
    n_active = np.count_nonzero(space == 1)
    print(f"PART1: n active after 6 cycles: {n_active}")

    # width_x_y = 35
    # width_z_t = 20
    # x0, y0, z0, t0 = width_x_y//2, width_x_y//2, width_z_t//2, width_z_t//2
    # space = np.zeros((width_x_y, width_x_y, width_z_t, width_z_t), dtype = np.dtype('u1'))
    # for i, row in enumerate(input_data) :
    #    for y, col in enumerate(row) :
    #        space[x0+i, y0+y, z0, t0] = int(pos2num(col))
    # for _ in range(0,6):
    #    apply_rules_4d(space, width_x_y, width_z_t)
    # n_active = np.count_nonzero(space==1)
    # print(f"PART2: n active after 6 cycles: {n_active}")


if __name__ == "__main__":
    parser = ArgumentParser(description="AoC day #17")
    parser.add_argument("input", help="Day #17 input file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: bad input '{args.input}'")
        sys.exit(1)
    main(input_path)
