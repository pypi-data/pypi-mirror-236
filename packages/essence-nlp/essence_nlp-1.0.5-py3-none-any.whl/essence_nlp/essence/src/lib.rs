extern crate env_logger;
extern crate libc;
extern crate log;
extern crate regex;
extern crate serde;
extern crate serde_json;
extern crate symspell;

extern crate serde_derive;
use log::error;
use nlprule::{Rules, Tokenizer};
use rake::*;
use regex::Regex;
use std::collections::HashSet;
use std::ffi::{CStr, CString};
use std::fs::File;
use std::io::{self, BufRead};
use std::os::raw::c_char;
use std::path::Path;
use std::path::PathBuf;
use symspell::{SymSpell, UnicodeStringStrategy};

static RE: once_cell::sync::Lazy<Regex> =
    once_cell::sync::Lazy::new(|| Regex::new(r"[^a-zA-Z0-9\s]").unwrap());

#[no_mangle]
pub extern "C" fn get_keywords(input_ptr: *const c_char) -> *mut c_char {
    // Initialize logger
    let _ = env_logger::builder().is_test(true).try_init();

    // Convert input_ptr to a Rust string
    let c_str = unsafe { CStr::from_ptr(input_ptr) };
    match c_str.to_str() {
        Ok(r_str) => {
            // Initialize SymSpell for spelling correction
            let mut symspell: SymSpell<UnicodeStringStrategy> = SymSpell::default();
            let dictionary_path = get_resource_path("data/frequency_dictionary_en_82_765.txt");
            let tokenizer_path = get_resource_path("rules/en_tokenizer.bin");
            let rules_path = get_resource_path("rules/en_rules.bin");
            let stopword_path = get_resource_path("data/stopwords.txt");
            symspell.load_dictionary(dictionary_path.to_str().unwrap(), 0, 1, " ");

            // Create tokenizer for grammar correction
            let tokenizer = match Tokenizer::new(
                tokenizer_path.to_str().unwrap(),
            ) {
                Ok(tokenizer) => tokenizer,
                Err(err) => {
                    eprintln!("Failed to create tokenizer: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Create rules for grammar correction
            let rules = match Rules::new(
                rules_path.to_str().unwrap(),
            ) {
                Ok(rules) => rules,
                Err(err) => {
                    eprintln!("Failed to create rules: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Perform spelling correction
            let spelling_result = symspell.lookup_compound(&r_str, 2);
            let corrected_spelling = match spelling_result.first() {
                Some(suggestion) => suggestion.term.clone(),
                None => r_str.to_string(),
            };

            // Perform grammar correction
            let corrected_text = rules.correct(&corrected_spelling, &tokenizer);

            let lowercase_text = corrected_text.to_lowercase();

            // Remove symbols from the corrected text
            let text_no_punc = RE.replace_all(&lowercase_text, "").to_string();

            // Load stop words for keyword extraction
            let sw = StopWords::from_file(stopword_path.to_str().unwrap()).unwrap();
            let r = Rake::new(sw);

            // Extract keywords from the text
            let keywords = r.run(&text_no_punc);

            // Format keywords and scores into a single string
            let keywords_string = keywords
                .iter()
                .map(
                    |&KeywordScore {
                         ref keyword,
                         ref score,
                     }| { format!("{}: {}", keyword, score) },
                )
                .collect::<Vec<String>>()
                .join("\n");

            // Convert the result to a CString to return to Python
            let c_final_str = CString::new(keywords_string).expect("Failed to create CString");
            c_final_str.into_raw()
        }
        Err(_) => {
            error!("UTF-8 validation error");
            std::ptr::null_mut() // Return null pointer on UTF-8 validation error
        }
    }
}

#[no_mangle]
pub extern "C" fn get_corrected(input_ptr: *const c_char) -> *mut c_char {
    // Initialize logger
    let _ = env_logger::builder().is_test(true).try_init();

    // Convert input_ptr to a Rust string
    let c_str = unsafe { CStr::from_ptr(input_ptr) };
    match c_str.to_str() {
        Ok(r_str) => {
            // Initialize SymSpell for spelling correction
            let mut symspell: SymSpell<UnicodeStringStrategy> = SymSpell::default();
            let dictionary_path = get_resource_path("data/frequency_dictionary_en_82_765.txt");
            let tokenizer_path = get_resource_path("rules/en_tokenizer.bin");
            let rules_path = get_resource_path("rules/en_rules.bin");
            symspell.load_dictionary(
                dictionary_path.to_str().unwrap(),
                0,
                1,
                " ",
            );

            // Create tokenizer for grammar correction
            let tokenizer = match Tokenizer::new(
                tokenizer_path.to_str().unwrap(),
            ) {
                Ok(tokenizer) => tokenizer,
                Err(err) => {
                    eprintln!("Failed to create tokenizer: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Create rules for grammar correction
            let rules = match Rules::new(
                rules_path.to_str().unwrap(),
            ) {
                Ok(rules) => rules,
                Err(err) => {
                    eprintln!("Failed to create rules: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Perform spelling correction
            let spelling_result = symspell.lookup_compound(&r_str, 2);
            let corrected_spelling = match spelling_result.first() {
                Some(suggestion) => suggestion.term.clone(),
                None => r_str.to_string(),
            };

            // Perform grammar correction
            let corrected_text = rules.correct(&corrected_spelling, &tokenizer);

            let lowercase_text = corrected_text.to_lowercase();

            // Convert the result to a CString to return to Python
            let c_final_str = CString::new(lowercase_text).expect("Failed to create CString");
            c_final_str.into_raw()
        }
        Err(_) => {
            error!("UTF-8 validation error");
            std::ptr::null_mut() // Return null pointer on UTF-8 validation error
        }
    }
}

#[no_mangle]
pub extern "C" fn get_cleaned(input_ptr: *const c_char) -> *mut c_char {
    // Initialize logger
    let _ = env_logger::builder().is_test(true).try_init();

    // Convert input_ptr to a Rust string
    let c_str = unsafe { CStr::from_ptr(input_ptr) };
    match c_str.to_str() {
        Ok(r_str) => {
            // Initialize SymSpell for spelling correction
            let mut symspell: SymSpell<UnicodeStringStrategy> = SymSpell::default();
            let dictionary_path = get_resource_path("data/frequency_dictionary_en_82_765.txt");
            let tokenizer_path = get_resource_path("rules/en_tokenizer.bin");
            let rules_path = get_resource_path("rules/en_rules.bin");
            let stopword_path = get_resource_path("data/stopwords.txt");
            symspell.load_dictionary(
                dictionary_path.to_str().unwrap(),
                0,
                1,
                " ",
            );

            // Create tokenizer for grammar correction
            let tokenizer = match Tokenizer::new(
                tokenizer_path.to_str().unwrap(),
            ) {
                Ok(tokenizer) => tokenizer,
                Err(err) => {
                    eprintln!("Failed to create tokenizer: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Create rules for grammar correction
            let rules = match Rules::new(
                rules_path.to_str().unwrap(),
            ) {
                Ok(rules) => rules,
                Err(err) => {
                    eprintln!("Failed to create rules: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Perform spelling correction
            let spelling_result = symspell.lookup_compound(&r_str, 2);
            let corrected_spelling = match spelling_result.first() {
                Some(suggestion) => suggestion.term.clone(),
                None => r_str.to_string(),
            };

            // Perform grammar correction
            let corrected_text = rules.correct(&corrected_spelling, &tokenizer);

            let lowercase_text = corrected_text.to_lowercase();

            // Remove symbols from the corrected text
            let text_no_punc = RE.replace_all(&lowercase_text, "").to_string();

            
            let stopwords = match load_stopwords(stopword_path) {
                Ok(stopwords) => stopwords,
                Err(err) => {
                    eprintln!("Failed to load stopwords: {}", err);
                    return std::ptr::null_mut();
                }
            };

            // Remove stopwords from the text
            let cleaned_text = text_no_punc
                .split_whitespace()
                .filter(|word| !stopwords.contains(*word))
                .collect::<Vec<&str>>()
                .join(" ");

            // Convert the result to a CString to return to Python
            let c_final_str = CString::new(cleaned_text).expect("Failed to create CString");
            c_final_str.into_raw()
        }
        Err(_) => {
            error!("UTF-8 validation error");
            std::ptr::null_mut() // Return null pointer on UTF-8 validation error
        }
    }
}

fn load_stopwords<P: AsRef<Path>>(path: P) -> io::Result<HashSet<String>> {
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let stopwords = reader
        .lines()
        .filter_map(Result::ok)
        .collect::<HashSet<String>>();
    Ok(stopwords)
}

fn get_resource_path(resource: &str) -> PathBuf {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("resources");
    path.push(resource);
    path
}

#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    unsafe {
        if !s.is_null() {
            let _ = CString::from_raw(s);
        }
    }
}