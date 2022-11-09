from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import activation, exigency
from linguoplotter.structures import Frame


class ViewSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import ViewBuilder

        return ViewBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        frame: Frame = None,
        urgency: float = None,
    ):
        contextual_space = bubble_chamber.input_spaces.get(key=activation)
        if frame is None:
            frame = (
                bubble_chamber.frames.filter(lambda x: x.exigency > 0)
                .where(parent_frame=None, is_sub_frame=False)
                .get(key=exigency)
            )
        urgency = urgency if urgency is not None else frame.exigency
        targets = bubble_chamber.new_dict(
            {"frame": frame, "contextual_space": contextual_space}, name="targets"
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self) -> bool:
        return True

    def _calculate_confidence(self):
        number_of_equivalent_views = len(
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == self.targets["frame"].parent_concept
            )
        )
        self.bubble_chamber.loggers["activity"].log(
            "Frame activation: " + str(self.targets["frame"].activation)
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Number of equivalent views: {number_of_equivalent_views}"
        )
        self.confidence = self.targets["frame"].activation / (
            number_of_equivalent_views + 1
        )

    def _fizzle(self):
        pass
