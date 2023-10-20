use std::collections::HashMap;
use std::hash::Hash;

use gtokenizers::models::region::Region;
use gtokenizers::tokenizers::traits::{PAD_CHR, PAD_END, PAD_START};

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
}

#[pymethods]
impl PyTokenizedRegion {
    #[new]
    pub fn new(region: PyRegion, id: u32) -> Self {
        PyTokenizedRegion {
            region,
            id,
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
    pub ids: Vec<u32>,
    curr: usize,
}

#[pymethods]
impl PyTokenizedRegionSet {
    #[new]
    pub fn new(regions: Vec<PyRegion>, ids: Vec<u32>) -> Self {
        PyTokenizedRegionSet {
            regions,
            ids,
            curr: 0,
        }
    }

    #[getter]
    pub fn regions(&self) -> PyResult<Vec<PyRegion>> {
        Ok(self.regions.to_owned())
    }

    #[getter]
    pub fn ids(&self) -> PyResult<Vec<u32>> {
        Ok(self.ids.clone())
    }

    // this is wrong: the padding token might not be in the universe
    pub fn pad(&mut self, len: usize) {
        let pad_region = PyRegion {
            chr: PAD_CHR.to_string(),
            start: PAD_START as u32,
            end: PAD_END as u32,
        };
        let pad_id = self.ids[0];
        let pad_region_set = PyTokenizedRegionSet {
            regions: vec![pad_region; len],
            ids: vec![pad_id; len],
            curr: 0,
        };
        self.regions.extend(pad_region_set.regions);
        self.ids.extend(pad_region_set.ids);
    }

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

            self.curr += 1;
            Some(PyTokenizedRegion::new(region, id))
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
            Ok(PyTokenizedRegion::new(region, id))
        }
    }
}
