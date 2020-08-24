from typing import List, Tuple, Union

from .bubbles.concept import Concept
from .bubbles.perceptlets.word import Word


class Template:
    def __init__(self, words: List[Union[str, None]]):
        self.words = words

    def get_text_and_words(self, *args: Tuple[Concept]) -> List[Word]:
        arg_number = 0
        text = ""
        words = []
        for word in self.words:
            if word is None:
                words.append(Word.from_concept(args[arg_number]))
                text += " " + args[arg_number].name
                arg_number += 1
            else:
                words.append(Word.from_string(word))
                text += " " + word
        return text[1:], words
