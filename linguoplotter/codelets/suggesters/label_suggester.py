from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structure_collection_keys import activation, labeling_exigency
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Concept


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
        self.target_node = target_structures.get("target_node")
        self.parent_concept = target_structures.get("parent_concept")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import LabelBuilder

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
        space = bubble_chamber.input_spaces.get(key=activation)
        target = space.contents.where(is_chunk=True).get(key=labeling_exigency)
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
        potential_targets = bubble_chamber.input_nodes.where(is_slot=False).filter(
            lambda x: isinstance(x, parent_concept.instance_type)
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
    def targets_dict(self):
        return {
            "target_node": self.target_node,
            "parent_concept": self.parent_concept,
        }

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            try:
                conceptual_space = self.bubble_chamber.conceptual_spaces.filter(
                    lambda x: x.is_basic_level
                    and isinstance(self.target_node, x.instance_type)
                    and self.target_node.has_location_in_space(x)
                ).get()
                location = self.target_node.location_in_space(conceptual_space)
            except MissingStructureError:
                return False
            try:
                self.parent_concept = (
                    conceptual_space.contents.where(
                        is_concept=True, structure_type=Label, is_slot=False
                    )
                    .near(location)
                    .get()
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found parent concept: {self.parent_concept}"
                )
            except MissingStructureError:
                try:
                    self.parent_concept = (
                        conceptual_space.contents.where(
                            is_concept=True, structure_type=Label
                        )
                        .where_not(classifier=None)
                        .get()
                    )
                    self.bubble_chamber.loggers["activity"].log(
                        self, f"Found parent concept: {self.parent_concept}"
                    )
                except MissingStructureError:
                    return False
        if self.parent_concept is None:
            return False
        return True

    def _calculate_confidence(self):
        try:
            self.confidence = (
                self.parent_concept.classifier.classify(
                    concept=self.parent_concept, start=self.target_node
                )
                * self.target_node.quality
            )
        except NoLocationError:
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
            projected_location = Location(new_location_coordinates, source_space)
            self.target_node.locations.append(projected_location)
            self.confidence = self.parent_concept.classifier.classify(
                concept=self.parent_concept, start=self.target_node
            )
            self.target_node.locations.remove(projected_location)

    def _fizzle(self):
        pass
