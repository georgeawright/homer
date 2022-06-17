from __future__ import annotations

import math
from typing import Callable, Dict, List

from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Space
from linguoplotter.structures.nodes import Concept


class ConceptualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[ConceptualSpace],
        sub_spaces: List[ConceptualSpace],
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        possible_instances: StructureCollection,
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
        )
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
        return {}

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
        return StructureCollection.union(
            self.correspondees,
            *[correspondee.correspondees for correspondee in self.correspondees],
        )

    def add(self, structure: Structure):
        location_in_this_space = structure.location_in_space(self)
        if structure not in self.contents:
            self.contents.add(structure)
            for sub_space in self.sub_spaces:
                if not structure.has_location_in_space(sub_space):
                    location_in_sub_space = (
                        sub_space.location_from_super_space_location(
                            location_in_this_space
                        )
                    )
                    structure.locations.append(location_in_sub_space)
                sub_space.add(structure)

    def subsumes(self, other) -> bool:
        return all(
            [
                self.parent_concept.is_slot
                or self.parent_concept == other.parent_concept,
                math.isnan(self.no_of_dimensions)
                or self.no_of_dimensions == other.no_of_dimensions,
                self.is_symbolic == other.is_symbolic,
                other in self.possible_instances,
            ]
        )

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

    def make_projection(
        self,
        bubble_chamber: "BubbleChamber",
        target_space: ConceptualSpace,
        parent_id: str = "",
    ) -> ConceptualSpace:
        sub_space_copies = {
            sub_space: sub_space.copy(
                bubble_chamber=bubble_chamber,
                target_space=target_sub_space,
                parent_id=parent_id,
            )
            for sub_space, target_sub_space in zip(
                self.sub_spaces, target_space.sub_spaces
            )
        }
        new_space = bubble_chamber.new_conceptual_space(
            parent_id=parent_id,
            name=self.name + f"({target_space.name})",
            source_space=self,
            target_space=target_space,
            parent_concept=self.parent_concept,
            no_of_dimensions=self.no_of_dimensions,
            dimensions=[sub_space_copies[dimension] for dimension in self._dimensions],
            sub_spaces=[sub_space_copies[sub_space] for sub_space in self.sub_spaces],
            is_basic_level=self.is_basic_level,
            is_symbolic=self.is_symbolic,
            super_space_to_coordinate_function_map=self.super_space_to_coordinate_function_map,
        )
        source_concepts = [concept for concept in self.contents.where(is_concept=True)]
        source_concepts.sort(key=lambda x: x.location_in_space(self).coordinates[0][0])
        source_min_concept = source_concepts[0]
        source_max_concept = source_concepts[-1]
        target_min_concept = source_min_concept.correspondees.filter(
            lambda x: x.has_correspondence_to_space(self)
        ).get()
        target_max_concept = source_max_concept.correspondees.filter(
            lambda x: x.has_correspondence_to_space(self)
        ).get()
        source_min = source_min_concept.location_in_space(self).coordinates[0][0]
        source_max = source_max_concept.location_in_space(self).coordinates[0][0]
        target_min = target_min_concept.location_in_space(target_space).coordinates[0][
            0
        ]
        target_max = target_max_concept.location_in_space(target_space).coordinates[0][
            0
        ]
        conversion_ratio = (source_max - source_min) / (target_max - target_min)
        projection_function = (
            lambda x: (x.coordinates[0][0] - target_min) * conversion_ratio
        )
        new_space.super_space_to_coordinate_function_map[
            target_space
        ] = projection_function
        for concept in self.contents.where(is_concept=True):
            location_in_new_space = Location(
                concept.location_in_space(self).coordinates,
                new_space,
            )
            concept.locations.append(location_in_new_space)
            new_space.add(concept)
        return new_space
