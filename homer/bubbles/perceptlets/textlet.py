from __future__ import annotations
from typing import List

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles import Concept, Perceptlet
from homer.template import Template
from homer.perceptlet_collection import PerceptletCollection
from homer.perceptlet_collections import NeighbourCollection

from .word import Word


class Textlet(Perceptlet):
    """A fragment of text."""

    def __init__(
        self,
        value: str,
        parent_template: Template,
        parent_concept: Concept,
        constituents: List[Word],
        constituent_relations: PerceptletCollection,
        activation: PerceptletActivationPattern,
        parent_id: str,
    ):
        location = None
        neighbours = NeighbourCollection()
        Perceptlet.__init__(self, value, location, activation, neighbours, parent_id)
        self.parent_template = parent_template
        self.parent_concept = parent_concept
        self.constituents = constituents
        self.constituent_relations = constituent_relations

    def __str__(self) -> str:
        return " ".join([word.value for word in self.constituents])

    @property
    def size(self) -> int:
        return sum(constituent.size for constituent in self.constituents)
