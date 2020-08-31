from homer import fuzzy
from homer.bubbles import Concept, Perceptlet
from homer.classifier import Classifier
from homer.perceptlet_collection import PerceptletCollection


class CorrespondenceClassifier(Classifier):
    def confidence(
        self, perceptlet_1: Perceptlet, perceptlet_2: Perceptlet, concept: Concept,
    ):
        confidence_of_proximity = self._confidence_of_proximity(
            perceptlet_1, perceptlet_2, concept
        )
        return max(confidence_of_proximity, 1 - confidence_of_proximity)

    def _confidence_of_proximity(
        self, perceptlet_1: Perceptlet, perceptlet_2: Perceptlet, concept: Concept,
    ) -> float:
        """Returns a high value for groups labeled with a proximate concept."""
        return fuzzy.AND(
            perceptlet_1.has_label_in_space(concept),
            perceptlet_2.has_label_in_space(concept),
            fuzzy.OR(
                len(self._common_labels_in_space(perceptlet_1, perceptlet_2, concept))
                > 1,
                concept.proximity_between(
                    perceptlet_1.get_value(concept), perceptlet_2.get_value(concept),
                ),
            ),
        )

    def _common_labels_in_space(
        self, perceptlet_1: Perceptlet, perceptlet_2: Perceptlet, concept: Concept,
    ):
        return PerceptletCollection.intersection(
            perceptlet_1.labels_in_space(concept),
            perceptlet_2.labels_in_space(concept),
        )
