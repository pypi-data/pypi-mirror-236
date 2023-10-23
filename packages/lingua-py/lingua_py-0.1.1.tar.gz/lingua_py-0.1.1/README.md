<div align="center">

  ![lingua](https://raw.githubusercontent.com/pemistahl/lingua-rs/main/images/logo.png)
  
  ![Static Badge](https://img.shields.io/badge/dependency_version%3Alingua-1.5.0-blue)
  [![build status](https://github.com/chatblanc-ciel/lingua-py/actions/workflows/CI.yml/badge.svg)](https://github.com/chatblanc-ciel/lingua-py/actions/workflows/CI.yml)
  ![PyPI - Version](https://img.shields.io/pypi/v/lingua_py)
  [![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
</div>

<br>

# Lingua-py

Lingua-py is an Python wrapper for the [Rust][1] [lingua][2] crate with [PyO3/Maturin][4].

## Summary

Lingua is a NIF-based bridge for the [lingua][2] [Rust][1] language detection library.

## Usage 

In imitation of [Upstream][3], introduce basic usage.
Alternatively please see [`tests` section](https://github.com/chatblanc-ciel/lingua-py/tree/master/python/tests/small_usage).

### 10.1 [Basic usage](https://github.com/pemistahl/lingua-rs#101-basic-usage)

```python
    languages: list[Language] = [Language.English, Language.Japanese]
    detector: LanguageDetector = LanguageDetectorBuilder.from_languages(
        languages
    ).build()

    expected: Language = Language.Japanese
    actual: Language = detector.detect_language_of("これは何語ですか？")

    assert actual == expected
```
<details>
<summary>pytest command</summary>

```bash
rye sync --no-lock
rye run python -m pytest -s -vv python/tests/small_usage/test_basic.py::test_basic
```
</details>


# License

[Apache License v2](./LICENSE), and lingua-rs is also [Apache License v2](https://github.com/pemistahl/lingua-rs/blob/master/LICENSE).






[1]: https://www.rust-lang.org 
[2]: https://crates.io/crates/lingua
[3]: https://github.com/pemistahl/lingua-rs.git
[4]: https://www.maturin.rs/