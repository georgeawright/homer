import statistics
from typing import Callable

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space


class WorkingSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        contents: StructureCollection,
        quality: FloatBetweenOneAndZero,
        parent_concept: Concept,
        is_sub_space: bool = False,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        coordinates_from_super_space_location: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            contents,
            quality,
            parent_concept,
            is_sub_space=is_sub_space,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )

    @property
    def quality(self):
        active_contents = [
            structure for structure in self.contents if structure.activation > 0
        ]
        if len(active_contents) == 0 and len(self.child_spaces) == 0:
            return 0.0
        if len(active_contents) > 0:
            contents_quality = [
                statistics.fmean(
                    [item.quality * item.activation for item in active_contents]
                )
            ]
        else:
            contents_quality = []
        return statistics.fmean(
            [space.quality for space in self.child_spaces] + contents_quality
        )

    def update_activation(self):
        self._activation = (
            statistics.median([item.activation for item in self.contents])
            if len(self.contents) != 0
            else 0.0
        )
