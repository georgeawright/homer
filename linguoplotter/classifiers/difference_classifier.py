import math

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
        return_nan = kwargs.get("return_nan", False)

        difference = (
            average_vector(start.location_in_space(space).coordinates)[0]
            - average_vector(end.location_in_space(space).coordinates)[0]
        )
        if math.isnan(difference):
            return math.nan if return_nan else 1.0
        space_breadth_adjusted_difference = difference / space.breadth
        try:
            return FloatBetweenOneAndZero(
                space_breadth_adjusted_difference / self.prototype_difference
            )
        except ZeroDivisionError:
            return FloatBetweenOneAndZero(
                1 / (1 - abs(space_breadth_adjusted_difference))
            )
