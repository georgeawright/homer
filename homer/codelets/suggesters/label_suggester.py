import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.structures.links import Label
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace
from homer.tools import project_item_into_space


class LabelSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_node = None
        self.parent_concept = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import LabelBuilder

        return LabelBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["parent_concept"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
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
        target = bubble_chamber.input_nodes.get_exigent()
        urgency = urgency if urgency is not None else target.unlinkedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_node": target, "parent_concept": None},
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target = StructureCollection(
            {
                node
                for node in bubble_chamber.input_nodes
                if isinstance(node.value, parent_concept.instance_type)
            }
        ).get_unhappy()
        urgency = urgency if urgency is not None else target.unlinkedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_node": target, "parent_concept": parent_concept},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    @property
    def target_structures(self):
        return StructureCollection({self.target_node})

    def _passes_preliminary_checks(self):
        self.target_node = self._target_structures["target_node"]
        self.parent_concept = self._target_structures["parent_concept"]
        if self.parent_concept is None and self.target_node.is_word:
            self.parent_concept = random.sample(
                self.target_node.lexeme.parts_of_speech[self.target_node.word_form],
                1,
            )[0]
        if self.parent_concept is None and self.target_node.is_chunk:
            conceptual_space = (
                self.bubble_chamber.spaces["label concepts"]
                .contents.of_type(ConceptualSpace)
                .where(is_basic_level=True)
                .where(instance_type=type(self.target_node.value))
                .get_random()
            )
            location = Location(
                getattr(
                    self.target_node, conceptual_space.parent_concept.relevant_value
                ),
                conceptual_space,
            )
            try:
                self.parent_concept = (
                    conceptual_space.contents.of_type(Concept)
                    .where_not(classifier=None)
                    .near(location)
                    .get_random()
                )
            except MissingStructureError:
                self.parent_concept = (
                    conceptual_space.contents.of_type(Concept)
                    .where_not(classifier=None)
                    .get_random()
                )
        if self.parent_concept is None:
            return False
        self._target_structures["parent_concept"] = self.parent_concept
        return not self.target_node.has_label(self.parent_concept)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept, start=self.target_node
        )

    def _fizzle(self):
        pass
