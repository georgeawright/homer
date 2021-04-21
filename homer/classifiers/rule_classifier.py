from homer.classifier import Classifier


class RuleClassifier(Classifier):
    def __init__(self, rules):
        self.rules = rules

    def classify(self, **kwargs: dict):
        return all(rule(kwargs) for rule in self.rules)
