from __future__ import annotations
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

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target = bubble_chamber.frames.get_active()
        urgency = urgency if urgency is not None else target.exigency
        return cls.spawn(parent_id, bubble_chamber, target, target.unhappiness)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.frame is None:
            for space in self.target_spaces:
                if isinstance(space, Frame):
                    self.frame = space
                    return True
        return False

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [space.activation for space in self.target_spaces]
        )

    def _process_structure(self):
        view_id = ID.new(View)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        view_output = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=self.frame.parent_concept,
            conceptual_space=self.frame.conceptual_space,
            locations=[view_location],
            contents=StructureCollection(),
            no_of_dimensions=1,
            dimensions=[],
            sub_spaces=[],
        )
        view = View(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=self.target_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.logger.log(view)
        self.child_structure = view

    def _engender_follow_up(self):
        from homer.codelets.evaluators import ViewEvaluator

        self.child_codelets.append(
            ViewEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        from homer.codelets.builders import CorrespondenceBuilder

        self.child_codelets.append(
            CorrespondenceBuilder.make(self.codelet_id, self.bubble_chamber)
        )

    def _fail(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )
