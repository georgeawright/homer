from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import activation, exigency
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures import Frame


class FrameSuggester(Suggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import FrameBuilder

        return FrameBuilder

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
        urgency: float = None,
    ):
        targets = bubble_chamber.new_dict(name="targets")
        urgency = urgency if urgency is not None else 1 - bubble_chamber.satisfaction
        return BottomUpFrameSuggester.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        frame: Frame,
        urgency: float = None,
    ):
        targets = bubble_chamber.new_dict({"frame": frame}, name="targets")
        urgency = urgency if urgency is not None else frame.exigency
        return TopDownFrameSuggester.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["frame"]

    def _calculate_confidence(self):
        self.confidence = self.urgency

    def _fizzle(self):
        pass


class BottomUpFrameSuggester(FrameSuggester):
    def _passes_preliminary_checks(self):
        try:
            self.targets["view"] = self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == self.bubble_chamber.concepts["conjunction"]
            ).get(key=exigency)
            self.targets["frame"] = self.bubble_chamber.frames.filter(
                lambda x: x.is_secondary
                and not any(
                    [
                        x.subsumes(frame)
                        for frame in self.targets["view"].secondary_frames
                    ]
                )
            ).get()
        except MissingStructureError:
            return False
        return True


class TopDownFrameSuggester(FrameSuggester):
    def _passes_preliminary_checks(self):
        try:
            self.targets["view"] = self.bubble_chamber.views.filter(
                lambda x: not any(
                    [
                        frame.subsumes(self.targets["frame"])
                        for frame in x.secondary_frames
                    ]
                )
            ).get(key=activation)
        except MissingStructureError:
            return False
