use std::collections::HashMap;
use std::fmt::{Display, Formatter, Result};

use pyo3::prelude::*;

use serde_json::json;
use serde_json::{to_string, Value};

#[pyclass]
pub struct JsonValueWrapper{
    pub value: Value,
}

impl Display for JsonValueWrapper {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", to_string(&self.value).unwrap())
    }
}

#[pymethods]
impl JsonValueWrapper {
    #[new]
    pub fn new(v: String) -> Self {
        Self{value: serde_json::from_str(&v).unwrap()}
    }

    fn __str__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn __repr__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn __len__(self_: PyRef<'_, Self>) -> usize {
        if self_.value.is_array() {
            let empty: Vec<Value> = vec![];
            return self_.value.as_array().unwrap_or(&empty).len();
        } else if self_.value.is_string() {
            let empty = String::new();
            return self_.value.as_str().unwrap_or(empty.as_str()).len();
        } else if self_.value.is_object() {
            let empty_json = json!("{}");
            let empty = empty_json.as_object().unwrap();
            return self_.value.as_object().unwrap_or(empty).len();
        }
        return 0;
    }

    fn is_array(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_array();
    }

    fn as_array(self_: PyRef<'_, Self>) -> Option<Vec<Self>> {
        return self_.value.as_array().map(|item| item.iter().map(|inner_item| Self{value: inner_item.clone()}).collect::<Vec<Self>>());
    }

    fn is_boolean(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_boolean();
    }

    fn as_boolean(self_: PyRef<'_, Self>) -> Option<bool> {
        return self_.value.as_bool();
    }

    fn is_f64(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_f64();
    }

    fn as_f64(self_: PyRef<'_, Self>) -> Option<f64> {
        return self_.value.as_f64();
    }

    fn is_i64(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_i64();
    }

    fn as_i64(self_: PyRef<'_, Self>) -> Option<i64> {
        return self_.value.as_i64();
    }

    fn is_null(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_null();
    }

    fn as_null(self_: PyRef<'_, Self>) -> Option<()> {
        return self_.value.as_null();
    }

    fn is_number(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_number();
    }

    fn as_number(self_: PyRef<'_, Self>) -> Option<f64> {
        return self_.value.as_number().unwrap().as_f64();
    }

    fn is_object(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_object();
    }

    fn as_object(self_: PyRef<'_, Self>) -> HashMap<String, Self> {
        return self_.value.as_object().unwrap().iter().map(|(k, v)| (k.clone(), Self{value: v.clone()})).collect::<HashMap<String, Self>>();
    }

    fn is_string(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_string();
    }

    fn as_string(self_: PyRef<'_, Self>) -> Option<String> {
        let v = self_.value.as_str();
        if v.is_none() {
            return None;
        }
        return Some(v.unwrap().to_string());
    }

    fn is_u64(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_u64();
    }

    fn as_u64(self_: PyRef<'_, Self>) -> Option<u64> {
        return self_.value.as_u64();
    }

    fn get_by_index(self_: PyRef<'_, Self>, i: usize) -> Option<Self> {
        let item = self_.value.get(i);
        if item.is_none() {
            return None;
        }
        return Some(Self{value: item.unwrap().clone()});
    }

    fn get_by_key(self_: PyRef<'_, Self>, k: String) -> Option<Self> {
        let item = self_.value.get::<String>(k);
        if item.is_none() {
            return None;
        }
        return Some(Self{value: item.unwrap().clone()});
    }
}
