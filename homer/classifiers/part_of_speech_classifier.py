from homer.classifier import Classifier


class PartOfSpeechClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict):
        part_of_speech = kwargs["concept"]
        word = kwargs["start"]
        lexeme = word.lexeme
        word_form = word.word_form
        return part_of_speech in lexeme.parts_of_speech[word_form]
