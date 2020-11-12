from __future__ import annotations
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept, Space
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.spaces import ConceptualSpace

from .relation_builder import RelationBuilder


class CorrespondenceBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_space_one: Space,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_space_two: Space = None,
        target_structure_two: Structure = None,
        target_conceptual_space: ConceptualSpace = None,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_space_one = target_space_one
        self.target_structure_one = target_structure_one
        self.target_space_two = target_space_two
        self.target_structure_two = target_structure_two
        self.target_conceptual_space = target_conceptual_space
        self.parent_concept = parent_concept
        self.confidence = 0.0
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
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
            target_space_one,
            target_structure_one,
            urgency,
            target_space_two,
            target_structure_two,
            target_conceptual_space,
            parent_concept,
        )

    def _passes_preliminary_checks(self):
        if self.target_space_two is None:
            print(self.bubble_chamber.spaces["working spaces"].contents.structures)
            self.target_space_two = self.bubble_chamber.spaces[
                "working spaces"
            ].contents.get_active(exclude=[self.target_space_one])
        try:
            if self.target_structure_two is None:
                self.target_structure_two = self.target_space_two.contents.of_type(
                    type(self.target_structure_one)
                ).get_exigent()
        except MissingStructureError:
            return False
        if self.target_conceptual_space is None:
            try:
                print(self.bubble_chamber.spaces["labeling spaces"].contents.structures)
                print(self.target_structure_one.parent_spaces.structures)
                print(self.target_structure_two.parent_spaces.structures)
                self.target_conceptual_space = StructureCollection.intersection(
                    self.bubble_chamber.spaces["labeling spaces"].contents,
                    self.target_structure_one.parent_spaces,
                    self.target_structure_two.parent_spaces,
                ).get_random()
            except MissingStructureError:
                print("no target conceptual space")
                return False
        if self.parent_concept is None:
            self.parent_concept = self.bubble_chamber.spaces[
                "correspondential concepts"
            ].contents.get_random()
        return not self.target_structure_one.has_correspondence(
            self.target_conceptual_space, self.parent_concept, self.target_structure_two
        )

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            {
                "concept": self.parent_concept,
                "space": self.target_conceptual_space,
                "start": self.target_structure_one,
                "end": self.target_structure_two,
            }
        )

    def _boost_activations(self):
        pass

    def _process_structure(self):
        correspondence = Correspondence(
            self.target_structure_one,
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
            self.parent_concept,
            self.target_conceptual_space,
            self.confidence,
        )
        self.target_structure_one.links_in.add(correspondence)
        self.target_structure_one.links_out.add(correspondence)
        self.target_structure_two.links_in.add(correspondence)
        self.target_structure_two.links_out.add(correspondence)
        self.target_space_one.links_in.add(correspondence)
        self.target_space_one.links_out.add(correspondence)
        self.target_space_two.links_in.add(correspondence)
        self.target_space_two.links_out.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.child_structure = correspondence

    def _engender_follow_up(self):
        new_target = self.target_structure_one.nearby().get_unhappy()
        new_target_conceptual_space = self.bubble_chamber.spaces[
            "labeling spaces"
        ].contents.get_random(exclude=[self.target_conceptual_space])
        self.child_codelets.append(
            CorrespondenceBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_space_one,
                new_target,
                self.confidence,
                target_space_two=self.target_space_two,
                target_conceptual_space=new_target_conceptual_space,
                parent_concept=self.parent_concept,
            )
        )

    def _fizzle(self):
        new_target = self.target_structure_one.nearby().get_unhappy()
        self.child_codelets.append(
            CorrespondenceBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_space_one,
                new_target,
                new_target.unhappiness,
            )
        )

    def _fail(self):
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure_one.parent_spaces.get_random(),
                self.target_structure_one,
                self.target_structure_one.unhappiness,
            )
        )
