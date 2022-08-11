from __future__ import annotations
import math
from typing import List

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
        stable_activation: FloatBetweenOneAndZero = None,
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
            stable_activation=stable_activation,
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
        if not self.is_fully_active():
            return
        if self.parent_space is None or self.parent_space.is_conceptual_space:
            for link in self.links_out.where(is_label=False):
                if link.is_excitatory:
                    link.end.boost_activation(
                        link.parent_concept.activation
                        if link.parent_concept is not None
                        else None
                    )
                else:
                    link.end.decay_activation(
                        link.parent_concept.activation
                        if link.parent_concept is not None
                        else None
                    )
            for link in self.links_in.where(is_bidirectional=True):
                if link.is_excitatory:
                    link.start.boost_activation(
                        link.parent_concept.activation
                        if link.parent_concept is not None
                        else None
                    )
                else:
                    link.start.decay_activation(
                        link.parent_concept.activation
                        if link.parent_concept is not None
                        else None
                    )
            if self.parent_space is not None:
                self.parent_space.parent_concept.activate()
        else:
            for champion in self.champion_labels:
                champion.boost_activation(self.quality)
            for champion in self.champion_relations:
                champion.boost_activation(self.quality)

    def __repr__(self) -> str:
        if self.parent_space is None:
            return f"<{self.structure_id}>"
        return f"<{self.structure_id} in {self.parent_space.structure_id} {self.locations}>"
