from homer.classifier import Classifier
from homer.location import Location
from homer.tools import average_vector


class DifferenceClassifier(Classifier):
    from homer.structures.nodes import Chunk, Concept

    def __init__(
        self,
        scalar_classifier: Classifier,
    ):
        self.scalar_classifier = scalar_classifier

    def classify(self, **kwargs: dict):
        class Dummy:
            def __init__(self, value):
                self.value = [[value]]

            def location_in_conceptual_space(self, space):
                return Location(self.value, space)

        start = kwargs["start"]
        end = kwargs["end"]
        space = kwargs["space"]

        difference = (
            average_vector(start.location_in_space(space).coordinates)[0]
            - average_vector(end.location_in_space(space).coordinates)[0]
        )
        difference_container = Dummy(difference)
        kwargs["start"] = difference_container
        return self.scalar_classifier.classify(**kwargs)
