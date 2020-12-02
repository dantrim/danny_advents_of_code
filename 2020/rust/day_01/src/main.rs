//
// Advent of Code Day 2020
// Day 01
//
// author: Daniel Joseph Antrim
// e-mail: dantrim1023 AT gmail DOT com
//

use clap::{App, Arg};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

extern crate itertools;
use itertools::Itertools;

fn read_data_from_file(path: &str) -> Vec<i32> {
    let v = BufReader::new(File::open(path).unwrap())
        .lines()
        .map(|line| line.unwrap().trim().parse::<i32>().unwrap())
        .collect();
    v
}

fn day01(input_data: &Vec<i32>, n_for_combination: u32) -> i32 {
    let product = input_data
        .into_iter()
        .combinations(n_for_combination as usize)
        .filter(|pair| pair.clone().into_iter().sum::<i32>() == 2020)
        .map(|pair| pair.into_iter().product::<i32>())
        .collect::<Vec<_>>();
    let product = match product.len() {
        1 => product[0],
        _ => {
            eprintln!(
                "ERROR: Found more than one {}-lengthed combinations that sum to 2020!",
                n_for_combination
            );
            std::process::exit(1);
        }
    };
    product
}

fn main() {
    let matches = App::new("AoC day #1, now in Rust!")
        .version("0")
        .author("Daniel Joseph Antrim")
        .about("AoC day 1")
        .arg(
            Arg::with_name("input")
                .help("Day #1 input *.txt file")
                .required(true)
                .index(1),
        )
        .get_matches();

    let input = matches.value_of("input").unwrap();
    if !Path::new(input).exists() {
        eprintln!("ERROR: bad input \"{}\"", input);
        std::process::exit(1);
    }

    let input_data = read_data_from_file(input);
    let product_part1 = day01(&input_data, 2);
    let product_part2 = day01(&input_data, 3);
    println!("product_part1: {}", product_part1);
    println!("product_part2: {}", product_part2);
}
