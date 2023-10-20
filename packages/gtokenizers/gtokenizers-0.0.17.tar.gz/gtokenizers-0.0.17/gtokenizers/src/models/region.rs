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
}

impl TokenizedRegion {
    pub fn to_id(&self) -> u32 {
        self.id.to_owned()
    }
}
