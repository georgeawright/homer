from __future__ import annotations
import math
from typing import List

from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection

from .space import Space


class Node(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        champion_labels: StructureCollection,
        champion_relations: StructureCollection,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self._parent_space = parent_space
        self.is_node = True

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    @parent_space.setter
    def parent_space(self, space: Space):
        self._parent_space = space

    @property
    def is_slot(self):
        return any(
            [
                math.nan in coordinates
                for location in self.locations
                for coordinates in location.coordinates
            ]
        )

    def recalculate_uncorrespondedness(self):
        self.uncorrespondedness = 0.5 * 0.5 ** sum(
            link.activation for link in self.correspondences
        )

    def nearby(self, space: Space = None) -> StructureCollection:
        raise NotImplementedError

    def get_potential_relative(
        self, space: Space = None, concept: "Concept" = None
    ) -> Node:
        raise NotImplementedError

    def spread_activation(self):
        pass

    def update_activation(self):
        if self.parent_space is None or self.parent_space.is_conceptual_space:
            relatives_total = 0
            for relation in self.relations:
                try:
                    if not relation.arguments.excluding(self).get().is_fully_active():
                        continue
                except MissingStructureError:
                    pass
                relatives_total += relation.activation
            if relatives_total >= 1:
                self._activation_buffer += (
                    self.ACTIVATION_UPDATE_COEFFICIENT * relatives_total
                )
            if self._activation_buffer == 0.0:
                self.decay_activation(self.DECAY_RATE)
            self._activation = FloatBetweenOneAndZero(
                self._activation + self._activation_buffer
            )
            self._activation_buffer = 0.0
            self.recalculate_exigency()
            if (
                self.is_fully_active()
                and self.parent_space is not None
                and self.parent_space.is_conceptual_space
            ):
                self.parent_space.parent_concept.activate()

    def __repr__(self) -> str:
        if self.parent_space is None:
            return f"<{self.structure_id}>"
        return f"<{self.structure_id} in {self.parent_space.structure_id} {self.locations}>"
