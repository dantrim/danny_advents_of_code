//
// Advent of Code 2020
// Day 02
//
// author: Daniel Joseph Antrim
// e-mail: dantrim1023 AT gmail DOT com
//

use clap::{App, Arg};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn read_data_from_file(path: &str) -> Vec<String> {
    BufReader::new(File::open(path).unwrap())
        .lines()
        .map(|line| line.expect("Could not parse line"))
        .collect()
}

#[derive(Debug)]
struct DBEntry<'a> {
    min: i32,
    max: i32,
    character: &'a str,
    password: &'a str,
}

fn unpack_db_entry(db_entry: &str) -> DBEntry {
    let entry_split = db_entry.split(":").collect::<Vec<&str>>();
    let requirements = entry_split[0];
    let password = entry_split[1].trim();
    let requirements = requirements
        .split(" ")
        .map(|x| x.trim())
        .collect::<Vec<&str>>();
    let character = requirements[1].trim();
    let counts = requirements[0]
        .split("-")
        .map(|count| count.trim().parse::<i32>().unwrap())
        .collect::<Vec<i32>>();
    DBEntry {
        min: counts[0],
        max: counts[1],
        character: character,
        password: password,
    }
}

fn db_entries_from_input(input_data: &Vec<String>) -> Vec<DBEntry> {
    input_data
        .into_iter()
        .map(|db_entry| unpack_db_entry(db_entry.as_str()))
        .collect()
}

fn is_good_entry_part1(entry: &DBEntry) -> bool {
    let occurrences = entry.password.matches(entry.character).count() as i32;
    let valid_occurrences = (entry.min..entry.max + 1).collect::<Vec<i32>>();
    valid_occurrences.iter().any(|&i| i == occurrences)
}

fn n_good_part1(db_entries: &Vec<DBEntry>) -> u32 {
    db_entries
        .into_iter()
        .filter(|entry| is_good_entry_part1(&entry))
        .collect::<Vec<&DBEntry>>()
        .len() as u32
}

fn is_good_entry_part2(entry: &DBEntry) -> bool {
    (entry
        .password
        .chars()
        .nth((entry.min - 1) as usize)
        .unwrap()
        == entry.character.chars().nth(0).unwrap())
        ^ (entry
            .password
            .chars()
            .nth((entry.max - 1) as usize)
            .unwrap()
            == entry.character.chars().nth(0).unwrap())
}

fn n_good_part2(db_entries: &Vec<DBEntry>) -> u32 {
    db_entries
        .into_iter()
        .filter(|entry| is_good_entry_part2(&entry))
        .collect::<Vec<&DBEntry>>()
        .len() as u32
}

fn day02(input_data: &Vec<String>) {
    let db_entries = db_entries_from_input(&input_data);
    let n_good_part1 = n_good_part1(&db_entries);
    let n_good_part2 = n_good_part2(&db_entries);
    println!("n good part 1: {}", n_good_part1);
    println!("n good part 2: {}", n_good_part2);
}

fn main() {
    let matches = App::new("AoC day #2, Rust edition")
        .version("0")
        .author("Daniel Joseph Antrim")
        .about("AoC day 2")
        .arg(
            Arg::with_name("input")
                .help("Day #2 input *.txt file")
                .required(true),
        )
        .get_matches();

    let input = matches.value_of("input").unwrap();
    if !Path::new(input).exists() {
        eprintln!("ERROR: bad input \"{}\"", input);
        std::process::exit(1);
    }
    let input_data = read_data_from_file(input);
    day02(&input_data);
}
