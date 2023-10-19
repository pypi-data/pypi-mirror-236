from .. import config


def latter_dict() -> dict:
    vowels = ['a', ['u', 'uu'], ['i', 'ii'], ['aa'], ['e', 'ee'], '\'', ['o', 'oo']]
    consonants = ['h', 'l', 'm', 'r', 's', 'sh', 'q', 'b', 'v', 't', 'ch', 'n', 'ny', '\'', 'k', 'w', 'z', 'zy', 'y',
                  'd', 'j', 'g', 'x', 'c', 'ph', 'ts', 'f', 'p']
    all_latter_dict = {}
    the_dh = list("ዸꬉꬊꬋꬌꬍꬎ")
    for cons, latter in zip(consonants, config.REAL_LATTER):
        for vowel in vowels:
            ind = vowels.index(vowel)
            c = "" if cons == '\'' else cons
            if vowel == "'":
                vowel = ""
            if vowel == '' and c == "": continue
            
            if isinstance(vowel, list):
                for v in vowel:
                    all_latter_dict[c+v] = chr(ord(latter)+ind) + ('፞' if v != 'aa' and len(v) == 2 else '')
            else:
                all_latter_dict[c+vowel] = chr(ord(latter) + ind)

    for vowel, dh in zip(vowels, the_dh):
        if vowel == '\'': vowel = ''
        if isinstance(vowel, list):
            for v in vowel:
                all_latter_dict["dh" + v] = dh + ('፞' if v != 'aa' and len(v) == 2 else '')
        else:  
            all_latter_dict['dh'+vowel] = dh
    return all_latter_dict
