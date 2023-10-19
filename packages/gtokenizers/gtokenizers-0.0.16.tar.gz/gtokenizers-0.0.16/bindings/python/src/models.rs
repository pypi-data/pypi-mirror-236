use std::collections::HashMap;
use std::hash::Hash;

use gtokenizers::models::region::Region;

use pyo3::class::basic::CompareOp;
use pyo3::exceptions::{PyIndexError, PyTypeError};
use pyo3::prelude::*;

#[pyclass(name = "Universe")]
#[derive(Clone, Debug)]
pub struct PyUniverse {
    pub regions: Vec<PyRegion>,
    pub region_to_id: HashMap<PyRegion, u32>,
    pub length: u32,
}

#[pymethods]
impl PyUniverse {
    #[getter]
    pub fn regions(&self) -> PyResult<Vec<PyRegion>> {
        Ok(self.regions.to_owned())
    }
    pub fn region_to_id(&self, region: &PyAny) -> PyResult<u32> {
        
        // get the chr, start, end (use can provide anything that has these attributes)
        let chr: String = region.getattr("chr")?.extract()?;
        let start: u32 = region.getattr("start")?.extract()?;
        let end: u32 = region.getattr("end")?.extract()?;

        // use to create PyRegion
        let region = PyRegion { chr, start, end };

        let id = self.region_to_id.get(&region);
        match id {
            Some(id) => Ok(id.to_owned()),
            None => Err(PyTypeError::new_err("Region not found in universe")),
        }
    }
    pub fn __len__(&self) -> usize {
        self.length as usize
    }
}

#[pyclass(name = "Region")]
#[derive(Clone, Debug, Hash, Eq, PartialEq)]
pub struct PyRegion {
    pub chr: String,
    pub start: u32,
    pub end: u32,
}

impl PyRegion {
    pub fn to_region(&self) -> Region {
        Region {
            chr: self.chr.clone(),
            start: self.start,
            end: self.end,
        }
    }
}

#[pymethods]
impl PyRegion {
    #[new]
    pub fn new(chr: String, start: u32, end: u32) -> Self {
        PyRegion { chr, start, end }
    }

    #[getter]
    pub fn chr(&self) -> PyResult<&str> {
        Ok(&self.chr)
    }

    #[getter]
    pub fn start(&self) -> PyResult<u32> {
        Ok(self.start)
    }

    #[getter]
    pub fn end(&self) -> PyResult<u32> {
        Ok(self.end)
    }
    pub fn __repr__(&self) -> String {
        format!("Region({}, {}, {})", self.chr, self.start, self.end)
    }

    pub fn __richcmp__(&self, other: PyRef<PyRegion>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => {
                Ok(self.chr == other.chr && self.start == other.start && self.end == other.end)
            }
            CompareOp::Ne => {
                Ok(self.chr != other.chr || self.start != other.start || self.end != other.end)
            }
            _ => Err(PyTypeError::new_err("Unsupported comparison operator")),
        }
    }
}

#[pyclass(name = "TokenizedRegion")]
#[derive(Clone, Debug)]
pub struct PyTokenizedRegion {
    pub region: PyRegion,
    pub id: u32,
    pub bit_vector: Vec<bool>,
    pub one_hot: Vec<u8>,
}

#[pymethods]
impl PyTokenizedRegion {
    #[new]
    pub fn new(region: PyRegion, id: u32, bit_vector: Vec<bool>, one_hot: Vec<u8>) -> Self {
        PyTokenizedRegion {
            region,
            id,
            bit_vector,
            one_hot,
        }
    }

    #[getter]
    pub fn chr(&self) -> PyResult<&str> {
        Ok(&self.region.chr)
    }

    #[getter]
    pub fn start(&self) -> PyResult<u32> {
        Ok(self.region.start)
    }

    #[getter]
    pub fn end(&self) -> PyResult<u32> {
        Ok(self.region.end)
    }

    #[getter]
    pub fn region(&self) -> PyResult<PyRegion> {
        Ok(self.region.clone())
    }
    #[getter]
    pub fn id(&self) -> PyResult<u32> {
        Ok(self.id)
    }
    #[getter]
    pub fn bit_vector(&self) -> PyResult<Vec<bool>> {
        Ok(self.bit_vector.clone())
    }

    #[getter]
    pub fn one_hot(&self) -> PyResult<Vec<u8>> {
        Ok(self.one_hot.clone())
    }

    pub fn __repr__(&self) -> String {
        format!(
            "TokenizedRegion({}, {}, {})",
            self.region.chr, self.region.start, self.region.end
        )
    }
}

#[pyclass(name = "TokenizedRegionSet")]
#[derive(Clone, Debug)]
pub struct PyTokenizedRegionSet {
    pub regions: Vec<PyRegion>,
    pub bit_vector: Vec<bool>,
    pub ids: Vec<u32>,
    curr: usize,
}

#[pymethods]
impl PyTokenizedRegionSet {
    #[new]
    pub fn new(regions: Vec<PyRegion>, bit_vector: Vec<bool>, ids: Vec<u32>) -> Self {
        PyTokenizedRegionSet {
            regions,
            bit_vector,
            ids,
            curr: 0,
        }
    }

    #[getter]
    pub fn regions(&self) -> PyResult<Vec<PyRegion>> {
        Ok(self.regions.to_owned())
    }

    #[getter]
    pub fn bit_vector(&self) -> PyResult<Vec<bool>> {
        Ok(self.bit_vector.clone())
    }
    #[getter]
    pub fn ids(&self) -> PyResult<Vec<u32>> {
        Ok(self.ids.clone())
    }

    // pub fn pad(&mut self, len: usize) {
    //     let padding_token = PyRegion::new(PAD_CHR.to_string(), PAD_START as u32, PAD_END as u32);
    //     while self.regions.len() < len {
    //         self.regions.push(padding_token.clone());
    //         self.bit_vector.push(false);
    //         self.ids.push(0);
    //     }
    // }

    pub fn __repr__(&self) -> String {
        format!("TokenizedRegionSet({} regions)", self.regions.len())
    }

    pub fn __len__(&self) -> usize {
        self.regions.len()
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    pub fn __next__(&mut self) -> Option<PyTokenizedRegion> {
        if self.curr < self.regions.len() {
            let region = self.regions[self.curr].clone();
            let id = self.ids[self.curr];
            let bit_vector = self.bit_vector.clone();
            let one_hot = bit_vector
                .iter()
                .map(|&b| if b { 1 } else { 0 })
                .collect::<Vec<_>>();
            self.curr += 1;
            Some(PyTokenizedRegion::new(region, id, bit_vector, one_hot))
        } else {
            None
        }
    }

    pub fn __getitem__(&self, indx: isize) -> PyResult<PyTokenizedRegion> {
        let indx = if indx < 0 {
            self.regions.len() as isize + indx
        } else {
            indx
        };
        if indx < 0 || indx >= self.regions.len() as isize {
            Err(PyIndexError::new_err("Index out of bounds"))
        } else {
            let region = self.regions[indx as usize].clone();
            let id = self.ids[indx as usize];
            let bit_vector = self.bit_vector.clone();
            let one_hot = bit_vector
                .iter()
                .map(|&b| if b { 1 } else { 0 })
                .collect::<Vec<_>>();
            Ok(PyTokenizedRegion::new(region, id, bit_vector, one_hot))
        }
    }
}
