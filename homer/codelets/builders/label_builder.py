from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


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
        self.child_structures = self.bubble_chamber.new_structure_collection()
        if self.target_node.is_link:
            self._recursively_copy_links()
        if self.target_node not in self.parent_concept.parent_space.contents:
            self.parent_concept.parent_space.add(self.target_node)
        label = self.bubble_chamber.new_label(
            parent_id=self.codelet_id,
            start=self.target_node,
            parent_concept=self.parent_concept,
            locations=[
                self.target_node.location_in_space(self.target_node.parent_space),
                self.target_node.location_in_space(self.parent_concept.parent_space),
            ],
            quality=0,
        )
        self.child_structures.add(label)

    def _recursively_copy_links(self):
        item_to_copy = self.target_node
        while item_to_copy.start.is_link:
            item_to_copy = item_to_copy.start
        previous_item = item_to_copy.start
        while item_to_copy is not None:
            previous_item = item_to_copy.copy(
                bubble_chamber=self.bubble_chamber,
                parent_id=self.codelet_id,
                start=previous_item,
            )
            self.child_structures.add(previous_item)
            try:
                item_to_copy = item_to_copy.labels.get()
            except MissingStructureError:
                item_to_copy = None

    def _fizzle(self):
        pass
