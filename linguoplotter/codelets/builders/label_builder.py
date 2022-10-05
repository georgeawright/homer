from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.id import ID
from linguoplotter.tools import average_vector


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
        self._target_structures = target_structures

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import LabelEvaluator

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
        try:
            equivalent_label = self.target_node.labels.where(
                parent_concept=self.parent_concept
            ).get()
            while equivalent_label.is_label:
                self.child_structures.add(equivalent_label)
                equivalent_label = equivalent_label.start
        except MissingStructureError:
            pass
        return True

    def _process_structure(self):
        if not self.child_structures.is_empty():
            self.bubble_chamber.loggers["activity"].log(
                self, "Equivalent label already exists"
            )
            return
        try:
            try:
                conceptual_location = self.target_node.location_in_space(
                    self.parent_concept.parent_basic_space
                )
            except MissingStructureError:
                conceptual_location = self.target_node.location_in_space(
                    self.parent_concept.parent_space
                )
        except NoLocationError:
            conceptual_space = self.parent_concept.parent_space
            self.target_node.parent_space.conceptual_spaces.add(conceptual_space)
            for node in self.target_node.parent_space.contents.where(is_node=True):
                if node.has_location_in_space(conceptual_space):
                    continue
                for location in node.locations:
                    if location.space.is_conceptual_space:
                        try:
                            node.locations.append(
                                conceptual_space.location_from_super_space_location(
                                    location
                                )
                            )
                            conceptual_space.add(node)
                            break
                        except KeyError:
                            pass
            conceptual_location = self.target_node.location_in_space(conceptual_space)
        locations = [
            self.target_node.location_in_space(self.target_node.parent_space),
            conceptual_location,
        ]
        self.child_structures = self.bubble_chamber.new_structure_collection()
        if self.target_node.is_link:
            self._recursively_copy_links()
        if self.target_node not in self.parent_concept.parent_space.contents:
            self.parent_concept.parent_space.add(self.target_node)
        label = self.bubble_chamber.new_label(
            parent_id=self.codelet_id,
            start=self.target_node,
            parent_concept=self.parent_concept,
            locations=locations,
            quality=0,
        )
        self._structure_concept.instances.add(label)
        self._structure_concept.recalculate_exigency()
        self.child_structures.add(label)

    def _recursively_copy_links(self):
        item_to_copy = self.target_node
        while item_to_copy.start.is_link:
            item_to_copy = item_to_copy.start
        previous_item = item_to_copy
        while item_to_copy is not None:
            previous_item = item_to_copy.copy(
                bubble_chamber=self.bubble_chamber,
                parent_id=self.codelet_id,
                start=previous_item.start,
            )
            self.child_structures.add(previous_item)
            try:
                item_to_copy = item_to_copy.labels.get()
            except MissingStructureError:
                item_to_copy = None

    def _fizzle(self):
        pass
