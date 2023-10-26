from __future__ import annotations
import math
import statistics
from typing import Callable, List

from linguoplotter.classifier import Classifier
from linguoplotter.errors import NoLocationError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.location import Location
from linguoplotter.structure_collections import StructureSet
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
        child_spaces: StructureSet,
        distance_function: Callable,
        chunking_distance_function: Callable,
        possible_instances: StructureSet,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        subsumes: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DEFAULT_DISTANCE_TO_PROXIMITY_WEIGHT,
        is_slot: bool = False,
        reverse: Concept = None,
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
            instances=instances,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.name = name
        self.classifier = classifier
        self.instance_type = instance_type
        self.structure_type = structure_type
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.chunking_distance_function = chunking_distance_function
        self.possible_instances = possible_instances
        self._subsumes = subsumes
        self._depth = depth
        self.distance_to_proximity_weight = distance_to_proximity_weight
        self.is_concept = True
        self._is_slot = is_slot
        self._non_slot_value = None
        self.reverse = reverse

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
            "links_out": [link.structure_id for link in self.links_out],
            "links_in": [link.structure_id for link in self.links_in],
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

    @property
    def is_reversible(self) -> bool:
        return self.reverse is not None

    def subsumes(self, other) -> bool:
        return (
            any(
                [
                    self == other,
                    other in self._subsumes,
                    other in self.possible_instances,
                    self.is_slot and self.parent_space.subsumes(other.parent_space),
                ]
            )
            or (
                other.is_slot
                and other.is_filled_in
                and self.subsumes(other.non_slot_value)
            )
            or (
                other.is_slot
                and not other.is_filled_in
                and any(
                    [self.subsumes(instance) for instance in other.possible_instances]
                )
            )
        )

    def recalculate_unhappiness(self):
        self.unhappiness = 0.5 ** sum(
            instance.activation for instance in self.instances
        )

    def distance_from(self, other: Node, return_nan: bool = False):
        try:
            return self.distance_function(
                self.location_in_space(self.parent_space).coordinates,
                other.location_in_space(self.parent_space).coordinates,
                return_nan=return_nan,
            )
        except NotImplementedError:
            return statistics.mean(
                [
                    self.distance_function(
                        self.location_in_space(self.parent_space).start_coordinates,
                        other.location_in_space(self.parent_space).start_coordinates,
                        return_nan=return_nan,
                    ),
                    self.distance_function(
                        self.location_in_space(self.parent_space).end_coordinates,
                        other.location_in_space(self.parent_space).end_coordinates,
                        return_nan=return_nan,
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
                "", "", [new_location], None, None, None, None, None, None, None, None
            )
            if new_location is None:
                raise NoLocationError
            return self.distance_from(mock_node, return_nan)

    def proximity_to(self, other: Node, return_nan: bool = False):
        try:
            distance = self.distance_from(other, return_nan)
            if math.isnan(distance) and return_nan:
                return math.nan
            return self._distance_to_proximity(distance)
        except NoLocationError:
            return 0.0

    def distance_between(
        self,
        a: Node,
        b: Node,
        space: "Space" = None,
        distance_function: callable = None,
        return_nan: bool = False,
    ):
        space = self.parent_basic_space if space is None else space
        distance_function = (
            self.distance_function if distance_function is None else distance_function
        )
        try:
            return distance_function(
                a.location_in_space(space).coordinates,
                b.location_in_space(space).coordinates,
                return_nan,
            )
        except NotImplementedError:
            try:
                return statistics.mean(
                    [
                        distance_function(
                            a.location_in_space(space).start_coordinates,
                            b.location_in_space(space).start_coordinates,
                            return_nan,
                        ),
                        distance_function(
                            a.location_in_space(space).end_coordinates,
                            b.location_in_space(space).end_coordinates,
                            return_nan,
                        ),
                    ]
                )
            except AttributeError:
                return 0.0

    def proximity_between(
        self, a: Node, b: Node, space: "Space" = None, return_nan: bool = False
    ):
        distance = self.distance_between(a, b, space=space, return_nan=return_nan)
        if math.isnan(distance) and return_nan:
            return math.nan
        return self._distance_to_proximity(distance)

    def adjacency_of(
        self, a: Node, b: Node, space: "Space" = None, return_nan: bool = False
    ):
        distance = self.distance_between(
            a,
            b,
            space=space,
            distance_function=self.chunking_distance_function,
            return_nan=return_nan,
        )
        if math.isnan(distance) and return_nan:
            return math.nan
        return self._distance_to_proximity(distance)

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
            possible_instances=self.possible_instances.copy(),
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
