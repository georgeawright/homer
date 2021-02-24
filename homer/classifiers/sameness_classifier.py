import statistics

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structures.nodes import Chunk
from homer.structures.links import Label, Relation


class SamenessClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict):
        start = kwargs["start"]
        end = kwargs["end"]
        sameness_concept = kwargs["concept"]
        if isinstance(start, Label) and isinstance(end, Label):
            if start.parent_concept == end.parent_concept:
                return statistics.fmean([start.quality, end.quality])
        if isinstance(start, Chunk) and isinstance(end, Chunk):
            if start.is_slot or end.is_slot:
                slot, chunk = (start, end) if start.is_slot else (end, start)
                try:
                    return max(
                        label.quality
                        for label in chunk.labels
                        if label.parent_concept.location.space
                        in slot.value.child_spaces
                    )
                except ValueError:
                    return 0.0
            common_correspondences = set.intersection(
                {
                    correspondence
                    for label in start.labels
                    for correspondence in label.correspondences
                },
                {
                    correspondence
                    for label in start.labels
                    for correspondence in label.correspondences
                },
            )
            try:
                return statistics.fmean(
                    [
                        correspondence.quality
                        for correspondence in common_correspondences
                        if correspondence.parent_concept == sameness_concept
                    ]
                )
            except statistics.StatisticsError:
                return FloatBetweenOneAndZero(0)
        if isinstance(start, Relation) and isinstance(end, Relation):
            relation_starts_sameness = self.classify(
                start=start.start, end=end.start, concept=sameness_concept
            )
            relation_ends_sameness = self.classify(
                start=start.end, end=end.end, concept=sameness_concept
            )
            relation_concepts_sameness = FloatBetweenOneAndZero(
                start.parent_concept == end.parent_concept
            )
            return statistics.fmean(
                [
                    relation_starts_sameness,
                    relation_ends_sameness,
                    relation_concepts_sameness,
                ]
            )
        return FloatBetweenOneAndZero(0)
