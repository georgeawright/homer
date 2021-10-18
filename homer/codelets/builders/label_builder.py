from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structures.links import Label


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
        self._target_structures = target_structures
        self.target_node = None
        self.parent_concept = None

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

    def _passes_preliminary_checks(self):
        self.parent_concept = self._target_structures["parent_concept"]
        self.target_node = self._target_structures["target_node"]
        return not self.target_node.has_label(self.parent_concept)

    def _process_structure(self):
        parent_concept_coordinates = self.parent_concept.location_in_space(
            self.parent_concept.parent_space
        ).coordinates
        if not self.target_node.has_location_in_space(self.parent_concept.parent_space):
            self.target_node.locations.append(
                Location(parent_concept_coordinates, self.parent_concept.parent_space)
            )
            self.parent_concept.parent_space.add(self.target_node)
        label = Label(
            ID.new(Label),
            self.codelet_id,
            self.target_node,
            self.bubble_chamber.new_structure_collection(self.target_node),
            self.parent_concept,
            self.target_node.parent_space,
            0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        label.activation = self.INITIAL_STRUCTURE_ACTIVATION
        self.target_node.parent_space.add(label)
        self.target_node.links_out.add(label)
        self.bubble_chamber.labels.add(label)
        self.bubble_chamber.logger.log(label)
        self.child_structures = self.bubble_chamber.new_structure_collection(label)

    def _fizzle(self):
        pass
