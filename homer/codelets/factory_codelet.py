from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet


class FactoryCodelet(Codelet):
    def __init__(
        self, urgency: float, bubble_chamber: BubbleChamber, parent_id: str = ""
    ):
        codelet_id = "FactoryCodelet"
        Codelet.__init__(self, urgency, codelet_id, parent_id, bubble_chamber)

    @classmethod
    def from_components(cls):
        pass

    def run(self) -> Codelet:
        self._select_action()
        self._select_strategy()
        self._select_child_type()
        self._select_target_type()
        self.child_codelets.append(self._spawn_codelet())
        self.child_codelets.append(self._duplicate())

    def _select_action(self):
        raise NotImplementedError

    def _select_strategy(self):
        raise NotImplementedError

    def _select_child_type(self):
        raise NotImplementedError

    def _select_target_type(self):
        raise NotImplementedError

    def _spawn_codelet(self) -> Codelet:
        return self.action.codelet_type.from_components(
            self.codelet_id, self.strategy, self.target_type, self.child_type
        )

    def _duplicate(self) -> FactoryCodelet:
        urgency = (
            1 - self.bubble_chamber.concept_space["satisfaction"].activation.as_scalar()
        )
        return FactoryCodelet(urgency, self.bubble_chamber, self.codelet_id)
