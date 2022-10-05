from typing import List

from linguoplotter.classifier import Classifier


class NotClassifier(Classifier):
    def __init__(self, negated_concepts: List["Concept"]):
        self.negated_concept = (
            negated_concepts[0] if negated_concepts is not None else None
        )

    def classify(self, **kwargs: dict):
        return 1 - self.negated_concept.classifier.classify(**kwargs)