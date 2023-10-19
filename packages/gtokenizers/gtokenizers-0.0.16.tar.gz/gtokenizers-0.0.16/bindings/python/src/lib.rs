use pyo3::prelude::*;

pub mod models;
pub mod tokenizers;

use crate::models::{PyRegion, PyTokenizedRegion, PyTokenizedRegionSet, PyUniverse};
use crate::tokenizers::PyTreeTokenizer;

/// A Python module implemented in Rust.
#[pymodule]
fn gtokenizers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyTreeTokenizer>()?;
    m.add_class::<PyRegion>()?;
    m.add_class::<PyTokenizedRegionSet>()?;
    m.add_class::<PyTokenizedRegion>()?;
    m.add_class::<PyUniverse>()?;
    Ok(())
}
