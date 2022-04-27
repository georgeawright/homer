from linguoplotter.classifier import Classifier


class ProximityClassifier(Classifier):
    def classify(self, **kwargs: dict):
        """
        Required: 'concept'; 'start' OR 'collection'
        """
        collection = kwargs.get("collection")
        start = kwargs.get("start")
        concept = kwargs.get("concept")

        item = start if start is not None else collection.get()
        return concept.proximity_to(item)
