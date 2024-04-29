import deepl


def get_uk_translation(word: str, auth_key: str) -> str:
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(word, source_lang="DE", target_lang="UK")
    translated_text = result.text
    translated_text = translated_text.lower()
    translated_text = translated_text.strip(".")
    return translated_text
