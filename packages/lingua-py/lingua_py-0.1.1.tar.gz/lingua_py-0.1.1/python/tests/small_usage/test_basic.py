from lingua_py import Language, LanguageDetector, LanguageDetectorBuilder


def test_basic(request):
    languages: list[Language] = [Language.English, Language.Japanese]
    detector: LanguageDetector = LanguageDetectorBuilder.from_languages(
        languages
    ).build()

    expected: Language = Language.Japanese
    actual: Language = detector.detect_language_of("これは何語ですか？")
    print(actual)
    assert actual == expected

    expected: Language = Language.English
    actual: Language = detector.detect_language_of("What is this language?")
    print(actual)
    assert actual == expected

def test_Language_matches(request):
    actual: Language = Language.English
    match actual:
        case Language.Japanese:
            raise AssertionError("Language.Japanese should not match Language.English")
        case Language.French:
            raise AssertionError("Language.French should not match Language.English")
        case Language.English:
            pass
    match actual:
        case Language.Japanese:
            raise AssertionError("Language.Japanese should not match Language.English")
        case Language.English:
            pass
        case Language.French:
            raise AssertionError("Language.French should not match Language.English")

    actual: Language = Language.Japanese
    match actual:
        case Language.English:
            raise AssertionError("Language.English should not match Language.Japanese")
        case Language.French:
            raise AssertionError("Language.French should not match Language.Japanese")
        case Language.Japanese:
            pass
    match actual:
        case Language.English:
            raise AssertionError("Language.English should not match Language.Japanese")
        case Language.Japanese:
            pass
        case Language.French:
            raise AssertionError("Language.French should not match Language.Japanese")
        