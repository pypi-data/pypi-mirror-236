import time
from typing import List
from pathlib import Path

import pytest
from geniml.io import RegionSet
from gtokenizers import Region, TokenizedRegionSet, TreeTokenizer



@pytest.fixture
def vocab_file() -> str:
    return "tests/data/peaks.bed"


@pytest.fixture
def regions_to_tokenize() -> List[Region]:
    # chr6	157381091	157381200
    # chr2	168247745	168247800
    return [Region("chr6", 157381111, 157381220), Region("chr2", 168247765, 168247820)]


@pytest.fixture
def tokenizer(vocab_file: str) -> TreeTokenizer:
    return TreeTokenizer(vocab_file)


def test_make_tokenizer(vocab_file: str) -> None:
    tokenizer = TreeTokenizer(vocab_file)
    assert tokenizer is not None


def test_tokenize(tokenizer, regions_to_tokenize) -> None:
    tokens = tokenizer.tokenize(regions_to_tokenize)
    assert len(tokens) == 2

    # assert things got tokenized right
    assert tokens.regions[0].chr == "chr6"
    assert tokens.regions[0].start == 157381091
    assert tokens.regions[0].end == 157381200

    # assert the second token is good
    assert tokens.regions[1].chr == "chr2"
    assert tokens.regions[1].start == 168247745
    assert tokens.regions[1].end == 168247800

    # test that we can yield tokens
    for token in tokens:
        assert token is not None
        assert isinstance(token.id, int)


def test_tokenized_region_set_getitem(tokenizer, regions_to_tokenize) -> None:
    tokens = tokenizer.tokenize(regions_to_tokenize)
    assert len(tokens) == 2

    # assert things got tokenized right
    assert tokens[0].chr == "chr6"
    assert tokens[0].start == 157381091
    assert tokens[0].end == 157381200

    # assert the second token is good
    assert tokens[1].chr == "chr2"
    assert tokens[1].start == 168247745
    assert tokens[1].end == 168247800

    # test that we can still yield tokens
    for token in tokens:
        assert token is not None
        assert isinstance(token.id, int)

    # test that we can't go out of bounds
    with pytest.raises(IndexError):
        tokens[2]


def test_tokenized_region_set_to_list(tokenizer, regions_to_tokenize) -> None:
    tokens = tokenizer.tokenize(regions_to_tokenize)
    assert len(tokens) == 2

    # assert things got tokenized right
    assert tokens.regions[0].chr == "chr6"
    assert tokens.regions[0].start == 157381091
    assert tokens.regions[0].end == 157381200

    # assert the second token is good
    assert tokens.regions[1].chr == "chr2"
    assert tokens.regions[1].start == 168247745
    assert tokens.regions[1].end == 168247800

    # test that we can convert to a list
    tokens_list = list(tokens)
    assert len(tokens_list) == 2

    # assert things got tokenized right
    assert tokens_list[0].chr == "chr6"
    assert tokens_list[0].start == 157381091
    assert tokens_list[0].end == 157381200

    # assert the second token is good
    assert tokens_list[1].chr == "chr2"
    assert tokens_list[1].start == 168247745
    assert tokens_list[1].end == 168247800

    # test that we can still yield tokens
    for token in tokens_list:
        assert token is not None
        assert isinstance(token.id, int)


def test_tokenize_to_unknown(tokenizer) -> None:
    # un-tokenizable region
    r = Region("chr1", 100, 200)
    tokens = tokenizer.tokenize([r])
    assert len(tokens) == 1
    assert tokens[0].chr == "chrUNK"
    assert tokens[0].start == 0
    assert tokens[0].end == 0

    assert tokens[0].id == 6551
