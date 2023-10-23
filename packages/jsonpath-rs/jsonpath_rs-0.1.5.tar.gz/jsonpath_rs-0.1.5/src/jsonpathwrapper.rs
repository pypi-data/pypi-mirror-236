use std::collections::HashMap;
use std::fmt::{Display, Formatter, Result};
use std::ops::Deref;
use std::str::FromStr;

use pyo3::prelude::*;

use serde_json::Value;
use jsonpath_rust::JsonPathInst;
use jsonpath_rust::JsonPtr;

use crate::jsonvaluewrapper::JsonValueWrapper;


#[pyclass]
pub struct JsonPathWrapper{
    pub value: JsonValueWrapper,
}

impl Display for JsonPathWrapper {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", self.to_string())
    }
}

impl JsonPathWrapper {
    fn _find(json: Value, path: String) -> Vec<JsonValueWrapper> {
        let query: JsonPathInst = JsonPathInst::from_str(path.as_str()).unwrap();
        let slice: Vec<JsonPtr<'_, Value>> = query.find_slice(&json);
        return slice.iter().map(|item| JsonValueWrapper{value: item.deref().clone()}).collect::<Vec<JsonValueWrapper>>();
    }
}

#[pymethods]
impl JsonPathWrapper {
    #[new]
    fn new(v: String) -> Self {
        Self{value: JsonValueWrapper::new(v)}
    }

    fn __str__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn __repr__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn find(self_: PyRef<'_, Self>, path: String) -> Vec<JsonValueWrapper> {
        let json: Value = self_.value.value.clone();
        return Self::_find(json, path);
    }

    fn find_all(self_: PyRef<'_, Self>, mapping: Vec<(String, String)>) -> HashMap<String, Vec<JsonValueWrapper>> {
        let mut result: HashMap<String, Vec<JsonValueWrapper>> = HashMap::new();
        for (alias, path) in mapping {
            result.insert(alias, Self::_find(self_.value.value.clone(), path));
        }
        return result
    }
}
