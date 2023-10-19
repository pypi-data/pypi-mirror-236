#[derive(Debug, Eq, Hash, PartialEq)]
pub struct Region {
    pub chr: String,
    pub start: u32,
    pub end: u32,
}

pub type TokenizedRegions = Vec<Region>;

impl Clone for Region {
    fn clone(&self) -> Self {
        Region {
            chr: self.chr.clone(),
            start: self.start,
            end: self.end,
        }
    }
}

pub struct TokenizedRegion {
    pub chr: String,
    pub start: u32,
    pub end: u32,
    pub id: u32,
    pub bit_vector: Vec<bool>,
    pub one_hot: Vec<u8>,
}

impl TokenizedRegion {
    pub fn to_id(&self) -> u32 {
        self.id.to_owned()
    }
    pub fn to_bit_vector(&self) -> Vec<bool> {
        self.bit_vector.to_owned()
    }
    pub fn to_one_hot_encoded(&self) -> Vec<u8> {
        let mut one_hot_encoded = vec![0; self.bit_vector.len()];
        for (i, bit) in self.bit_vector.iter().enumerate() {
            if *bit {
                one_hot_encoded[i] = 1;
            }
        }
        one_hot_encoded
    }
}
