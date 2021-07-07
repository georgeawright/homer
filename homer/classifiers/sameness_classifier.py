import statistics

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class SamenessClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        start = kwargs["start"]
        end = kwargs["end"]
        start_concept = (
            start.parent_concept
            if start.parent_concept is not None
            else start.parent_space.parent_concept
        )
        end_concept = (
            end.parent_concept
            if end.parent_concept is not None
            else end.parent_space.parent_concept
        )
        if start_concept.is_compatible_with(end_concept):
            return statistics.fmean([start.quality, end.quality])
        return 0.0
