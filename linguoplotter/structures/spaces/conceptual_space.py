from __future__ import annotations

import math
from typing import Callable, Dict, List

from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Space
from linguoplotter.structures.nodes import Concept


class ConceptualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureSet,
        breadth: int,
        no_of_dimensions: int,
        dimensions: List[ConceptualSpace],
        sub_spaces: List[ConceptualSpace],
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        possible_instances: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
    ):
        Space.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            quality=1.0,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.breadth = breadth
        self.possible_instances = possible_instances
        self.no_of_dimensions = no_of_dimensions
        self._dimensions = dimensions
        self.sub_spaces = sub_spaces
        self.is_basic_level = is_basic_level
        self.is_symbolic = is_symbolic
        self.super_space_to_coordinate_function_map = (
            (super_space_to_coordinate_function_map)
            if super_space_to_coordinate_function_map is not None
            else {}
        )
        self.is_conceptual_space = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "activation": self.activation,
        }

    @property
    def is_slot(self) -> bool:
        return self.parent_concept.is_slot

    @property
    def instance_type(self):
        return self.parent_concept.instance_type

    @property
    def structure_type(self):
        return self.parent_concept.structure_type

    @property
    def dimensions(self) -> List[Space]:
        if self.no_of_dimensions < 1:
            return []
        if self.no_of_dimensions == 1:
            return [self]
        return self._dimensions

    def nearby(self, space: Structure = None):
        return StructureSet.union(
            self.correspondees,
            *[correspondee.correspondees for correspondee in self.correspondees],
        )

    def add(self, structure: Structure):
        location_in_this_space = structure.location_in_space(self)
        if structure not in self.contents:
            self.contents.add(structure)
            for sub_space in self.sub_spaces:
                if structure.parent_space is None or (
                    structure.parent_space.is_conceptual_space
                    and structure.parent_space != self
                    and structure.parent_space != sub_space
                ):
                    continue
                if not structure.has_location_in_space(sub_space):
                    location_in_sub_space = (
                        sub_space.location_from_super_space_location(
                            location_in_this_space
                        )
                    )
                    structure.locations.append(location_in_sub_space)
                sub_space.add(structure)

    def subsumes(self, other) -> bool:
        if isinstance(other, ConceptualSpace):
            if self == other:
                return True
            return all(
                [
                    self.parent_concept.is_slot
                    or self.parent_concept == other.parent_concept,
                    math.isnan(self.no_of_dimensions)
                    or self.no_of_dimensions == other.no_of_dimensions,
                    self.is_symbolic == other.is_symbolic,
                    other in self.possible_instances
                    or (
                        all(
                            [
                                other_possible_instance in self.possible_instances
                                for other_possible_instance in self.possible_instances
                            ]
                        )
                        if other.possible_instances.not_empty
                        else False
                    ),
                ]
            )
        for space in other:
            if self.subsumes(space):
                return True
        return False

    def unifies_with(self, other) -> bool:
        return self.subsumes(other) or other.subsumes(self)

    def location_from_super_space_location(self, location: Location) -> Location:
        try:
            if location.coordinates[0][0] is None:
                coordinates = [[None for _ in range(self.no_of_dimensions)]]
            if math.isnan(location.coordinates[0][0]):
                coordinates = [[math.nan for _ in range(self.no_of_dimensions)]]
            else:
                coordinates_function = self.super_space_to_coordinate_function_map[
                    location.space.name
                ]
                coordinates = coordinates_function(location)
            return Location(coordinates, self)
        except NotImplementedError:
            if location.start_coordinates[0][0] is None:
                start_coordinates = [[None for _ in range(self.no_of_dimensions)]]
            if math.isnan(location.start_coordinates[0][0]):
                start_coordinates = [[math.nan for _ in range(self.no_of_dimensions)]]
            else:
                coordinates_function = self.super_space_to_coordinate_function_map[
                    location.space.name
                ]
                start_coordinates = coordinates_function(
                    Location(location.start_coordinates, location.space)
                )
            if location.end_coordinates[0][0] is None:
                end_coordinates = [[None for _ in range(self.no_of_dimensions)]]
            if math.isnan(location.end_coordinates[0][0]):
                end_coordinates = [[math.nan for _ in range(self.no_of_dimensions)]]
            else:
                coordinates_function = self.super_space_to_coordinate_function_map[
                    location.space.name
                ]
                end_coordinates = coordinates_function(
                    Location(location.end_coordinates, location.space)
                )
            return TwoPointLocation(start_coordinates, end_coordinates, self)
