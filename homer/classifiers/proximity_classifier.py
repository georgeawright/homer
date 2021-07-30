import statistics

from homer import fuzzy
from homer.classifier import Classifier


class ProximityClassifier(Classifier):
    def __init__(self):
        pass

    def classify_link(self, **kwargs: dict):
        return kwargs["concept"].proximity_to(kwargs["start"])

    def classify_chunk(self, **kwargs: dict):
        root = kwargs.get("root")
        child = kwargs.get("child")
        if root is None and child is not None:
            return 1.0
        if child is None or child.is_slot:
            proximities = [
                space.proximity_between(member, root) if not member.is_slot else 0
                for space in root.parent_spaces
                for member in root.members
                if space.is_conceptual_space and space.is_basic_level
            ]
            return statistics.fmean(proximities) if proximities != [] else 0
        distances = [
            space.proximity_between(root, child)
            for space in root.parent_spaces
            if space.is_conceptual_space and space.is_basic_level
        ]
        return 0.0 if distances == [] else fuzzy.AND(*distances)
