from homer.bubbles import Concept, Perceptlet
from homer.classifier import Classifier


class GroupLabelClassifier(Classifier):
    def confidence(self, target_perceptlet: Perceptlet, concept: Concept):
        total_activation = 0.0
        for member in target_perceptlet.members:
            for label in member.labels:
                if label.parent_concept == concept:
                    total_activation += label.activation.as_scalar()
        return total_activation / target_perceptlet.size
