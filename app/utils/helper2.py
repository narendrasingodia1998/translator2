from app.utils.lang_code import lang_code


def valid_language(language):
    return language.strip().lower() in set(lang_code.keys())


def get_code(language):
    return lang_code[language.strip().lower()]


def get_language(code):
    code_lang = {v: k for k, v in lang_code.items()}
    language = code_lang[code]
    return language[0].upper() + language[1:]
