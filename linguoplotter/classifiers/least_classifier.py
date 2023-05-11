import math

from linguoplotter.classifier import Classifier


class LeastClassifier(Classifier):
    def classify(self, **kwargs: dict):
        start = kwargs.get("start")
        space = kwargs["space"]
        return_nan = kwargs.get("return_nan", False)

        start_item = start.non_slot_value if start.is_slot else start
        start_location = start_item.location_in_space(space)

        for item in start.parent_space.contents.where(is_chunk=True, is_raw=False):
            if item == start:
                continue
            if not item.has_location_in_space(space):
                continue
            item_location = (
                item.non_slot_value.location_in_space(space)
                if item.is_slot
                else item.location_in_space(space)
            )
            if math.isnan(item_location.coordinates[0][0]):
                return math.nan if return_nan else 0.0
            if item_location.coordinates[0][0] < start_location.coordinates[0][0]:
                return 0.0
        return 1.0
