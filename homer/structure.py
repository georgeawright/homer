from __future__ import annotations
from abc import ABC
import statistics
from typing import List

from .errors import MissingStructureError, NoLocationError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .location import Location
from .structure_collection import StructureCollection


class Structure(ABC):

    MINIMUM_ACTIVATION_UPDATE = HyperParameters.MINIMUM_ACTIVATION_UPDATE
    ACTIVATION_UPDATE_COEFFICIENT = HyperParameters.ACTIVATION_UPDATE_COEFFICIENT
    DECAY_RATE = HyperParameters.DECAY_RATE

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        stable_activation: float = None,
    ):
        self.structure_id = structure_id
        self.parent_id = parent_id
        self._locations = locations
        self._quality = quality
        self.links_in = links_in
        self.links_out = links_out
        self.parent_spaces = parent_spaces
        # TODO: get rid of randomness
        # self._activation = FloatBetweenOneAndZero(
        #    random.random() if stable_activation is None else stable_activation
        # )
        self._activation = 0.0 if stable_activation is None else stable_activation
        self.stable = stable_activation is not None
        self._depth = 1
        self._activation_buffer = 0.0
        self._activation_update_coefficient = self.ACTIVATION_UPDATE_COEFFICIENT
        self._parent_space = None
        self._parent_concept = None

        self.unchunkedness = 1.0
        self.unlabeledness = 1.0
        self.unrelatedness = 1.0
        self.uncorrespondedness = 1.0
        self.unhappiness = 1.0

        self.chunking_exigency = 0.5
        self.labeling_exigency = 0.5
        self.relating_exigency = 0.5
        self.corresponding_exigency = 0.5
        self.exigency = 0.5

        self.is_link_or_node = False
        self.is_node = False
        self.is_concept = False
        self.is_chunk = False
        self.is_letter_chunk = False
        self.is_rule = False
        self.is_link = False
        self.is_correspondence = False
        self.is_label = False
        self.is_relation = False
        self.is_view = False
        self.is_space = False
        self.is_conceptual_space = False
        self.is_contextual_space = False
        self.is_frame = False
        self.is_template = False

    @classmethod
    def get_builder_class(cls):
        raise NotImplementedError

    @classmethod
    def get_evaluator_class(cls):
        raise NotImplementedError

    @classmethod
    def get_selector_class(cls):
        raise NotImplementedError

    @property
    def is_labellable(self) -> bool:
        return (self.is_chunk or self.is_label or self.is_relation) and not self.is_slot

    @property
    def parent_space(self) -> Structure:
        return self._parent_space

    @property
    def parent_concept(self) -> Structure:
        return self._parent_concept

    @property
    def location(self) -> Location:
        if len(self._locations) == 0:
            return None
        if len(self._locations) == 1:
            return self._locations[0]
        return self.location_in_space(self.parent_space)

    @property
    def locations(self) -> List[Location]:
        return self._locations

    @locations.setter
    def locations(self, locations: List[Location]):
        self._locations = locations

    @property
    def size(self) -> int:
        return 1

    @property
    def coordinates(self) -> list:
        return self.location_in_space(self.parent_space).coordinates

    @property
    def is_slot(self) -> bool:
        return False

    def recalculate_exigency(self):
        self.recalculate_unhappiness()
        self.recalculate_chunking_exigency()
        self.recalculate_labeling_exigency()
        self.recalculate_relating_exigency()
        self.recalculate_corresponding_exigency()
        self.exigency = statistics.fmean([self.activation, self.unhappiness])

    def recalculate_chunking_exigency(self):
        self.chunking_exigency = statistics.fmean([self.activation, self.unchunkedness])

    def recalculate_labeling_exigency(self):
        self.labeling_exigency = statistics.fmean([self.activation, self.unlabeledness])

    def recalculate_relating_exigency(self):
        self.relating_exigency = statistics.fmean([self.activation, self.unrelatedness])

    def recalculate_corresponding_exigency(self):
        self.corresponding_exigency = statistics.fmean(
            [self.activation, self.uncorrespondedness]
        )

    @property
    def quality(self) -> FloatBetweenOneAndZero:
        return self._quality

    @property
    def depth(self) -> FloatBetweenOneAndZero:
        return self._depth

    @quality.setter
    def quality(self, q: FloatBetweenOneAndZero):
        self._quality = q

    @property
    def activation(self) -> FloatBetweenOneAndZero:
        return self._activation

    @activation.setter
    def activation(self, a: FloatBetweenOneAndZero):
        self._activation = a

    def recalculate_unhappiness(self):
        self.recalculate_unlabeledness()
        self.recalculate_unrelatedness()
        self.recalculate_uncorrespondedness()
        return statistics.fmean(
            [self.unlabeledness, self.unrelatedness, self.uncorrespondedness]
        )

    def recalculate_unchunkedness(self):
        raise NotImplementedError

    def recalculate_unlabeledness(self):
        self.unlabeledness = 0.5 ** sum(link.activation for link in self.labels)

    def recalculate_unrelatedness(self):
        self.unrelatedness = 0.5 ** sum(link.activation for link in self.relations)

    def recalculate_uncorrespondedness(self) -> FloatBetweenOneAndZero:
        self.uncorrespondedness = 0.5 ** sum(
            link.activation for link in self.correspondences
        )

    @property
    def links(self) -> StructureCollection:
        return StructureCollection.union(self.links_in, self.links_out)

    @property
    def labels(self) -> StructureCollection:
        return self.links_out.where(is_label=True)

    @property
    def relations(self) -> StructureCollection:
        return StructureCollection.union(
            self.links_in.where(is_relation=True),
            self.links_out.where(is_relation=True),
        )

    @property
    def correspondences(self) -> StructureCollection:
        return StructureCollection.union(
            self.links_in.where(is_correspondence=True),
            self.links_out.where(is_correspondence=True),
        )

    @property
    def relatives(self) -> StructureCollection:
        if self.relations.is_empty():
            return self.relations.copy()
        return StructureCollection.union(
            *[relation.arguments for relation in self.relations]
        ).excluding(self)

    @property
    def correspondees(self) -> StructureCollection:
        if self.correspondences.is_empty():
            return self.correspondences.copy()
        return StructureCollection.union(
            *[correspondence.arguments for correspondence in self.correspondences]
        ).excluding(self)

    def nearby(self, space: Structure = None):
        raise NotImplementedError

    def similarity_with(self, other: Structure):
        return statistics.fmean(
            [
                location.space.proximity_between(self, other)
                if other.has_location_in_space(location.space)
                else 0.0
                for location in self.locations
                if location.space.is_conceptual_space
            ]
        )

    def is_near(self, other: Structure) -> bool:
        for other_location in other.locations:
            for self_location in self.locations:
                if self_location.is_near(other_location):
                    return True
        return False

    def has_location_in_space(self, space: Structure) -> bool:
        try:
            self.location_in_space(space)
            return True
        except NoLocationError:
            return False

    def location_in_space(
        self, space: Structure, start: Location = None, end: Location = None
    ) -> Location:
        locations = self.locations
        for location in locations:
            if location is not None and location.space == space:
                if (
                    start is not None
                    and location.start_coordinates != start.coordinates
                ):
                    continue
                if end is not None and location.end_coordinates != end.coordinates:
                    continue
                return location
        raise NoLocationError(f"{self} has no location in space {space}")

    def has_label(self, concept: Structure) -> FloatBetweenOneAndZero:
        for label in self.labels:
            if label.parent_concept == concept:
                return label.activation
        return 0.0

    def has_label_with_name(self, name: str) -> FloatBetweenOneAndZero:
        for label in self.labels:
            if label.parent_concept.name == name:
                return label.activation
        return 0.0

    def label_of_type(self, concept: Structure):
        for label in self.labels:
            if label.parent_concept == concept:
                return label
        raise MissingStructureError

    def labels_in_space(self, space: Structure) -> StructureCollection:
        return self.labels.filter(lambda x: x in space.contents)

    def has_relation(
        self,
        space: Structure,
        concept: Structure,
        first_argument: Structure,
        second_argument: Structure,
    ) -> FloatBetweenOneAndZero:
        for relation in self.relations:
            if (
                relation.parent_concept == concept
                and relation.start == first_argument
                and relation.end == second_argument
                and relation.parent_space == space
            ):
                return relation.activation
        return 0.0

    def has_relation_with_name(self, name: str) -> FloatBetweenOneAndZero:
        for relation in self.relations:
            if relation.parent_concept.name == name:
                return relation.activation
        return 0.0

    def relation_with_name(self, name: str) -> Structure:
        for relation in self.relations:
            if relation.parent_concept.name == name:
                return relation
        raise MissingStructureError

    def relations_in_space(self, space: Structure) -> StructureCollection:
        return self.relations.filter(lambda x: x in space.contents)

    def relations_in_space_with(
        self, space: Structure, other: Structure
    ) -> StructureCollection:
        return self.relations.filter(
            lambda x: x in space.contents and other in x.arguments
        )

    def relations_with(self, other: Structure) -> StructureCollection:
        return self.relations.filter(lambda x: other in x.arguments)

    def has_relation_with(
        self, other: Structure, parent_concept: Structure = None
    ) -> StructureCollection:
        relations = self.relations_with(other)
        if parent_concept is not None:
            relations = relations.where(parent_concept=parent_concept)
        return not relations.is_empty()

    def relation_in_space_of_type_with(
        self, space: Structure, concept: Structure, start: Structure, end: Structure
    ) -> Structure:
        return self.relations.where(
            parent_space=space, parent_concept=concept, start=start, end=end
        ).get()

    def has_correspondence(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for correspondence in self.correspondences:
            if (
                correspondence.parent_concept == concept
                and correspondence.conceptual_space == space
                and second_argument in (correspondence.start, correspondence.end)
            ):
                return True
        return False

    def has_correspondence_to_space(self, space: Structure) -> bool:
        return len(self.correspondences_to_space(space)) > 0

    def has_correspondence_in_view(self, view: Structure) -> bool:
        return len(self.correspondences.where(parent_view=view)) > 0

    def correspondences_with(self, other: Structure):
        return self.correspondences.filter(
            lambda x: (x.start == self and x.end == other)
            or (x.start == other and x.end == self)
        )

    def correspondences_to_space(self, space: Structure):
        return self.correspondences.filter(
            lambda x: (x.start == self and x.end.parent_space == space)
            or (x.end == self and x.start.parent_space == space)
        )

    def is_fully_active(self) -> bool:
        return self.activation == 1.0

    def boost_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer += (
            self._activation_update_coefficient * (1 / self.depth) * amount
        )

    def decay_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= (
            self._activation_update_coefficient * (1 / self.depth) * amount
        )

    def spread_activation(self):
        raise NotImplementedError

    def update_activation(self):
        if self._activation_buffer == 0.0:
            self.decay_activation(self.DECAY_RATE)
        self._activation = FloatBetweenOneAndZero(
            self._activation + self._activation_buffer
        )
        self._activation_buffer = 0.0
        self.recalculate_exigency()

    def copy(self, **kwargs: dict):
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.structure_id
