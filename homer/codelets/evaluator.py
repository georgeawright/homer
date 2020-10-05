from __future__ import annotations

from homer.bubbles import Perceptlet
from homer.classifier import Classifier
from homer.codelet import Codelet
from homer.strategy import Strategy

from .builder import Builder


class Evaluator(Codelet):
    def __init__(
        self,
        urgency: float,
        codelet_id: str,
        parent_id: str,
        target_perceptlet: Perceptlet,
        child_perceptlet_type: type,
        classifier: Classifier,
    ):
        Codelet.__init__(self, urgency, codelet_id, parent_id)
        self.target_perceptlet = target_perceptlet
        self.child_perceptlet_type = child_perceptlet_type
        self.classifier = classifier

    @classmethod
    def from_components(
        cls,
        urgency: float = None,
        parent_id: str = None,
        strategy: Strategy = None,
        target_perceptlet_type: Perceptlet = None,
        child_perceptlet_type: type = None,
    ) -> Builder:
        codelet_id = None
        target_perceptlet = target_perceptlet_type.instances.get_exigent()
        urgency = urgency if urgency is not None else target_perceptlet.exigency()
        return Builder(
            urgency,
            codelet_id,
            parent_id,
            target_perceptlet,
            child_perceptlet_type,
            target_perceptlet_type.classifier,
        )

    def run(self):
        if self._passes_checks():
            confidence = self.classifier.confidence()
            self.target_perceptlet.quality = confidence
            self.child_codelets.append()
        else:
            self.child_codelets.append(
                Builder.from_components(
                    parent_id=self.codelet_id,
                    target_perceptlet_type=type(self.target_perceptlet),
                    child_perceptlet_type=self.child_perceptlet_type,
                )
            )

    def _reproduce(
        self,
        urgency: float = None,
        child_perceptlet_type: type = None,
        strategy: Strategy = None,
    ) -> Builder:
        if urgency is None:
            urgency = self.urgency / 2
        if child_perceptlet_type is None:
            child_perceptlet_type = self.child_perceptlet_type
        if strategy is None:
            strategy = self.strategy
        target_perceptlet_type = type(self.target_perceptlet)
        return Builder.from_components(
            urgency,
            self.codelet_id,
            strategy,
            target_perceptlet_type,
            child_perceptlet_type,
        )
