from __future__ import annotations
from abc import ABC
import statistics

from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .location import Location
from .structure_collection import StructureCollection


class Structure(ABC):

    MINIMUM_ACTIVATION_UPDATE = HyperParameters.MINIMUM_ACTIVATION_UPDATE
    ACTIVATION_UPDATE_COEFFICIENT = HyperParameters.ACTIVATION_UPDATE_COEFFICIENT

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        location: Location,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        parent_chunks: StructureCollection = None,
    ):
        self.structure_id = structure_id
        self.parent_id = parent_id
        self.location = location
        self._quality = quality
        self.links_in = StructureCollection() if links_in is None else links_in
        self.links_out = StructureCollection() if links_out is None else links_out
        self.parent_chunks = (
            StructureCollection() if parent_chunks is None else parent_chunks
        )
        self._activation = FloatBetweenOneAndZero(0)
        self._activation_buffer = 0.0
        self._activation_update_coefficient = self.ACTIVATION_UPDATE_COEFFICIENT

    @property
    def coordinates(self) -> list:
        return self.location.coordinates

    @property
    def exigency(self) -> FloatBetweenOneAndZero:
        return self.activation * self.unhappiness

    @property
    def quality(self) -> FloatBetweenOneAndZero:
        return self._quality

    @quality.setter
    def quality(self, q: FloatBetweenOneAndZero):
        self._quality = q

    @property
    def activation(self) -> FloatBetweenOneAndZero:
        return self._activation

    @property
    def unhappiness(self) -> FloatBetweenOneAndZero:
        return statistics.fmean([self.unchunkedness, self.unlinkedness])

    @property
    def unchunkedness(self) -> FloatBetweenOneAndZero:
        return 0.5 ** len(self.parent_chunks)

    @property
    def unlinkedness(self) -> FloatBetweenOneAndZero:
        return 0.5 ** len(self.links)

    @property
    def links(self) -> StructureCollection:
        return StructureCollection.union(self.links_in, self.links_out)

    @property
    def correspondences(self) -> StructureCollection:
        from homer.structures.links import Correspondence

        return StructureCollection(
            set.union(
                {link for link in self.links_in if isinstance(link, Correspondence)},
                {link for link in self.links_out if isinstance(link, Correspondence)},
            )
        )

    @property
    def labels(self) -> StructureCollection:
        from homer.structures.links import Label

        return StructureCollection(
            {link for link in self.links_out if isinstance(link, Label)}
        )

    @property
    def relations(self) -> StructureCollection:
        from homer.structures.links import Relation

        return StructureCollection(
            set.union(
                {link for link in self.links_in if isinstance(link, Relation)},
                {link for link in self.links_out if isinstance(link, Relation)},
            )
        )

    @property
    def lexemes(self) -> StructureCollection:
        from homer.structures import Lexeme

        return StructureCollection(
            {link.end for link in self.links_out if isinstance(link.end, Lexeme)}
        )

    def nearby(self, space: Structure = None):
        raise NotImplementedError

    def is_near(self, location: Location):
        return self.location.is_near(location)

    def has_link(self, structure: Structure) -> bool:
        from homer.structures.links import Correspondence, Label, Relation

        if isinstance(structure, Label):
            return self.has_label(structure.parent_concept)
        other_arg = structure.end if self == structure.start else structure.start
        if isinstance(structure, Correspondence):
            return self.has_correspondence(
                structure.conceptual_space, structure.parent_concept, other_arg
            )
        if isinstance(structure, Relation):
            return self.has_relation(
                structure.parent_space, structure.parent_concept, other_arg
            )
        return False

    def has_label(self, concept: Structure) -> bool:
        for label in self.labels:
            if label.parent_concept == concept:
                return True
        return False

    def labels_in_space(self, space: Structure) -> StructureCollection:
        return StructureCollection(
            {label for label in self.labels if label in space.contents}
        )

    def has_relation(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for link in self.links_out:
            if (
                link.parent_concept == concept
                and link.end == second_argument
                and link.parent_space == space
            ):
                return True
        return False

    def relations_in_space_with(
        self, space: Structure, other: Structure
    ) -> StructureCollection:
        return StructureCollection(
            {
                relation
                for relation in self.relations
                if relation in space.contents
                and other in {relation.start, relation.end}
            }
        )

    def relations_with(self, other: Structure) -> StructureCollection:
        return StructureCollection(
            {
                relation
                for relation in self.relations
                if other in {relation.start, relation.end}
            }
        )

    def has_correspondence(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for link in self.links_out:
            if (
                link.parent_concept == concept
                and link.end == second_argument
                and link.parent_space == space
            ):
                return True
        return False

    def correspondences_with(self, other: Structure):
        return StructureCollection(
            {
                correspondence
                for correspondence in self.correspondences
                if correspondence.start == self
                and correspondence.end == other
                or correspondence.start == other
                and correspondence.end == self
            }
        )

    def correspondences_to_space(self, space: Structure):
        return StructureCollection(
            {
                correspondence
                for correspondence in self.correspondences
                if correspondence.start == self
                and correspondence.end_space == space
                or correspondence.end == self
                and correspondence.start_space == space
            }
        )

    def is_fully_active(self) -> bool:
        return self.activation == 1.0

    def boost_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer += self._activation_update_coefficient * amount

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount

    def spread_activation(self):
        if not self.is_fully_active():
            return
        for link in self.links_out:
            try:
                link.end.boost_activation(link.activation)
            except AttributeError:  # labels have no end
                pass

    def update_activation(self):
        if self._activation_buffer == 0.0:
            self.decay_activation()
        self._activation = FloatBetweenOneAndZero(
            self._activation + self._activation_buffer
        )
        self._activation_buffer = 0.0
