from homer import fuzzy
from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection


class SamenessClassifier(Classifier):
    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        """
        Required: ('start' AND 'end') OR 'collection'
        Optional: 'space'
        """
        start = kwargs.get("start")
        end = kwargs.get("end")
        collection = kwargs.get("collection")
        space = kwargs.get("space")

        collection = list(collection) if collection is not None else [start, end]
        spaces = (
            StructureCollection.union(
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
        return fuzzy.OR(
            *[
                fuzzy.AND(
                    *[
                        space.proximity_between(pair[0], pair[1])
                        if pair[0].has_location_in_space(space)
                        and pair[1].has_location_in_space(space)
                        else 0.0
                        for pair in distinct_pairs
                    ]
                )
                for space in spaces
            ]
        )
