from homer.classifier import Classifier
from homer.structures import Space


class DifferenceClassifier(Classifier):
    from homer.structures import Chunk
    from homer.structures import Concept

    def __init__(
        self,
        scalar_classifier: Classifier,
        proximity_weight: float = 0.6,
        neighbours_weight: float = 0.4,
    ):
        self.scalar_classifier = scalar_classifier
        self.proximity_weight = proximity_weight
        self.neighbours_weight = neighbours_weight

    def classify(self, **kwargs: dict):
        class Dummy:
            def __init__(self, value):
                self.value = [value]

        start = kwargs["start"]
        end = kwargs["end"]
        space = kwargs["space"]

        difference = (
            getattr(start, space.parent_concept.relevant_value)[0]
            - getattr(end, space.parent_concept.relevant_value)[0]
        )
        difference_container = Dummy(difference)
        kwargs["start"] = difference_container
        return self.scalar_classifier.classify(**kwargs)
