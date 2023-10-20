use gtokenizers::models::region::Region;
use gtokenizers::models::region_set::RegionSet;
use gtokenizers::tokenizers::traits::{Tokenizer, PAD_CHR, PAD_END, PAD_START};
use gtokenizers::tokenizers::TreeTokenizer;
use std::path::Path;

use rstest::rstest;
use rstest::fixture;


#[fixture]
fn tokenizer() -> TreeTokenizer {
    let bed_file = Path::new("tests/data/peaks.bed");
    TreeTokenizer::from(bed_file)
}

#[fixture]
fn vocab_length() -> usize {
    6553 // 6551 regions + 1 unknown token + 1 pad token
}

#[fixture]
fn vocab_length_no_specials() -> usize {
    6551 // 6551 regions
}

#[rstest]
fn test_make_tokenizer(tokenizer: TreeTokenizer, vocab_length: usize) {
    // make sure the tree got made, and the universe is there, check for unknown token
    assert_eq!(tokenizer.tree.len(), 25); // 23 chromosomes + 1 unknown token + 1 pad token
    assert_eq!(tokenizer.universe.regions.len(), vocab_length); // 6551 regions
    assert_eq!(tokenizer.universe.region_to_id.len(), vocab_length); // 6551 regions + 1 unknown token + 1 pad token
}

#[rstest]
fn test_universe_len(tokenizer: TreeTokenizer, vocab_length: usize) {
    assert_eq!(tokenizer.universe.len(), vocab_length as u32); // 6551 regions + 1 unknown token + 1 pad token
}

#[rstest]
fn test_tokenize_region(tokenizer: TreeTokenizer) {
    
    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 151399383,
        end: 151399479,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();
    assert_eq!(tokenized_regions.len(), 1);
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].chr,
        "chr1"
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].start,
        151399431
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].end,
        151399527
    );
    assert_eq!(tokenized_regions.into_iter().collect::<Vec<_>>()[0].id, 6);
}

#[rstest]
fn test_pad_tokenization_result(tokenizer: TreeTokenizer) {
    
    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 151399383,
        end: 151399479,
    };

    let mut tokenized_regions = tokenizer.tokenize_region(&region).unwrap();
    assert!(tokenized_regions.len() == 1);

    // pad them
    tokenized_regions.pad(10);
    assert!(tokenized_regions.len() == 10);
}

#[rstest]
fn test_batch_tokenization(tokenizer: TreeTokenizer) {
    // tokenizers to:
    // chr1	151399431	151399527
    let region1 = Region {
        chr: "chr1".to_string(),
        start: 151399383,
        end: 151399479,
    };

    // tokenizes to:
    // chr9	3526071	3526165
    // chr9	3526183	3526269
    let region2 = Region {
        chr: "chr9".to_string(),
        start: 3526051,
        end: 3526289,
    };

    let region_sets = vec![
        RegionSet::from(vec![region1]),
        RegionSet::from(vec![region2]),
    ];
    let result = tokenizer.tokenize_region_set_batch(&region_sets).unwrap();

    // all tokenization results should be the same length
    // and the first should have been padded
    assert_eq!(result[0].len(), result[1].len());
    assert_eq!(result[0].into_iter().collect::<Vec<_>>()[0].chr, "chr1");
    assert_eq!(
        result[0].into_iter().collect::<Vec<_>>()[0].start,
        151399431
    );
    assert_eq!(result[0].into_iter().collect::<Vec<_>>()[0].end, 151399527);
    assert_eq!(result[0].into_iter().collect::<Vec<_>>()[1].chr, PAD_CHR);
    assert_eq!(
        result[0].into_iter().collect::<Vec<_>>()[1].start,
        PAD_START as u32
    );
    assert_eq!(
        result[0].into_iter().collect::<Vec<_>>()[1].end,
        PAD_END as u32
    );
}

#[rstest]
fn test_get_unknown_region(tokenizer: TreeTokenizer, vocab_length_no_specials: usize) {

    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 10,
        end: 11,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    assert_eq!(tokenized_regions.len(), 1);
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].chr,
        "chrUNK"
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].start,
        0
    );
    assert_eq!(tokenized_regions.into_iter().collect::<Vec<_>>()[0].end, 0);
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].id,
        vocab_length_no_specials as u32
    );
}

#[rstest]
fn test_one_region_to_many_tokens(tokenizer: TreeTokenizer) {
    
    // chr9	3526071	3526165
    // chr9	3526183	3526269
    let region = Region {
        chr: "chr9".to_string(),
        start: 3526051,
        end: 3526289,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    assert_eq!(tokenized_regions.len(), 2);
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].chr,
        "chr9"
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].start,
        3526071
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[0].end,
        3526165
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[1].chr,
        "chr9"
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[1].start,
        3526183
    );
    assert_eq!(
        tokenized_regions.into_iter().collect::<Vec<_>>()[1].end,
        3526269
    );
}
