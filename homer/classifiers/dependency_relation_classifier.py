from homer.classifier import Classifier


# TODO
class DependencyRelationClassifier(Classifier):
    def __init__(self, rules):
        self.rules = rules

    def classify(self, **kwargs: dict):
        return all(rule(kwargs) for rule in self.rules)
