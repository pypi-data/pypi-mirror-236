# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.17]
- performance optimizations.
- remove all instances of `bit_vector` and `one_hot_vector` from the core crate + python bindings. This is because it was going unused, and was causing a lot of unnecessary overhead; both computationally and in developer time.
- add `pad` function to the python bindings.
- updated the type stubs for the python bindings.

## [0.0.16]
- add ability to extract padding and unknown tokens from a tokenizer
- streamline and standardize the addition of padding and unknown tokens to tokenizer vocab if they dont exist
- introduce `rstest` for more robust and streamlined testing
- make the interface to the python bindings when giving regions more flexible by only requiring an object that can have a `chr`, `start`, and `end` attribute

## [0.0.15]
- bump everything to 0.0.15 to fix pypi issues

## [0.0.14]
- introduced concept of padding to the TreeTokenizer
- added basic padding capabilities to the TreeTokenizer
- exposed getters for the unknown and the padding token to the python bindings

## [0.0.13]
- update readmes
- typos

## [0.0.12]
- added more/better documentation

## [0.0.11]
- introduced concept of `TokenizedRegion`.
- `TokenizedRegion`s contain and `id`, `bit_vector`, and `one_hot_vector`.
- `TokenizedRegion`s are yielded by `TokenizedRegionSet`s.
- Added more magic methods to `TokenizedRegionSet` to make it more pythonic.
- More unit tests.

## [0.0.10]
- added .pyi stubs for type hinting inside IDEs

## [0.0.9]
- Fix bug that prevented unknown tokens from being yielded when tokenizing region sets.

## [0.0.8]
- Initial release of the `TreeTokenizer`  for tokenizing traditional region sets (bed files).