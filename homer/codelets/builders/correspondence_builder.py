from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.links import Correspondence


class CorrespondenceBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.target_view = None
        self.target_space_one = None
        self.target_structure_one = None
        self.target_space_two = None
        self.target_structure_two = None
        self.target_conceptual_space = None
        self.parent_concept = None
        self.parent_space = None
        self.correspondence = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import CorrespondenceEvaluator

        return CorrespondenceEvaluator

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
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.target_space_one = self._target_structures["target_space_one"]
        self.target_space_two = self._target_structures["target_space_two"]
        self.target_conceptual_space = self._target_structures[
            "target_conceptual_space"
        ]
        self.parent_concept = self._target_structures["parent_concept"]
        self.target_view = self._target_structures["target_view"]
        if self.target_view.has_member(
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
        ):
            return False
        self.correspondence = Correspondence(
            None,
            self.codelet_id,
            self.target_structure_one,
            self.bubble_chamber.new_structure_collection(
                self.target_structure_one, self.target_structure_two
            ),
            [self.target_structure_one.location, self.target_structure_two.location],
            self.parent_concept,
            self.target_conceptual_space,
            self.target_view,
            0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        return self.target_view.can_accept_member(self.correspondence)

    def _process_structure(self):
        if not self.correspondence.slot_argument.parent_concept.is_filled_in:
            self.bubble_chamber.new_relation(
                parent_id=self.codelet_id,
                start=self.correspondence.slot_argument.parent_concept,
                end=self.correspondence.non_slot_argument.parent_concept,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
        self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.correspondence.start,
            end=self.correspondence.end,
            locations=self.correspondence.locations,
            parent_concept=self.correspondence.parent_concept,
            conceptual_space=self.correspondence.conceptual_space,
            parent_view=self.target_view,
        )
        self.child_structures = self.bubble_chamber.new_structure_collection(
            self.correspondence
        )

    def _fizzle(self):
        pass
