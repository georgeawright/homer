from linguoplotter.classifier import Classifier
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.tools import average_vector


class DifferenceClassifier(Classifier):
    from linguoplotter.structures.nodes import Chunk, Concept

    def __init__(self, prototype_difference: float):
        self.prototype_difference = prototype_difference

    def classify(self, **kwargs: dict):
        """
        Required: 'start'; 'end'; 'space'
        """
        start = kwargs["start"]
        end = kwargs["end"]
        space = kwargs["space"]

        difference = (
            average_vector(start.location_in_space(space).coordinates)[0]
            - average_vector(end.location_in_space(space).coordinates)[0]
        )
        try:
            return FloatBetweenOneAndZero(difference / self.prototype_difference)
        except ZeroDivisionError:
            return FloatBetweenOneAndZero(1 / (1 - abs(difference)))
