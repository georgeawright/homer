from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import RelationBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation
from homer.tools import add_vectors, project_item_into_space


class RelationProjectionBuilder(RelationBuilder):
    """Builds a relation in a new space with a correspondence to a node in another space.
    Sets or alters the value or coordinates of its arguments
    according to the parent concept's prototype."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        RelationBuilder.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_view = None
        self.target_structure_one = None
        self.target_structure_two = None
        self.target_word = None
        self.parent_concept = None
        self.conceptual_space = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.relation_evaluators import (
            RelationProjectionEvaluator,
        )

        return RelationProjectionEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: Structure,
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
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.target_word = self._target_structures["target_word"]
        self.target_space = self._target_structures["target_space"]
        self.parent_concept = self._target_structures["parent_concept"]
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        ) and not self.target_word.has_correspondence_to_space(
            self.target_view.interpretation_space
        )

    def _process_structure(self):
        self.bubble_chamber.logger.log(self.target_space)
        if self.target_structure_one not in self.target_space.contents:
            project_item_into_space(self.target_structure_one, self.target_space)
        if self.target_structure_two not in self.target_space.contents:
            project_item_into_space(self.target_structure_two, self.target_space)
        if self.target_space.parent_concept.relevant_value == "value":
            self.target_structure_one.value = self.target_space.parent_concept.value
            self.target_structure_two.value = add_vectors(
                self.target_structure_one.value, self.parent_concept.value
            )
        if self.target_space.parent_concept.relevant_value == "coordinates":
            self.target_structure_one.location_in_space(
                self.target_space
            ).coordinates = self.target_space.parent_concept.location_in_space(
                self.conceptual_space
            ).coordinates
            self.target_structure_two.location_in_space(
                self.target_space
            ).coordinates = add_vectors(
                self.target_space.parent_concept.location_in_space(
                    self.conceptual_space
                ).coordinates,
                self.parent_concept.value,
            )
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=self.codelet_id,
            start=self.target_structure_one,
            end=self.target_structure_two,
            parent_concept=self.parent_concept,
            parent_space=self.target_space,
            quality=0,
        )
        self.target_structure_one.links_out.add(relation)
        self.target_structure_two.links_in.add(relation)
        start_space = self.target_word.parent_space
        end_space = self.target_space
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=self.codelet_id,
            start=self.target_word,
            end=relation,
            start_space=start_space,
            end_space=end_space,
            locations=[self.target_word.location, relation.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.conceptual_space,
            parent_view=self.target_view,
            quality=0,
        )
        relation.links_out.add(correspondence)
        relation.links_in.add(correspondence)
        self.target_word.links_out.add(correspondence)
        self.target_word.links_in.add(correspondence)
        start_space.add(correspondence)
        end_space.add(correspondence)
        self.target_view.members.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.bubble_chamber.logger.log(self.target_view)
        self.child_structures = StructureCollection({relation, correspondence})
