from typing import Set

from homer.concept import Concept
from homer.concepts.correspondence_type import CorrespondenceType
from homer.concepts.perceptlet_type import PerceptletType
from homer.logger import Logger


class ConceptSpace:
    def __init__(
        self,
        perceptlet_types: Set[PerceptletType],
        correspondence_types: Set[CorrespondenceType],
        conceptual_spaces: Set[Concept],
        workspace_concepts: Set[Concept],
        logger: Logger,
    ):
        self.perceptlet_types = perceptlet_types
        self.perceptlet_types_dictionary = {
            perceptlet_type.name: perceptlet_type
            for perceptlet_type in perceptlet_types
        }
        self.correspondence_types = correspondence_types
        self.conceptual_spaces = conceptual_spaces
        self.workspace_concepts = workspace_concepts
        self.concepts = set.union(
            self.perceptlet_types,
            self.correspondence_types,
            self.conceptual_spaces,
            self.workspace_concepts,
        )
        self.spawning_concepts = set.union(perceptlet_types, workspace_concepts)
        self.logger = logger

    def get_perceptlet_type_by_name(self, name: str) -> PerceptletType:
        return self.perceptlet_types_dictionary[name]

    def update_activations(self):
        self.spread_activations()
        for concept in self.concepts:
            concept.update_activation()
            self.logger.log(concept)

    def spread_activations(self):
        for concept in self.concepts:
            concept.spread_activation()
