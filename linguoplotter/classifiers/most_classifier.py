import math

from linguoplotter.classifier import Classifier


class MostClassifier(Classifier):
    def classify(self, **kwargs: dict):
        start = kwargs.get("start")
        space = kwargs["space"]
        return_nan = kwargs.get("return_nan", False)

        start_location = start.location_in_space(space)

        for item in start.parent_space.where(is_chunk=True, is_raw=False):
            if item == start:
                continue
            if not item.has_location_in_space(space):
                continue
            item_location = item.location_in_space(space)
            if math.isnan(item_location.coordinates[0][0]):
                return math.nan if return_nan else 0.0
            if item_location.coordinates[0][0] > start_location.coordinates[0][0]:
                return 0.0
        return 1.0
