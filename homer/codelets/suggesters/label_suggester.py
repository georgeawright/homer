from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import labeling_exigency
from homer.structures.links import Label
from homer.structures.nodes import Concept


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
        target = bubble_chamber.input_nodes.get(key=labeling_exigency)
        urgency = urgency if urgency is not None else target.unlabeledness
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
        potential_targets = StructureCollection(
            {
                node
                for node in bubble_chamber.input_nodes
                if isinstance(node, parent_concept.instance_type)
            }
        )
        target = potential_targets.get(key=lambda x: parent_concept.proximity_to(x))
        urgency = urgency if urgency is not None else target.unlabeledness
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
        if self.parent_concept is None:
            conceptual_space = StructureCollection(
                {
                    space
                    for space in self.bubble_chamber.conceptual_spaces.where(
                        is_basic_level=True
                    ).where(instance_type=type(self.target_node))
                    if self.target_node.has_location_in_conceptual_space(space)
                }
            ).get()
            location = self.target_node.location_in_conceptual_space(conceptual_space)
            try:
                self.parent_concept = (
                    conceptual_space.contents.where(
                        is_concept=True, structure_type=Label
                    )
                    .near(location)
                    .get()
                )
            except MissingStructureError:
                try:
                    self.parent_concept = (
                        conceptual_space.contents.of_type(Concept)
                        .where(structure_type=Label)
                        .where_not(classifier=None)
                        .get()
                    )
                except MissingStructureError:
                    return False
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
