import math

from linguoplotter.classifier import Classifier


class MostOfTheCountryClassifier(Classifier):
    def classify(self, **kwargs: dict):
        """
        Required: 'concept'; 'start' OR 'collection'
        """
        collection = kwargs.get("collection")
        start = kwargs.get("start")
        item = start if start is not None else collection.get()
        return_nan = kwargs.get("return_nan", False)

        if item.is_slot:
            return math.nan if return_nan else 1.0

        return 0.5 ** abs(13 - item.size)
