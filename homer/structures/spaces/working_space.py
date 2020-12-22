from __future__ import annotations

import statistics
from typing import Callable, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space


class WorkingSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        locations: List[Location],
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[WorkingSpace],
        sub_spaces: List[WorkingSpace],
        is_basic_level: bool = False,
        coordinates_from_super_space_location: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = 0
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            locations,
            contents,
            no_of_dimensions,
            dimensions,
            sub_spaces,
            quality,
            is_basic_level=is_basic_level,
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )

    @property
    def quality(self):
        active_contents = {
            structure
            for space in [self] + self.sub_spaces
            for structure in space.contents
            if structure.activation > 0
        }
        if len(active_contents) == 0:
            return 0.0
        return statistics.fmean([structure.quality for structure in active_contents])

    def update_activation(self):
        self._activation = (
            statistics.median([item.activation for item in self.contents])
            if len(self.contents) != 0
            else 0.0
        )
