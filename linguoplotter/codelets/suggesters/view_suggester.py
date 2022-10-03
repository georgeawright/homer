from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
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
        self.frame = target_structures.get("frame")
        self.contextual_space = target_structures.get("contextual_space")
        self.conceptual_spaces_map = {}
        self.prioritized_conceptual_spaces = target_structures.get(
            "prioritized_conceptual_spaces", bubble_chamber.new_structure_collection()
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
            frame = bubble_chamber.frames.where(
                parent_frame=None, is_sub_frame=False
            ).get(key=exigency)
        urgency = urgency if urgency is not None else frame.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"frame": frame, "contextual_space": contextual_space},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    @property
    def targets_dict(self):
        return {
            "frame": self.frame,
            "contextual_space": self.contextual_space,
            "conceptual_spaces_map": self.conceptual_spaces_map,
            "prioritized_conceptual_spaces": self.prioritized_conceptual_spaces,
        }

    @property
    def target_structures(self):
        return self.bubble_chamber.new_structure_collection(
            self.frame, self.contextual_space
        )

    def _passes_preliminary_checks(self) -> bool:
        self.bubble_chamber.loggers["activity"].log(
            self, f"frame activation: {self.frame.activation}"
        )
        input_space_concept = self.contextual_space.parent_concept
        frame_input_space = (
            self.frame.input_space
            if self.frame.input_space.parent_concept == input_space_concept
            else self.frame.output_space
        )
        for conceptual_space in frame_input_space.conceptual_spaces:
            if (
                not conceptual_space.is_slot
                and not conceptual_space in self.contextual_space.conceptual_spaces
                and not any(
                    conceptual_space in space.sub_spaces
                    for space in self.contextual_space.conceptual_spaces
                )
            ):
                self.bubble_chamber.loggers["activity"].log(
                    self,
                    f"{conceptual_space} is not a slot and "
                    + f"is not in {self.contextual_space} conceptual spaces",
                )
                return False
            if conceptual_space.is_slot:
                try:
                    self.conceptual_spaces_map[
                        conceptual_space
                    ] = self.prioritized_conceptual_spaces.filter(
                        lambda x: x not in self.conceptual_spaces_map.values()
                        and conceptual_space.subsumes(x)
                    ).get(
                        key=activation
                    )
                except MissingStructureError:
                    try:
                        self.conceptual_spaces_map[conceptual_space] = (
                            StructureCollection.union(
                                self.contextual_space.conceptual_spaces,
                                *[
                                    space.sub_spaces
                                    for space in self.contextual_space.conceptual_spaces
                                ],
                            )
                            .filter(
                                lambda x: x not in self.conceptual_spaces_map.values()
                                and conceptual_space.subsumes(x)
                            )
                            .get(key=activation)
                        )
                    except MissingStructureError:
                        self.bubble_chamber.loggers["activity"].log_dict(
                            self, self.conceptual_spaces_map, "Conceptual Space Map"
                        )
                        self.bubble_chamber.loggers["activity"].log(
                            self,
                            f"Unable to find space subsumed by {conceptual_space.structure_id}",
                        )
                        return False
        return True

    def _calculate_confidence(self):
        number_of_equivalent_views = len(
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept == self.frame.parent_concept
            )
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Frame activation: {self.frame.activation}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Number of equivalent views: {number_of_equivalent_views}"
        )
        try:
            self.confidence = self.frame.activation / number_of_equivalent_views
        except ZeroDivisionError:
            self.confidence = self.frame.activation

    def _fizzle(self):
        pass
