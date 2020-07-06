from homer.codelet import Codelet
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters


class TopDownClassifierCodelet(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(self, parent_concept: Concept, target_object, classification_weights):
        self.parent_concept = parent_concept
        self.target_object = target_object
        self.classification_weights = classification_weights

    def run(self):
        confidence_of_class_membership = self.calculate_confidence(
            [
                self.parent_concept.activation,
                self.parent_concept.depth,
                self.parent_concept.distance_from(self.target_object.value),
                self.target_object.proportion_of_neighbours_with_label(
                    self.parent_concept
                ),
            ]
        )
        self.parent_concept.boost_activation(confidence_of_class_membership)
        if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
            self.target_object.add_label(self.parent_concept)
            self.engender_follow_up()

    def calculate_confidence(self, inputs):
        return sum(i[0] * i[1] for i in zip(inputs, self.classification_weights))

    def engender_follow_up(self):
        pass
