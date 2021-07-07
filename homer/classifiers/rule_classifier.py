from homer.classifier import Classifier


class RuleClassifier(Classifier):
    def __init__(self, rule):
        self.rule = rule

    def classify(self, **kwargs: dict):
        return self.rule(kwargs)
