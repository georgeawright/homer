from homer.bubbles import Concept, Perceptlet
from homer.classifier import Classifier


class LabelClassifier(Classifier):
    def confidence(self, target_perceptlet: Perceptlet, concept: Concept):
        proximity = concept.proximity_to(target_perceptlet.get_value(concept))
        try:
            neighbours = target_perceptlet.neighbours.proportion_with_label(concept)
            return sum([0.6 * proximity, 0.4 * neighbours])
        except ZeroDivisionError:
            return proximity
