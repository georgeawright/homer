from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection


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
        self.target_view = None
        self.target_projectee = None
        self.frame = None
        self.frame_correspondee = None
        self.correspondence_to_non_frame = None
        self.non_frame = None
        self.non_frame_correspondee = None

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
    def target_structures(self):
        return StructureCollection({self.target_view, self.target_projectee})

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_projectee = self._target_structures["target_projectee"]
        self._target_structures["target_correspondence"] = None
        self._target_structures["frame_correspondee"] = None
        self._target_structures["non_frame"] = None
        self._target_structures["non_frame_correspondee"] = None
        try:
            self.frame_correspondee = StructureCollection(
                {
                    correspondence.start
                    if correspondence.start != self.target_projectee
                    else correspondence.end
                    for correspondence in self.target_projectee.correspondences
                    if correspondence.start.is_slot and correspondence.end.is_slot
                }
            ).get()
            self._target_structures["frame_correspondee"] = self.frame_correspondee
            self.correspondence_to_non_frame = StructureCollection(
                {
                    correspondence
                    for correspondence in self.frame_correspondee.correspondences
                    if correspondence.start.parent_space
                    != correspondence.end.parent_space
                    and correspondence in self.target_view.members
                }
            ).get()
            self._target_structures[
                "target_correspondence"
            ] = self.correspondence_to_non_frame
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
            self._target_structures["non_frame"] = self.non_frame
            self._target_structures[
                "non_frame_correspondee"
            ] = self.non_frame_correspondee
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
