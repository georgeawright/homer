from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location


class LabelBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_node = target_structures.get("target_node")
        self.parent_concept = target_structures.get("parent_concept")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import LabelEvaluator

        return LabelEvaluator

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
        return self.bubble_chamber.concepts["label"]

    @property
    def targets_dict(self):
        return {
            "target_node": self.target_node,
            "parent_concept": self.parent_concept,
        }

    def _passes_preliminary_checks(self):
        return not self.target_node.has_label(self.parent_concept)

    def _process_structure(self):
        if self.target_node.is_label:
            # TODO: test
            self.target_node = self.target_node.copy(
                bubble_chamber=self.bubble_chamber, parent_id=self.codelet_id
            )
        parent_concept_coordinates = self.parent_concept.location_in_space(
            self.parent_concept.parent_space
        ).coordinates
        if self.target_node not in self.parent_concept.parent_space:
            # TODO: create space if doesn't exist?
            self.parent_concept.parent_space.add(self.target_node)
        label = self.bubble_chamber.new_label(
            parent_id=self.codelet_id,
            start=self.target_node,
            parent_concept=self.parent_concept,
            locations=[
                self.target_node.location_in_space(self.parent_concept.parent_space)
            ],
            quality=0,
        )
        label.activation = self.INITIAL_STRUCTURE_ACTIVATION
        self.child_structures = self.bubble_chamber.new_structure_collection(label)

    def _fizzle(self):
        pass
