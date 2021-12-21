from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class ProjectionSuggester(Suggester):
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
        self.target_view = target_structures.get("target_view")
        self.target_projectee = target_structures.get("target_projectee")
        self.frame = target_structures.get("frame")
        self.frame_correspondee = target_structures.get("frame_correspondee")
        self.correspondence_to_non_frame = target_structures.get(
            "correspondence_to_non_frame"
        )
        self.non_frame = target_structures.get("non_frame")
        self.non_frame_correspondee = target_structures.get("non_frame_correspondee")

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

    @property
    def targets_dict(self):
        return {
            "target_view": self.target_view,
            "target_projectee": self.target_projectee,
            "frame": self.frame,
            "frame_correspondee": self.frame_correspondee,
            "correspondence_to_non_frame": self.correspondence_to_non_frame,
            "non_frame": self.non_frame,
            "non_frame_correspondee": self.non_frame_correspondee,
        }

    def _passes_preliminary_checks(self):
        try:
            self.frame_correspondee = self.bubble_chamber.new_structure_collection(
                *[
                    correspondence.start
                    if correspondence.start != self.target_projectee
                    else correspondence.end
                    for correspondence in self.target_projectee.correspondences
                    if correspondence.start.is_slot and correspondence.end.is_slot
                ]
            ).get()
            self.correspondence_to_non_frame = (
                self.bubble_chamber.new_structure_collection(
                    *[
                        correspondence
                        for correspondence in self.frame_correspondee.correspondences
                        if correspondence.start.parent_space
                        != correspondence.end.parent_space
                        and correspondence in self.target_view.members
                    ]
                ).get()
            )
            self.non_frame, self.non_frame_correspondee = (
                (
                    self.correspondence_to_non_frame.start.parent_space,
                    self.correspondence_to_non_frame.start,
                )
                if self.correspondence_to_non_frame.start != self.frame_correspondee
                else (
                    self.correspondence_to_non_frame.end.parent_space,
                    self.correspondence_to_non_frame.end,
                )
            )
            return (
                self.frame_correspondee.structure_id in self.target_view.slot_values
                and self.target_projectee.structure_id
                not in self.target_view.slot_values
            )
        except MissingStructureError:
            return (
                not self.target_projectee.is_slot
                and not self.target_projectee.has_correspondence_to_space(
                    self.target_view.output_space
                )
            )

    def _calculate_confidence(self):
        self.confidence = (
            self.correspondence_to_non_frame.activation
            if self.target_projectee.is_slot
            else 1.0
        )

    def _fizzle(self):
        pass
