use super::{detector::PyLanguageDetector, language::PyLanguage};
use lingua::{Language, LanguageDetectorBuilder};
use pyo3::{prelude::*, types::PyList};

#[pyclass(name = "LanguageDetectorBuilder")]
pub struct PyLanguageDetectorBuilder {
    builder: LanguageDetectorBuilder,
}
#[pymethods]
impl PyLanguageDetectorBuilder {
    /// Creates and returns an instance of `LanguageDetectorBuilder` with all built-in languages.
    #[staticmethod]
    pub fn from_all_languages() -> Self {
        Self {
            builder: LanguageDetectorBuilder::from_all_languages(),
        }
    }

    /// Creates and returns an instance of `LanguageDetectorBuilder`
    /// with all built-in spoken languages.
    #[staticmethod]
    pub fn from_all_spoken_languages() -> Self {
        Self {
            builder: LanguageDetectorBuilder::from_all_spoken_languages(),
        }
    }

    /// Creates and returns an instance of `LanguageDetectorBuilder`
    /// with the specified `languages`.
    ///
    /// ⚠ Panics if less than two `languages` are specified.
    #[staticmethod]
    pub fn from_languages(py_languages: &PyList) -> Self {
        let languages: Vec<Language> = py_languages
            .extract::<Vec<Py<PyLanguage>>>()
            .unwrap()
            .iter()
            .map(|lang| PyLanguage::clone_from_py(lang).into())
            .collect();
        //let languages: Vec<Language> = py_languages.clone().into_iter().map(|lang| (*lang).into()).collect();
        Self {
            builder: LanguageDetectorBuilder::from_languages(&languages),
        }
    }

    /// Creates and returns the configured instance of [LanguageDetector].
    pub fn build(&mut self) -> PyLanguageDetector {
        PyLanguageDetector {
            detector: self.builder.build(),
        }
    }
}
