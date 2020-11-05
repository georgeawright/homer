from enum import Enum, auto


class WordForm(Enum):
    HEADWORD = auto()
    PRESENT_NOT_THIRD = auto()
    PRESENT_THIRD = auto()
    PAST = auto()
    COMPARATIVE = auto()
    SUPERLATIVE = auto()
