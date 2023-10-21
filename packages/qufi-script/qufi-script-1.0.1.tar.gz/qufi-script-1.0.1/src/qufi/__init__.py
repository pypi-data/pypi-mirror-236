from .helpers.letters import letter_dict
from .utils.filters import filter_unchangeable_words, word_spliter
from .config import PUNCTUATIONS, LONG_VOWELS
from .version import __version__


class QubeFidel:
    def __init__(self):
        self.letters = letter_dict()

    def convert(self, text: str) -> str:
        new_text = text
        for flu in filter_unchangeable_words(new_text):
            new_text = new_text.replace(flu, "``")
        new_text = self.__direct(new_text)
        for flu in filter_unchangeable_words(text).values():
            new_text = new_text.replace('``', flu, 1)

        new_text = self.__replace_punc(new_text)
        return new_text

    def __replace_vowels(self, text):
        new_text = text

        for vowel in LONG_VOWELS:
            new_text = new_text.replace(f"'{vowel}", self.letters[vowel]) \
                               .replace(f"'{vowel[0]}", self.letters[vowel[0]])\
                               .replace(vowel, self.letters[vowel]) \
                               .replace(vowel[0], self.letters[vowel[0]])
                              
        return new_text
        
    def __replace_punc(self, text):
        import re 
        dot_regex = re.findall(r"((\w+\.\w+(\.\w+)*\.?)|(\.\.(\.)*))", text) # ምህጻረ-ቃለት ወይም ነጠብጣብ መለያ
        new_text = text
        repl = [dot[0].replace(".", "።") for dot in dot_regex]
     
        for punc in PUNCTUATIONS:
            new_text = new_text.replace(punc, PUNCTUATIONS[punc])
        
        for dot, rp in zip(dot_regex, repl):
            new_text = new_text.replace(rp, dot[0].upper(), 1)
            
        return new_text
   
    def __direct(self, text):
        new_text = text.lower()

        for ws in word_spliter(new_text):
            new_text = new_text.replace(ws, self.letters.get(ws, ""), 1)

        new_text = self.__replace_vowels(new_text)
        for k, v in self.letters.items():
            new_text = new_text.replace(k, v)

        return new_text

         
__all__ = ("QubeFidel", "__version__")