from linguoplotter.classifier import Classifier


class EverywhereClassifier(Classifier):
    def classify(self, **kwargs: dict):
        """
        Required: 'concept'; 'start' OR 'collection'
        """
        collection = kwargs.get("collection")
        start = kwargs.get("start")
        item = start if start is not None else collection.get()

        return 0.5 ** (16 - item.size)
