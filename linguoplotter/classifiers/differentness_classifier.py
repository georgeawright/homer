import math

from linguoplotter import fuzzy
from linguoplotter.classifier import Classifier
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collections import StructureSet


class DifferentnessClassifier(Classifier):
    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        """
        Required: ('start' AND 'end') OR 'collection'
        Optional: 'space'
        """
        start = kwargs.get("start")
        end = kwargs.get("end")
        collection = kwargs.get("collection")
        space = kwargs.get("space")
        return_nan = kwargs.get("return_nan", False)

        collection = list(collection) if collection is not None else [start, end]
        spaces = (
            StructureSet.union(
                *[
                    item.parent_spaces.where(
                        is_conceptual_space=True, is_basic_level=True
                    )
                    for item in collection
                ]
            )
            if space is None
            else [space]
        )
        distinct_pairs = [
            (collection[i], collection[j])
            for i in range(len(collection))
            for j in range(len(collection[:i]))
        ]
        if distinct_pairs == []:
            distinct_pairs = [(collection[0], collection[0])]
        proximities = []
        for space in spaces:
            for pair in distinct_pairs:
                if not (
                    pair[0].has_location_in_space(space)
                    and pair[1].has_location_in_space(space)
                ):
                    return 0.0
                for a in pair[0].location_in_space(space).coordinates:
                    min_distance = float("inf")
                    for b in pair[1].location_in_space(space).coordinates:
                        distance = space.parent_concept.distance_function(
                            [a], [b], return_nan=return_nan
                        )
                        if math.isnan(distance):
                            return math.nan if return_nan else 1.0
                        if distance < min_distance:
                            min_distance = distance
                    proximities.append(
                        space.parent_concept._distance_to_proximity(min_distance)
                    )
        return fuzzy.AND(*[1 - p for p in proximities])
