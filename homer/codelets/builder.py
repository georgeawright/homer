from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.classifier import Classifier
from homer.codelet import Codelet
from homer.errors import FailedGettingRequirements
from homer.strategy import Strategy


class Builder(Codelet):
    def __init__(
        self,
        urgency: float,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_perceptlet: Perceptlet,
        child_perceptlet_type: type,
        classifier: Classifier,
    ):
        Codelet.__init__(self, urgency, codelet_id, parent_id, bubble_chamber)
        self.target_perceptlet = target_perceptlet
        self.child_perceptlet_type = child_perceptlet_type
        self.classifier = classifier

    @classmethod
    def from_components(
        cls,
        urgency: float = None,
        parent_id: str = None,
        strategy: Strategy = None,
        target_perceptlet_type: type = None,
        child_perceptlet_type: type = None,
    ) -> Builder:
        codelet_id = None
        strategy = strategy if strategy is not None else Strategy["BottomUp"]
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
        try:
            requirements = self.target_perceptlet_type.get_requirements(
                self.strategy, self.target_perceptlet_type
            )
        except FailedGettingRequirements:
            return self.child_codelets.append(
                self._reproduce(
                    child_perceptlet_type=self.child_perceptlet_type.previous,
                )
            )
        confidence = self.classifier.confidence(requirements)
        if confidence > self.CONFIDENCE_THRESHOLD:
            self.child_perceptlet = self.child_perceptlet_type.build()
            self.child_codelets.append(self._reproduce(urgency=confidence))
        else:
            self.child_codelets.append(self._reproduce(strategy=Strategy["BottomUp"]))

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
