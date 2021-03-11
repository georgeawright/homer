from __future__ import annotations
from abc import abstractclassmethod
import statistics
from typing import List, Set, Tuple

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.links import Correspondence
from homer.structures.spaces import Frame, WorkingSpace


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_spaces: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_spaces = target_spaces
        self.second_target_view = None
        self.correspondences = None
        self.correspondences_to_add = None
        self.child_structure = None
        self.frame = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_spaces: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_spaces,
            urgency,
        )

    @abstractclassmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        pass

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        for view in self.bubble_chamber.views:
            if view.input_spaces == self.target_spaces:
                return False
        if self.frame is None:
            for space in self.target_spaces:
                if isinstance(space, Frame):
                    self.frame = space
        return self.frame is not None

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [space.activation for space in self.target_spaces]
        )

    def _fizzle(self):
        from homer.codelets.builders import CorrespondenceBuilder

        self.child_codelets.append(self.make(self.codelet_id, self.bubble_chamber))

    def _fail(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )
