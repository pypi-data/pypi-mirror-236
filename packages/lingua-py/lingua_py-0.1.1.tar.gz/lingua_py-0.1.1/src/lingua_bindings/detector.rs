use lingua::LanguageDetector;
use pyo3::prelude::*;

use super::language::PyLanguage;

#[pyclass(name = "LanguageDetector")]
pub struct PyLanguageDetector {
    pub(crate) detector: LanguageDetector,
}
#[pymethods]
impl PyLanguageDetector {
    pub fn detect_language_of(&self, text: String) -> Option<PyLanguage> {
        if let Some(lang) = self.detector.detect_language_of(text) {
            Some(lang.into())
        } else {
            None
        }
    }
}
