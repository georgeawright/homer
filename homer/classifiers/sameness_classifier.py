import statistics

from homer import fuzzy
from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class SamenessClassifier(Classifier):
    def __init__(self):
        pass

    def classify_link(self, **kwargs: dict) -> FloatBetweenOneAndZero:
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

    def classify_chunk(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        root = kwargs["root"]
        child = kwargs["child"]
        if root is None:
            return 1.0
        if child is None:
            return 1.0
        distances = [
            location.space.proximity_between(root, child)
            for location in root.locations
            if location.space.is_conceptual_space and location.space.is_basic_level
        ]
        return 0.0 if distances == [] else fuzzy.AND(*distances)
