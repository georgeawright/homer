from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space, View
from homer.structures.nodes import Concept
from homer.structures.links import Correspondence
from homer.structures.spaces import ConceptualSpace, WorkingSpace


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

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get_active()
        target_space = (
            target_view.input_working_spaces.get_random()
            .contents.of_type(Space)
            .where(is_basic_level=True)
            .get_active()
        )
        target = (
            target_space.contents.not_of_type(Space)
            .not_of_type(Correspondence)
            .get_exigent()
        )
        urgency = urgency if urgency is not None else target.exigency
        return cls.spawn(
            parent_id, bubble_chamber, target_view, target_space, target, urgency
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        correspondence_builder = cls.make(parent_id, bubble_chamber, urgency=urgency)
        correspondence_builder.parent_concept = parent_concept
        return correspondence_builder

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
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
            [
                self.target_structure_one.location_in_space(self.target_space_one),
                self.target_structure_two.location_in_space(self.target_space_two),
            ],
            self.parent_concept,
            self.target_conceptual_space,
            self.target_view,
            0,
        )
        for correspondence in self.target_view.members:
            if not correspondence.is_compatible_with(self.correspondence):
                return False
        return True

    def _process_structure(self):
        self.correspondence.structure_id = ID.new(Correspondence)
        self.target_view.slot_values[self.correspondence.slot_argument.structure_id] = (
            self.correspondence.non_slot_argument.value
            if isinstance(self.correspondence.non_slot_argument, Node)
            else self.correspondence.non_slot_argument.parent_concept
        )
        self.target_view.members.add(self.correspondence)
        self.target_space_one.add(self.correspondence)
        self.target_space_two.add(self.correspondence)
        self.target_structure_one.links_in.add(self.correspondence)
        self.target_structure_one.links_out.add(self.correspondence)
        self.target_structure_two.links_in.add(self.correspondence)
        self.target_structure_two.links_out.add(self.correspondence)
        self.bubble_chamber.correspondences.add(self.correspondence)
        self.bubble_chamber.logger.log(self.correspondence)
        self.child_structures = StructureCollection({self.correspondence})

    def _fizzle(self):
        pass
