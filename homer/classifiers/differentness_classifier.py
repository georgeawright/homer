from homer.classifier import Classifier


class DifferentnessClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict):
        start = kwargs["start"]
        end = kwargs["end"]
        if start.is_slot or end.is_slot:
            return 0.0
        return 1 - start.parent_concept.proximity_to(end.parent_concept)
