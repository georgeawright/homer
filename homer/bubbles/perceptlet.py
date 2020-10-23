from __future__ import annotations
import statistics
from typing import Any, List, Optional, Union

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubble import Bubble
from homer.hyper_parameters import HyperParameters
from homer.id import ID
from homer.perceptlet_collection import PerceptletCollection
from homer.perceptlet_collections import NeighbourCollection

from .concept import Concept


class Perceptlet(Bubble):

    ACTIVATION_WEIGHT = HyperParameters.EXIGENCY_ACTIVATION_WEIGHT
    UNHAPPINESS_WEIGHT = HyperParameters.EXIGENCY_UNHAPPINESS_WEIGHT

    def __init__(
        self,
        value: Any,
        location: Optional[List[Union[float], float[int]]],
        activation: PerceptletActivationPattern,
        neighbours: NeighbourCollection,
        parent_id: str,
    ):
        self.perceptlet_id = ID.new(self)
        Bubble.__init__(self, activation, self.perceptlet_id)
        self.value = value
        self.location = location
        self.neighbours = neighbours
        self.parent_id = parent_id
        self.quality = activation.as_scalar()
        self.unhappiness = PerceptletActivationPattern(activation=1.0)
        self.labels = PerceptletCollection()
        self.groups = PerceptletCollection()
        self.correspondences = PerceptletCollection()
        self.textlets = PerceptletCollection()
        self.connections = PerceptletCollection.union(
            self.labels, self.groups, self.correspondences, self.textlets
        )

    @property
    def size(self) -> int:
        return 1

    @property
    def exigency(self) -> float:
        """Returns a rating between 0 and 1."""
        return statistics.fmean(
            [
                self.ACTIVATION_WEIGHT * self.activation.as_scalar(),
                self.UNHAPPINESS_WEIGHT * self.unhappiness.as_scalar(),
            ]
        )

    def get_value(self, concept: Concept) -> Any:
        return {
            "location": lambda: self.location[1:],
            "time": lambda: self.location[0],
            "value": lambda: self.value,
            "size": lambda: self.size,
        }[concept.relevant_value]()

    def total_connection_activations(self) -> float:
        return sum(connection.activation.as_scalar() for connection in self.connections)

    def add_label(self, label: Perceptlet):
        self._add_connection("labels", label)

    def add_group(self, group: Perceptlet):
        self._add_connection("groups", group)

    def add_correspondence(self, correspondence: Perceptlet):
        self._add_connection("correspondences", correspondence)

    def add_textlet(self, textlet: Perceptlet):
        self._add_connection("textlets", textlet)

    def _add_connection(self, collection: str, perceptlet: Perceptlet):
        getattr(self, collection).add(perceptlet)
        self.connections.add(perceptlet)
        self.unhappiness.decay_by_amount(perceptlet.activation.as_scalar())

    def has_label(self, concept: Concept) -> bool:
        return True in (
            True for label in self.labels if label.parent_concept == concept
        )

    def labels_in_space(self, space: Concept) -> PerceptletCollection:
        return PerceptletCollection(
            {label for label in self.labels if label.parent_concept.space == space}
        )

    def has_label_in_space(self, space: Concept) -> bool:
        return len(self.labels_in_space(space)) > 0

    def makes_group_with(self, other_members: PerceptletCollection) -> bool:
        for group in self.groups:
            if group.members == PerceptletCollection.union(
                other_members,
                PerceptletCollection({self}),
            ):
                return True
        return False

    def has_correspondence(self, second_perceptlet: Perceptlet, space: Concept) -> bool:
        for correspondence in self.correspondences:
            if (
                correspondence.is_between(self, second_perceptlet)
                and correspondence.parent_concept == space
            ):
                return True
        return False

    def has_textlet(self, template, label):
        for textlet in self.textlets:
            if (
                textlet.parent_concept == label.parent_concept
                and textlet.parent_template == template
            ):
                return True
        return False

    def boost_activation(self, amount: float):
        self.activation.boost_by_amount(amount)
        for connection in self.connections:
            connection.boost_activation(amount)

    def decay_activation(self, amount: float):
        self.activation.decay_by_amount(amount)
        for connection in self.connections:
            connection.decay_activation(amount)
