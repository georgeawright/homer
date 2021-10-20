import statistics

from homer import fuzzy
from homer.classifier import Classifier


class ProximityClassifier(Classifier):
    def __init__(self):
        pass

    def classify_link(self, **kwargs: dict):
        return kwargs["concept"].proximity_to(kwargs["start"])

    def classify_chunk(self, **kwargs: dict):
        chunk = kwargs.get("chunk")
        return statistics.fmean(
            [
                chunk.rule.root_concept.proximity_to(chunk.root)
                if not (chunk.root.is_slot or chunk.root is None)
                else 0,
                chunk.rule.left_concept.proximity_to(chunk.left_branch.get())
                if not (chunk.left_branch.is_empty() or chunk.left_branch.get().is_slot)
                else 0,
                chunk.rule.right_concept.proximity_to(chunk.right_branch.get())
                if not (
                    chunk.right_branch.is_empty() or chunk.right_branch.get().is_slot
                )
                else 0,
            ]
        )
