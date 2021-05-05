import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets import Factory
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace


class ConceptDrivenFactory(Factory):
    """Finds an active concept to spawn a top down codelet for"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def _engender_follow_up(self):
        follow_up_class = self._decide_follow_up_class()
        follow_up_parent_concept = self._decide_follow_up_parent_concept(
            follow_up_class
        )
        proportion_of_follow_up_class_on_coderack = (
            self.coderack.number_of_codelets_of_type(follow_up_class) / 50
        )
        if proportion_of_follow_up_class_on_coderack < random.random():
            follow_up = follow_up_class.make_top_down(
                self.codelet_id, self.bubble_chamber, follow_up_parent_concept
            )
            self.child_codelets.append(follow_up)

    def _decide_follow_up_class(self):
        action_concept = self.bubble_chamber.concepts["build"]
        space_concept = self.bubble_chamber.concepts["inner"]
        direction_concept = self.bubble_chamber.concepts["forward"]
        structure_concept = StructureCollection(
            {
                self.bubble_chamber.concepts["label"],
                self.bubble_chamber.concepts["relation"],
                self.bubble_chamber.concepts["correspondence"],
                self.bubble_chamber.concepts["phrase"],
            }
        ).get_active()
        return self._get_codelet_type_from_concepts(
            action=action_concept,
            space=space_concept,
            direction=direction_concept,
            structure=structure_concept,
        )

    def _decide_follow_up_parent_concept(self, follow_up_class: type) -> Concept:
        from homer.codelets.builders import (
            CorrespondenceBuilder,
            LabelBuilder,
            PhraseBuilder,
            RelationBuilder,
        )

        if follow_up_class == CorrespondenceBuilder:
            return (
                self.bubble_chamber.spaces["correspondential concepts"]
                .contents.of_type(ConceptualSpace)
                .get_active()
                .contents.of_type(Concept)
                .get_active()
            )
        if follow_up_class == LabelBuilder:
            return (
                self.bubble_chamber.spaces["label concepts"]
                .contents.of_type(ConceptualSpace)
                .where(is_basic_level=True)
                .get_active()
                .contents.of_type(Concept)
                .where_not(classifier=None)
                .get_active()
            )
        if follow_up_class == PhraseBuilder:
            return self.bubble_chamber.rules.get_active()

        if follow_up_class == RelationBuilder:
            return (
                self.bubble_chamber.spaces["relational concepts"]
                .contents.of_type(ConceptualSpace)
                .get_active()
                .contents.of_type(Concept)
                .where_not(classifier=None)
                .get_active()
            )
        return None
