from __future__ import annotations
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structures import Space, View
from homer.structures.nodes import Concept
from homer.structures.links import Correspondence
from homer.structures.spaces import ConceptualSpace, WorkingSpace

from .relation_builder import RelationBuilder


class CorrespondenceBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_space_one: Space,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_space_two: Space = None,
        target_structure_two: Structure = None,
        target_conceptual_space: ConceptualSpace = None,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.target_space_one = target_space_one
        self.target_structure_one = target_structure_one
        self.target_space_two = target_space_two
        self.target_structure_two = target_structure_two
        self.target_conceptual_space = target_conceptual_space
        self.parent_concept = parent_concept
        self.parent_space = None
        self.correspondence = None
        self.child_structure = None

    @classmethod
    def get_target_class(cls):
        return Correspondence

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_space_one: Space,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_space_two: Space = None,
        target_structure_two: Structure = None,
        target_conceptual_space: ConceptualSpace = None,
        parent_concept: Concept = None,
    ):
        qualifier = "TopDown" if parent_concept is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_space_one,
            target_structure_one,
            urgency,
            target_space_two,
            target_structure_two,
            target_conceptual_space,
            parent_concept,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.views.get_active()
        target_space = bubble_chamber.working_spaces.where(
            is_basic_level=True
        ).get_active()
        target = target_space.contents.not_of_type(Space).get_exigent()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_view,
            target_space,
            target,
            target.exigency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.target_space_two is None:
            try:
                self.target_space_two = (
                    self.bubble_chamber.frames.get_active()
                    .contents.of_type(WorkingSpace)
                    .get_random()
                )
            except MissingStructureError:
                return False
        try:
            if self.target_structure_two is None:
                self.target_structure_two = self.target_space_two.contents.of_type(
                    type(self.target_structure_one)
                ).get_exigent()
        except MissingStructureError:
            return False
        if self.target_conceptual_space is None:
            self.target_conceptual_space = self.target_space_one.conceptual_space
        if self.target_conceptual_space != self.target_space_two.conceptual_space:
            return False
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.spaces["correspondential concepts"]
                .contents.of_type(ConceptualSpace)
                .get_random()
                .contents.of_type(Concept)
                .get_random()
            )
        self.parent_space = self.bubble_chamber.get_super_space(
            self.target_space_one, self.target_space_two
        )
        if self.target_view.has_member(
            self.parent_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        ):
            return False
        self.correspondence = Correspondence(
            None,
            self.codelet_id,
            self.target_structure_one,
            self.target_structure_two,
            Location.for_correspondence_between(
                self.target_structure_one.location_in_space(self.target_space_one),
                self.target_structure_two.location_in_space(self.target_space_two),
                self.parent_space,
            ),
            self.target_space_one,
            self.target_space_two,
            self.parent_concept,
            self.target_conceptual_space,
            self.target_view,
            0,
        )
        for correspondence in self.target_view.members:
            if not correspondence.is_compatible_with(self.correspondence):
                return False
        return True

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept,
            space=self.target_conceptual_space,
            start=self.target_structure_one,
            end=self.target_structure_two,
        )

    def _process_structure(self):
        self.correspondence.structure_id = ID.new(Correspondence)
        self.parent_space.add(self.correspondence)
        self.target_structure_one.links_in.add(self.correspondence)
        self.target_structure_one.links_out.add(self.correspondence)
        self.target_structure_two.links_in.add(self.correspondence)
        self.target_structure_two.links_out.add(self.correspondence)
        self.bubble_chamber.correspondences.add(self.correspondence)
        self.bubble_chamber.logger.log(self.correspondence)
        self.child_structure = self.correspondence

    def _fizzle(self):
        self.child_codelets.append(self.make(self.codelet_id, self.bubble_chamber))

    def _fail(self):
        try:
            self.child_codelets.append(
                RelationBuilder.make(self.codelet_id, self.bubble_chamber)
            )
        except MissingStructureError:
            pass
