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
        action_type = self.bubble_chamber.concepts["build"]
        links_to_structure_nodes = StructureCollection(
            {
                link
                for link in action_type.links_out
                if link.end in self.bubble_chamber.spaces["structures"].contents
            }
        )
        structure_type = links_to_structure_nodes.get_active().end
        follow_up_parent_concept = self._get_concept_for_structure_type(structure_type)
        follow_up_type = self._get_follow_up_type(action_type, structure_type)
        proportion_of_follow_up_type_on_coderack = (
            self.coderack.number_of_codelets_of_type(follow_up_type) / 50
        )
        if proportion_of_follow_up_type_on_coderack < random.random():
            follow_up = follow_up_type.make_top_down(
                self.codelet_id, self.bubble_chamber, follow_up_parent_concept
            )
            self.child_codelets.append(follow_up)

    def _get_concept_for_structure_type(self, structure_type: Concept) -> Concept:
        if structure_type == self.bubble_chamber.concepts["label"]:
            return (
                self.bubble_chamber.spaces["label concepts"]
                .contents.of_type(ConceptualSpace)
                .where(is_basic_level=True)
                .get_active()
                .contents.of_type(Concept)
                .where_not(classifier=None)
                .get_active()
            )
        if structure_type == self.bubble_chamber.concepts["relation"]:
            return (
                self.bubble_chamber.spaces["relational concepts"]
                .contents.of_type(ConceptualSpace)
                .get_active()
                .contents.of_type(Concept)
                .where_not(classifier=None)
                .get_active()
            )
        if structure_type == self.bubble_chamber.concepts["correspondence"]:
            return (
                self.bubble_chamber.spaces["correspondential concepts"]
                .contents.of_type(ConceptualSpace)
                .get_active()
                .contents.of_type(Concept)
                .get_active()
            )
        if structure_type == self.bubble_chamber.concepts["phrase"]:
            return self.bubble_chamber.rules.get_active()
        return None
