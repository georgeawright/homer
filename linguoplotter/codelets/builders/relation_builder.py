from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.structure_collections import StructureDict
from linguoplotter.tools import centroid_difference


class RelationBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import RelationEvaluator

        return RelationEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        equivalent_relations = self.targets["start"].relations.where(
            end=self.targets["end"],
            parent_concept=self.targets["concept"],
            conceptual_space=self.targets["space"],
        )
        if equivalent_relations.not_empty:
            self.child_structures.add(equivalent_relations.get())
        return True

    def _process_structure(self):
        if self.child_structures.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Equivalent relation already exists"
            )
            return
        start_coordinates = (
            self.targets["start"].location_in_space(self.targets["space"]).coordinates
        )
        end_coordinates = (
            self.targets["end"].location_in_space(self.targets["space"]).coordinates
        )
        location_coordinates = centroid_difference(start_coordinates, end_coordinates)
        locations = [
            Location([[location_coordinates]], self.targets["concept"].parent_space),
            TwoPointLocation(start_coordinates, end_coordinates, self.targets["space"]),
        ]
        if self.targets["start"].parent_space == self.targets["end"].parent_space:
            locations.append(
                Location([], self.targets["start"].parent_space),
            )
            parent_space = self.targets["start"].parent_space
        else:
            parent_space = None
        relation = self.bubble_chamber.new_relation(
            parent_id=self.codelet_id,
            start=self.targets["start"],
            end=self.targets["end"],
            locations=locations,
            parent_concept=self.targets["concept"],
            parent_space=parent_space,
            conceptual_space=self.targets["space"],
            quality=0,
            is_interspatial_relation=parent_space is None,
        )
        self._structure_concept.instances.add(relation)
        self.child_structures.add(relation)
        if self.targets["concept"].is_reversible:
            mirror_relation = self.bubble_chamber.new_relation(
                parent_id=self.codelet_id,
                start=self.targets["end"],
                end=self.targets["start"],
                locations=locations,
                parent_concept=self.targets["concept"].reverse,
                parent_space=parent_space,
                conceptual_space=self.targets["space"],
                quality=0,
                is_interspatial_relation=parent_space is None,
            )
            self._structure_concept.instances.add(mirror_relation)
            self.child_structures.add(mirror_relation)
        self._structure_concept.recalculate_exigency()

    def _fizzle(self):
        pass
