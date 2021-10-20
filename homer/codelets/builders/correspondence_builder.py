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
        for correspondence in self.target_view.members:
            if not correspondence.is_compatible_with(self.correspondence):
                return False
        return True

    def _process_structure(self):
        self.correspondence.structure_id = ID.new(Correspondence)
        try:
            if self.correspondence.slot_argument.is_word:
                self._fill_in_word_slot()
            if self.correspondence.slot_argument.is_label:
                self._fill_in_label_slot()
            if self.correspondence.slot_argument.is_relation:
                self._fill_in_relation_slot()
        except MissingStructureError:
            pass
        self.target_view.members.add(self.correspondence)
        self.target_space_one.add(self.correspondence)
        self.target_space_two.add(self.correspondence)
        self.target_structure_one.links_in.add(self.correspondence)
        self.target_structure_one.links_out.add(self.correspondence)
        self.target_structure_two.links_in.add(self.correspondence)
        self.target_structure_two.links_out.add(self.correspondence)
        self.bubble_chamber.correspondences.add(self.correspondence)
        self.bubble_chamber.logger.log(self.correspondence)
        self.child_structures = self.bubble_chamber.new_structure_collection(
            self.correspondence
        )

    def _fill_in_word_slot(self):
        print(
            self.codelet_id,
            self.correspondence.non_slot_argument.lexeme,
            self.correspondence.non_slot_argument.lexeme.concepts,
        )
        self.target_view.slot_values[
            self.correspondence.slot_argument.structure_id
        ] = self.correspondence.non_slot_argument.lexeme.concepts.get()

    def _fill_in_label_slot(self):
        self.target_view.slot_values[
            self.correspondence.slot_argument.structure_id
        ] = self.correspondence.non_slot_argument.parent_concept
        self.target_view.slot_values[
            self.correspondence.slot_argument.start.structure_id
        ] = (
            self.correspondence.non_slot_argument.start.location_in_space(
                self.correspondence.conceptual_space
            )
            if self.correspondence.non_slot_argument.start.is_node
            else self.correspondence.non_slot_argument.start.parent_concept
        )

    def _fill_in_relation_slot(self):
        self.target_view.slot_values[
            self.correspondence.slot_argument.structure_id
        ] = self.correspondence.non_slot_argument.parent_concept
        self.target_view.slot_values[
            self.correspondence.slot_argument.start.structure_id
        ] = (
            self.correspondence.non_slot_argument.start.location_in_space(
                self.correspondence.conceptual_space
            )
            if self.correspondence.non_slot_argument.start.is_node
            else self.correspondence.non_slot_argument.start.parent_concept
        )
        self.target_view.slot_values[
            self.correspondence.slot_argument.end.structure_id
        ] = (
            self.correspondence.non_slot_argument.end.location_in_space(
                self.correspondence.conceptual_space
            )
            if self.correspondence.non_slot_argument.end.is_node
            else self.correspondence.non_slot_argument.end.parent_concept
        )

    def _fizzle(self):
        pass
