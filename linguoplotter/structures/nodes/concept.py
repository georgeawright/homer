from __future__ import annotations
import statistics
from typing import Callable, List

from linguoplotter.classifier import Classifier
from linguoplotter.errors import NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Node, Space


class Concept(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        locations: List[Location],
        classifier: Classifier,
        instance_type: type,
        structure_type: type,
        parent_space: Space,
        child_spaces: StructureCollection,
        distance_function: Callable,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        instances: StructureCollection,
        champion_labels: StructureCollection,
        champion_relations: StructureCollection,
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT,
        is_slot: bool = False,
    ):
        quality = None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.name = name
        self.classifier = classifier
        self.instance_type = instance_type
        self.structure_type = structure_type
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.instances = instances
        self._depth = depth
        self.distance_to_proximity_weight = distance_to_proximity_weight
        self.is_concept = True
        self._is_slot = is_slot
        self._non_slot_value = None

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id
            if self.parent_space is not None
            else None,
            "instance_type": self.instance_type.__name__
            if self.instance_type is not None
            else None,
            "structure_type": self.structure_type.__name__
            if self.structure_type is not None
            else None,
            "depth": self.depth,
            "quality": self.quality,
            "activation": self.activation,
        }

    @property
    def prototype(self) -> list:
        return self.location.coordinates

    @property
    def is_slot(self) -> bool:
        return self._is_slot

    @property
    def is_filled_in(self) -> bool:
        return not self.non_slot_value is None

    @property
    def non_slot_value(self) -> Concept:
        if self._non_slot_value is None:
            return None
        if not self._non_slot_value.is_slot:
            return self._non_slot_value
        return self._non_slot_value.non_slot_value

    @property
    def number_of_components(self):
        return 1

    @property
    def parent_basic_space(self) -> "ConceptualSpace":
        return self.parent_spaces.where(is_basic_level=True).get()

    def recalculate_unhappiness(self):
        self.unhappiness = 0.5 ** sum(
            instance.activation for instance in self.instances
        )

    def compatibility_with(self, other: Concept) -> FloatBetweenOneAndZero:
        if (
            self == other
            or self.parent_space.parent_concept == other
            or other.parent_space.parent_concept == self
        ):
            return 1.0
        if self.parent_space == other.parent_space:
            return self.proximity_to(other)
        return 0.0

    def friends(self, space: Space = None) -> StructureCollection:
        space = self.parent_space if space is None else space
        friend_concepts = self.relatives.filter(
            lambda x: not x.is_slot and x.is_concept and x in space.contents
        )
        if friend_concepts.is_empty():
            friend_concepts.add(self)
        return friend_concepts

    def distance_from(self, other: Node):
        try:
            return self.distance_function(
                self.location_in_space(self.parent_space).coordinates,
                other.location_in_space(self.parent_space).coordinates,
            )
        except NotImplementedError:
            return statistics.mean(
                [
                    self.distance_function(
                        self.location_in_space(self.parent_space).start_coordinates,
                        other.location_in_space(self.parent_space).start_coordinates,
                    ),
                    self.distance_function(
                        self.location_in_space(self.parent_space).end_coordinates,
                        other.location_in_space(self.parent_space).end_coordinates,
                    ),
                ]
            )
        except NoLocationError:
            new_location = None
            for location in other.locations:
                if location.space.is_conceptual_space:
                    try:
                        new_location = (
                            self.parent_space.location_from_super_space_location(
                                location
                            )
                        )
                        break
                    except KeyError:
                        pass
            mock_node = Node(
                "", "", [new_location], None, None, None, None, None, None, None
            )
            if new_location is None:
                raise NoLocationError
            return self.distance_from(mock_node)

    def distance_from_start(self, other: Node, end: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, end=end).start_coordinates,
            other.location_in_space(self.parent_space).coordinates,
        )

    def distance_from_end(self, other: Node, start: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, start=start).end_coordinates,
            other.location_in_space(self.parent_space).coordinates,
        )

    def proximity_to(self, other: Node):
        try:
            return self._distance_to_proximity(self.distance_from(other))
        except NoLocationError:
            return 0.0

    def proximity_to_start(self, other: Node, end: Location = None):
        return self._distance_to_proximity(self.distance_from_start(other, end=end))

    def proximity_to_end(self, other: Node, start: Location = None):
        return self._distance_to_proximity(self.distance_from_end(other, start=start))

    def distance_between(self, a: Node, b: Node, space: "Space" = None):
        space = self.parent_space if space is None else space
        try:
            return self.distance_function(
                a.location_in_space(space).coordinates,
                b.location_in_space(space).coordinates,
            )
        except NotImplementedError:
            try:
                return statistics.mean(
                    [
                        self.distance_function(
                            a.location_in_space(space).start_coordinates,
                            b.location_in_space(space).start_coordinates,
                        ),
                        self.distance_function(
                            a.location_in_space(space).end_coordinates,
                            b.location_in_space(space).end_coordinates,
                        ),
                    ]
                )
            except AttributeError:
                return 0.0

    def proximity_between(self, a: Node, b: Node, space: "Space" = None):
        return self._distance_to_proximity(self.distance_between(a, b, space=space))

    def _distance_to_proximity(self, value: float) -> float:
        # TODO: consider using a distance_to_proximity function instead of weight
        if value == 0:
            return 1.0
        # return min(self.distance_to_proximity_function(value), 1.0)
        inverse = 1.0 / value
        proximity = inverse * self.distance_to_proximity_weight
        return min(proximity, 1.0)

    def copy(self, bubble_chamber: "BubbleChamber", parent_id: str = "") -> Concept:
        return bubble_chamber.new_concept(
            parent_id=parent_id,
            name=self.name,
            locations=[location.copy() for location in self.locations],
            classifier=self.classifier,
            instance_type=self.instance_type,
            structure_type=self.structure_type,
            parent_space=self.parent_space,
            distance_function=self.distance_function,
            depth=self.depth,
            distance_to_proximity_weight=self.distance_to_proximity_weight,
            is_slot=self.is_slot,
        )

    def __repr__(self) -> str:
        parent_space_structure_id = (
            self.parent_space.structure_id if self.parent_space is not None else "-"
        )
        return (
            f"<{self.structure_id} {self.name} in "
            + f"{parent_space_structure_id} {self.locations}>"
        )
