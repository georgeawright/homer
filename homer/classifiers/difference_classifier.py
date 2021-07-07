from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.tools import average_vector


class DifferenceClassifier(Classifier):
    from homer.structures.nodes import Chunk, Concept

    def __init__(self, prototype_difference: float):
        self.prototype_difference = prototype_difference

    def classify(self, **kwargs: dict):
        start = kwargs["start"]
        end = kwargs["end"]
        space = kwargs["space"]

        difference = (
            average_vector(start.location_in_space(space).coordinates)[0]
            - average_vector(end.location_in_space(space).coordinates)[0]
        )
        return FloatBetweenOneAndZero(difference - self.prototype_difference)
