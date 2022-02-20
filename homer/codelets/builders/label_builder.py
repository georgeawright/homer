from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError, NoLocationError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.id import ID
from homer.tools import average_vector


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
        try:
            conceptual_location = self.target_node.location_in_space(
                self.parent_concept.parent_space
            )
        except NoLocationError:
            # TODO: this needs fixing for concepts like mild/central
            for space in self.target_node.parent_spaces:
                if (
                    not space.contents.where(is_concept=True)
                    .filter(
                        lambda x: x.has_correspondence_to_space(
                            self.parent_concept.parent_space
                        )
                    )
                    .is_empty()
                ):
                    source_space = self.parent_concept.parent_space
                    target_space = space
                    break
            source_concepts = [
                concept for concept in source_space.contents.where(is_concept=True)
            ]
            source_concepts.sort(
                key=lambda x: x.location_in_space(source_space).coordinates[0][0]
            )
            source_min_concept = source_concepts[0]
            source_max_concept = source_concepts[-1]
            target_min_concept = source_min_concept.correspondees.filter(
                lambda x: x.has_correspondence_to_space(source_space)
            ).get()
            target_max_concept = source_max_concept.correspondees.filter(
                lambda x: x.has_correspondence_to_space(source_space)
            ).get()
            source_min = source_min_concept.location_in_space(source_space).coordinates[
                0
            ][0]
            source_max = source_max_concept.location_in_space(source_space).coordinates[
                0
            ][0]
            target_min = target_min_concept.location_in_space(target_space).coordinates[
                0
            ][0]
            target_max = target_max_concept.location_in_space(target_space).coordinates[
                0
            ][0]
            conversion_ratio = (source_max - source_min) / (target_max - target_min)
            new_location_coordinates = [
                [(coordinates[0] - target_min) * conversion_ratio]
                for coordinates in self.target_node.location_in_space(
                    target_space
                ).coordinates
            ]
            conceptual_location = Location(new_location_coordinates, source_space)
            self.target_node.locations.append(conceptual_location)
        locations = [
            self.target_node.location_in_space(self.target_node.parent_space),
            conceptual_location,
        ]
        if self.parent_concept.has_relation_with(self.bubble_chamber.concepts["more"]):
            proximity_to_prototype = self.parent_concept.proximity_to(self.target_node)
            concept_location = self.parent_concept.location_in_space(
                self.parent_concept.parent_space
            )
            node_location = self.target_node.location_in_space(
                self.parent_concept.parent_space
            )
            if (
                average_vector(node_location.coordinates)[0]
                > concept_location.coordinates[0][0]
            ):
                magnitude_coordinates = [[1 - proximity_to_prototype]]
            else:
                magnitude_coordinates = [[proximity_to_prototype - 1]]
            locations.append(
                Location(
                    magnitude_coordinates,
                    self.bubble_chamber.conceptual_spaces["magnitude"],
                )
            )
            self.target_node.parent_space.conceptual_spaces.add(
                self.bubble_chamber.conceptual_spaces["magnitude"]
            )
        if self.parent_concept.has_relation_with(self.bubble_chamber.concepts["less"]):
            proximity_to_prototype = self.parent_concept.proximity_to(self.target_node)
            concept_location = self.parent_concept.location_in_space(
                self.parent_concept.parent_space
            )
            node_location = self.target_node.location_in_space(
                self.parent_concept.parent_space
            )
            if (
                average_vector(node_location.coordinates)[0]
                > concept_location.coordinates[0][0]
            ):
                magnitude_coordinates = [[proximity_to_prototype - 1]]
            else:
                magnitude_coordinates = [[1 - proximity_to_prototype]]
            locations.append(
                Location(
                    magnitude_coordinates,
                    self.bubble_chamber.conceptual_spaces["magnitude"],
                )
            )
            self.target_node.parent_space.conceptual_spaces.add(
                self.bubble_chamber.conceptual_spaces["magnitude"]
            )
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
