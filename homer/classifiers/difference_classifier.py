from homer.classifier import Classifier
from homer.structures import Space
from homer.tools import average_vector


class DifferenceClassifier(Classifier):
    from homer.structures.nodes import Chunk, Concept

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
                self.value = [[value]]

        start = kwargs["start"]
        end = kwargs["end"]
        space = kwargs["space"]

        difference = (
            average_vector(getattr(start, space.parent_concept.relevant_value))[0]
            - average_vector(getattr(end, space.parent_concept.relevant_value))[0]
        )
        difference_container = Dummy(difference)
        kwargs["start"] = difference_container
        return self.scalar_classifier.classify(**kwargs)
