from lingua_py import Language, LanguageDetector, LanguageDetectorBuilder


def test_from_all_languages():
    detector = LanguageDetectorBuilder.from_all_languages().build()
    print(detector)


def test_from_all_spoken_languages(request):
    detector = LanguageDetectorBuilder.from_all_spoken_languages().build()
    print(detector)


def test_from_languages(request):
    languages: list[Language] = [
        Language.English,
        Language.Japanese,
        Language.French,
        Language.Spanish,
    ]
    detector: LanguageDetector = LanguageDetectorBuilder.from_languages(
        languages
    ).build()
