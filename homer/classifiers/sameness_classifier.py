import statistics

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Link, Node
from homer.tools import correspond


class SamenessClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        start = kwargs["start"]
        end = kwargs["end"]
        if isinstance(start, Node) and isinstance(end, Node):
            start_conceptual_spaces = StructureCollection(
                {label.parent_space.conceptual_space for label in start.labels}
            )
            end_conceptual_spaces = StructureCollection(
                {label.parent_space.conceptual_space for label in end.labels}
            )
            all_conceptual_spaces = StructureCollection.union(
                start_conceptual_spaces, end_conceptual_spaces
            )
            common_conceptual_spaces = StructureCollection.intersection(
                start_conceptual_spaces, end_conceptual_spaces
            )
            if len(all_conceptual_spaces) == 0:
                return 0.0
            return len(common_conceptual_spaces) / len(all_conceptual_spaces)
        if isinstance(start, Link) and isinstance(end, Link):
            if not (
                correspond(start.start, end.start) and correspond(start.end, end.end)
            ):
                return 0.0
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
        return 0.0
