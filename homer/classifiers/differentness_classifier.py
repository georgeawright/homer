import statistics

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structures import Chunk
from homer.structures.links import Label, Relation


class DifferentnessClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict):
        start = kwargs["start"]
        end = kwargs["end"]
        differentness_concept = kwargs["concept"]
        if type(start) != type(end):
            return FloatBetweenOneAndZero(0)
        if isinstance(start, Label):
            return 1 - start.parent_concept.proximity_to(end.parent_concept)
        if isinstance(start, Chunk):
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
                        if correspondence.parent_concept == differentness_concept
                    ]
                )
            except statistics.StatisticsError:
                return FloatBetweenOneAndZero(0)
        if isinstance(start, Relation):
            relation_starts_sameness = self.classify(
                start=start.start, end=end.start, concept=differentness_concept
            )
            relation_ends_sameness = self.classify(
                start=start.end, end=end.end, concept=differentness_concept
            )
            relation_concepts_sameness = 1 - start.parent_concept.proximity_to(
                end.parent_concept
            )
            return statistics.fmean(
                [
                    relation_starts_sameness,
                    relation_ends_sameness,
                    relation_concepts_sameness,
                ]
            )
        return FloatBetweenOneAndZero(0)
