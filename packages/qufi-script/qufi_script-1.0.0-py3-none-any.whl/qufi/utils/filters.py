from .. import config


def filter_unchangeable_words(text: str) -> dict:
    split = False
    words_dict = {}
    temp_text = ""
    for latter in text:
        if latter == '`':
            if split:
                split = False
                words_dict['`%s`' % temp_text] = temp_text
                temp_text = ''
            else:
                split = True
        else:
            if split:
                temp_text += latter
    return words_dict


def is_vowel(latter):
    return latter in config.VOWELS


def is_consonant(latter):
    return latter in config.CONSONANTS


def is_long_vowel(latter):
    return len(latter) == 2 and is_vowel(latter)


def is_double_latter(latter):
    return len(latter) == 2 and latter in config.DOUBLE_LATTER


def get_consonants(word):
    for w in word:
        if is_consonant(w):
            yield w


def word_spliter(text: str):
    import re
    split_words = []

    new_text = text.lower()
    regex_of_double_latter_sound = re.findall(r'(([cdsp]h|[nz]y|ts)(aa?|ee?|ii?|oo?|uu?)?)',
                                              new_text)
    regex_of_double_latter_sound = [rdl[0] for rdl in regex_of_double_latter_sound]
    for rds in regex_of_double_latter_sound:
        new_text = new_text.replace(rds, "")

    regex_of_sounds = re.findall(r'([bcdfghjklmnpqrstvwxyz]{1}(aa?|ee?|ii?|oo?|uu?))', new_text)
    split_words.extend(regex_of_double_latter_sound)
    split_words.extend([rs[0] for rs in regex_of_sounds])

    return split_words
