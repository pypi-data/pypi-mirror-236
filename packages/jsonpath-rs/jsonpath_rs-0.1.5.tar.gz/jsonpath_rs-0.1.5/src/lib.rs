use pyo3::prelude::*;
use pyo3::Python;

mod jsonvaluewrapper;
mod jsonpathwrapper;

#[pymodule]
fn jsonpath_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<jsonvaluewrapper::JsonValueWrapper>()?;
    m.add_class::<jsonpathwrapper::JsonPathWrapper>()?;
    Ok(())
}
