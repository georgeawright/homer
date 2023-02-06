from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import activation, exigency
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures import Frame


class ViewSuggester(Suggester):
    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

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
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            targets,
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
        if frame is not None:
            contextual_space = bubble_chamber.input_spaces.get(key=activation)
            targets = bubble_chamber.new_dict(
                {"frame": frame, "contextual_space": contextual_space}, name="targets"
            )
            urgency = urgency if urgency is not None else frame.exigency
            return TopDownViewSuggester.spawn(
                parent_id, bubble_chamber, targets, urgency
            )
        targets = bubble_chamber.new_dict(name="targets")
        urgency = urgency if urgency is not None else 1 - bubble_chamber.satisfaction
        return BottomUpViewSuggester.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _fizzle(self):
        pass


class BottomUpViewSuggester(ViewSuggester):
    def _passes_preliminary_checks(self):
        try:
            self.targets["contextual_space"] = self.bubble_chamber.input_spaces.get(
                key=activation
            )
            self.targets["frame"] = self.bubble_chamber.frames.filter(
                lambda x: x.parent_frame is None
                and not x.is_sub_frame
                and x.exigency > 0
            ).get(key=exigency)
        except MissingStructureError:
            return False
        return True

    def _calculate_confidence(self):
        number_of_equivalent_views = len(
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == self.targets["frame"].parent_concept
                and x.unhappiness > self.FLOATING_POINT_TOLERANCE
            )
        )  # these views should be completed or deleted before more are built
        self.bubble_chamber.loggers["activity"].log(
            "Frame activation: " + str(self.targets["frame"].activation)
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Number of equivalent views: {number_of_equivalent_views}"
        )
        self.confidence = (
            self.targets["frame"].activation * 0.5 ** number_of_equivalent_views
        )


class TopDownViewSuggester(ViewSuggester):
    def _passes_preliminary_checks(self):
        return True

    def _calculate_confidence(self):
        self.confidence = self.urgency
