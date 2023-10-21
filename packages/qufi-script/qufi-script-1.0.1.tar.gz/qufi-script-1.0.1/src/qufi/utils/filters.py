from .. import config


def filter_unchangeable_words(text: str) -> dict:
    split = False
    words_dict = {}
    temp_text = ""
    for letter in text:
        if letter == '`':
            if split:
                split = False
                words_dict['`%s`' % temp_text] = temp_text
                temp_text = ''
            else:
                split = True
        else:
            if split:
                temp_text += letter
    return words_dict


def is_vowel(letter):
    return letter in config.LONG_VOWELS


def is_consonant(letter):
    return letter in config.CONSONANTS


def is_long_vowel(letter):
    return len(letter) == 2 and is_vowel(letter)


def is_double_letter(letter):
    return len(letter) == 2 and letter in config.DOUBLE_LETTERS


def get_consonants(word):
    for w in word:
        if is_consonant(w):
            yield w


def word_spliter(text: str):
    import re
    split_words = []

    new_text = text.lower()
    regex_of_double_letter_sound = re.findall(r'(([cdsp]h|[nz]y|ts)(aa?|ee?|ii?|oo?|uu?)?)',
                                              new_text)
    regex_of_double_letter_sound = [rdl[0] for rdl in regex_of_double_letter_sound]
    for rds in regex_of_double_letter_sound:
        new_text = new_text.replace(rds, "")

    regex_of_sounds = re.findall(r'([bcdfghjklmnpqrstvwxyz]{1}(aa?|ee?|ii?|oo?|uu?))', new_text)
    split_words.extend(regex_of_double_letter_sound)
    split_words.extend([rs[0] for rs in regex_of_sounds])

    return split_words
