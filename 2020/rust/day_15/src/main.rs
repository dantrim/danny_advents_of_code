use std::collections::HashMap;

fn play_game(game_input: &Vec<u32>, n_turns_to_take: u32) -> u32 {
    if n_turns_to_take < game_input.len() as u32 {
        eprintln!("ERROR: n_turns_to_take < game input length!");
        std::process::exit(1);
    }

    let mut word_to_be_spoken: u32 = 0;
    let mut spoken_word_history: HashMap<u32, u32> = HashMap::new();

    for (turn_num, val) in game_input.into_iter().enumerate() {
        spoken_word_history.insert(*val, turn_num as u32);
    }

    let mut word_to_speak: u32 = word_to_be_spoken;
    for turn_num in (game_input.len() as u32)..(n_turns_to_take as u32) {
        word_to_speak = word_to_be_spoken;
        if spoken_word_history.contains_key(&word_to_speak) {
            word_to_be_spoken = turn_num - spoken_word_history.get(&word_to_speak).unwrap();
        } else {
            word_to_be_spoken = 0
        }
        spoken_word_history.insert(word_to_speak, turn_num);
    }
    word_to_speak
}
fn main() {
    let input_data: Vec<u32> = vec![0, 20, 7, 16, 1, 18, 15];
    let last_spoken_word = play_game(&input_data, 30000000);
    println!("Last spoken word: {}", last_spoken_word);
}
