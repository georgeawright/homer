from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.classifier import Classifier
from homer.codelet import Codelet
from homer.strategy import Strategy


class Evaluator(Codelet):
    def __init__(
        self,
        urgency: float,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_perceptlet: Perceptlet,
        parent_perceptlet_type: type,
        classifier: Classifier,
    ):
        Codelet.__init__(self, urgency, codelet_id, parent_id, bubble_chamber)
        self.target_perceptlet = target_perceptlet
        self.parent_perceptlet_type = parent_perceptlet_type
        self.classifier = classifier

    @classmethod
    def from_components(
        cls,
        urgency: float = None,
        parent_id: str = None,
        strategy: Strategy = None,
        target_perceptlet_type: Perceptlet = None,
        parent_perceptlet_type: type = None,
    ) -> Evaluator:
        codelet_id = None
        target_perceptlet = target_perceptlet_type.instances.get_exigent()
        urgency = urgency if urgency is not None else target_perceptlet.exigency()
        return Evaluator(
            urgency,
            codelet_id,
            parent_id,
            target_perceptlet,
            parent_perceptlet_type,
            target_perceptlet_type.classifier,
        )

    def run(self):
        if self._passes_checks():
            from .selector import Selector

            confidence = self.classifier.confidence()
            self.target_perceptlet.quality = confidence
            self.child_codelets.append(
                Selector.from_components(
                    parent_id=self.codelet_id,
                    target_perceptlet=self.target_perceptlet,
                    parent_perceptlet_type=self.parent_perceptlet_type,
                )
            )
        else:
            from .builder import Builder

            self.child_codelets.append(
                Builder.from_components(
                    parent_id=self.codelet_id,
                    target_perceptlet_type=self.parent_perceptlet_type,
                    child_perceptlet_type=type(self.target_perceptlet),
                )
            )
