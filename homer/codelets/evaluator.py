from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters


class Evaluator(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.EVALUATOR_CONFIDENCE_THRESHOLD

    def __init__(self):
        pass

    def _process_perceptlet(self):
        self.target_perceptlet.quality += self.confidence
        if self.confidence > 0:
            self.target_type.activation.decay(self.location)
        if self.confidence < 0:
            self.target_type.activation.boost(abs(self.confidence), self.location)
        self.bubble_chamber.logger.log_perceptlet_update(
            self, self.target_perceptlet, "Quality updated"
        )
