from typing import List

from linguoplotter.classifier import Classifier


class NotClassifier(Classifier):
    def __init__(self, negated_concepts: List["Concept"]):
        self.negated_concept = (
            negated_concepts[0] if negated_concepts is not None else None
        )

    def classify(self, **kwargs: dict):
        try:
            if kwargs["start"].is_slot:
                return 1.0
            if kwargs["end"].is_slot:
                return 1.0
        except KeyError:
            pass

        return 1 - self.negated_concept.classifier.classify(**kwargs)
