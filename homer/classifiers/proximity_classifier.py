from homer.classifier import Classifier


class ProximityClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, **kwargs: dict):
        return kwargs["concept"].proximity_to(kwargs["start"])
