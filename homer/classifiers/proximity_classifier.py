from homer.classifier import Classifier


class ProximityClassifier(Classifier):
    def __init__(self):
        pass

    def classify(self, arguments: dict):
        return arguments["concept"].proximity_to(arguments["start"])
