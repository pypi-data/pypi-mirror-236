<h1 align="center">
🧬 gtokenizers
</h1>
<br/>

`gtokenizers` is library for fast and flexible tokenization of genomic data to be used in bioinformatic machine learning models. The purpose of this library is to provide a simple and highly performant interface for tokenizing genomic data in a way that is compatible with modern machine learning workflows.

## Installation
Run the following in your terminal:
```console
cargo add gtokenizers
```

or add the following to your `Cargo.toml` file:
```toml
gtokenizers = "0.0.11"
``````

## Quickstart
You can create a tokenizer from a universe (or vocab) file like so:
```rust
use gtokenizers::tokenizers::TreeTokenizer;
use gtokenizers::models::region_set::RegionSet;
use std::path::Path;

let vocab_path = Path::new("path/to/vocab.bed");
let t = TreeTokenizer::from(&vocab_path);

let rs = RegionSet::from("path/to/regions.bed");

let tokens = t.tokenize(&rs);

for t in tokens {
    println!("{}, {}", t, t.id);
}
```

## Additional information
This crate is still in early development. We will be adding more features and documentation in the near future. If you have any questions or suggestions, please feel free to open an issue or a pull request.