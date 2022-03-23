from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure import Structure
from homer.tools import average_vector, centroid_difference


class RelationBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_space = target_structures.get("target_space")
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_structure_two = target_structures.get("target_structure_two")
        self.parent_concept = target_structures.get("parent_concept")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import RelationEvaluator

        return RelationEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: Structure,
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
        return self.bubble_chamber.concepts["relation"]

    @property
    def targets_dict(self):
        return {
            "target_space": self.target_space,
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
            "parent_concept": self.parent_concept,
        }

    def _passes_preliminary_checks(self):
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _process_structure(self):
        start_coordinates = self.target_structure_one.location_in_space(
            self.target_space
        ).coordinates
        end_coordinates = self.target_structure_two.location_in_space(
            self.target_space
        ).coordinates
        location_coordinates = centroid_difference(start_coordinates, end_coordinates)
        locations = [
            Location([], self.target_structure_one.parent_space),
            Location([[location_coordinates]], self.parent_concept.parent_space),
            TwoPointLocation(start_coordinates, end_coordinates, self.target_space),
        ]
        relation = self.bubble_chamber.new_relation(
            parent_id=self.codelet_id,
            start=self.target_structure_one,
            end=self.target_structure_two,
            locations=locations,
            parent_concept=self.parent_concept,
            conceptual_space=self.target_space,
            quality=0,
        )
        if self.parent_concept.has_relation_with(self.bubble_chamber.concepts["more"]):
            self.bubble_chamber.loggers["activity"].log(
                self, "Getting a location in magnitude space"
            )
            proximity_to_prototype = self.parent_concept.proximity_to(relation)
            concept_location = self.parent_concept.location_in_space(
                self.parent_concept.parent_space
            )
            if location_coordinates > concept_location.coordinates[0][0]:
                magnitude_coordinates = [[1 - proximity_to_prototype]]
            else:
                magnitude_coordinates = [[proximity_to_prototype - 1]]
            relation.locations.append(
                Location(
                    magnitude_coordinates,
                    self.bubble_chamber.conceptual_spaces["magnitude"],
                )
            )
            self.bubble_chamber.conceptual_spaces["magnitude"].add(relation)
        if self.parent_concept.has_relation_with(self.bubble_chamber.concepts["less"]):
            self.bubble_chamber.loggers["activity"].log(
                self, "Getting a location in magnitude space"
            )
            proximity_to_prototype = self.parent_concept.proximity_to(relation)
            concept_location = self.parent_concept.location_in_space(
                self.parent_concept.parent_space
            )
            if location_coordinates > concept_location.coordinates[0][0]:
                magnitude_coordinates = [[proximity_to_prototype - 1]]
            else:
                magnitude_coordinates = [[1 - proximity_to_prototype]]
            relation.locations.append(
                Location(
                    magnitude_coordinates,
                    self.bubble_chamber.conceptual_spaces["magnitude"],
                )
            )
            self.bubble_chamber.conceptual_spaces["magnitude"].add(relation)
        self._structure_concept.instances.add(relation)
        self._structure_concept.recalculate_exigency()
        self.child_structures = self.bubble_chamber.new_structure_collection(relation)

    def _fizzle(self):
        pass
