//
// Advent of Code 2020
// Day 03
//
// author: Daniel Joseph Antrim
// e-mail: dantrim1023 AT gmail DOT com
//

use clap::{App, Arg};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use array2d::Array2D;

fn load_forest(path: &str) -> Array2D<char> {
    // I am not yet familiar enough with ndarray/Array2D to figure out how best
    // to convert vectors into matrices in rust...
    let mut forest = vec![];
    let forest_row_strings: Vec<String> = BufReader::new(File::open(path).unwrap())



        .lines()
        .map(|line| line.expect("Could not parse line"))
        .collect();

    let mut forest_row_width: i32 = -1;
    for (irow, forest_row) in forest_row_strings.iter().enumerate() {
        if forest_row_width < 0 {
            forest_row_width = forest_row.chars().count() as i32;
        }
        if forest_row.chars().count() != forest_row_width as usize {
            eprintln!(
                "ERROR: Abnormal forest row width encountered at row {}",
                irow
            );
            std::process::exit(1);
        }
        let mut v: Vec<char> = vec![];
        for c in forest_row.chars() {
            v.push(c);
        }
        forest.push(v);
    }
    let forest = Array2D::from_rows(&forest);
    forest
}

fn traverse_slope(full_forest: &Array2D<char>, right_step: usize, down_step: usize) -> u32 {
    let mut n_trees = 0;
    for (istep, forest_row) in full_forest.rows_iter().step_by(down_step).enumerate() {
        let characters = forest_row.map(|c| c).collect::<Vec<&char>>();
        let width = characters.len();
        match characters[(right_step * istep) % width] {
            '#' => n_trees = n_trees + 1,
            _ => (),
        }
    }
    n_trees
}

fn main() {
    let matches = App::new("AoC day #3, Rust edition")
        .version("0")
        .author("Daniel Joseph Antrim")
        .about("AoC day 3")
        .arg(
            Arg::with_name("input")
                .help("Day #3 input *.txt file")
                .required(true),
        )
        .get_matches();
    let input = matches.value_of("input").unwrap();
    if !Path::new(input).exists() {
        eprintln!("ERROR: bad input \"{}\"", input);
        std::process::exit(1);
    }
    let full_forest = load_forest(input);

    // part 1
    let n_trees_encountered: u32 = traverse_slope(&full_forest, 3, 1);
    println!(
        "PART 1: Number of trees encountered  : {}",
        n_trees_encountered
    );

    // part 2
    let slopes_to_consider = vec![[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]];
    let mut encountered_trees: Vec<u32> = vec![];
    for slope_to_consider in slopes_to_consider.iter() {
        encountered_trees.push(traverse_slope(
            &full_forest,
            slope_to_consider[0],
            slope_to_consider[1],
        ));
    }
    println!(
        "PART 2: Encountered trees            : {:?}",
        encountered_trees
    );
    println!(
        "PART 2: Product of encountered trees : {}",
        encountered_trees.iter().product::<u32>()
    );
}
