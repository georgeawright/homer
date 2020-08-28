from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters


class Evaluator(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.EVALUATOR_CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_perceptlet: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_perceptlet,
            urgency,
            parent_id,
        )
        self.target_type = target_type

    def _fizzle(self):
        self.perceptlet_type.activation.decay(self.location)
        return None

    def _fail(self):
        pass

    def _process_perceptlet(self):
        self.target_perceptlet.quality += self.confidence
        if self.confidence > 0:
            self.target_type.activation.decay(self.location)
        if self.confidence < 0:
            self.target_type.activation.boost(self.location)
