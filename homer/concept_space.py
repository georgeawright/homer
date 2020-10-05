import random
from typing import Set

from .bubbles.concept import Concept
from .bubbles.concepts.correspondence_type import CorrespondenceType
from .bubbles.concepts.emotion import Emotion
from .bubbles.concepts.perceptlet_type import PerceptletType
from .logger import Logger


class ConceptSpace:
    def __init__(
        self,
        emotions: Set[Emotion],
        perceptlet_types: Set[PerceptletType],
        correspondence_types: Set[CorrespondenceType],
        conceptual_spaces: Set[Concept],
        workspace_concepts: Set[Concept],
        logger: Logger,
    ):
        self.emotions = emotions
        self.perceptlet_types = perceptlet_types
        self.perceptlet_types_dictionary = {
            perceptlet_type.name: perceptlet_type
            for perceptlet_type in perceptlet_types
        }
        self.correspondence_types = correspondence_types
        self.conceptual_spaces = conceptual_spaces
        self.workspace_concepts = workspace_concepts
        self.concepts = set.union(
            self.emotions,
            self.perceptlet_types,
            self.correspondence_types,
            self.conceptual_spaces,
            self.workspace_concepts,
        )
        self.concept_dictionary = {concept.name: concept for concept in self.concepts}
        self.spawning_concepts = set.union(perceptlet_types, workspace_concepts)
        self.logger = logger

    def __getitem__(self, key: str):
        return self.concept_dictionary[key]

    def __iter__(self):
        return (concept for concept in self.concepts)

    def get_random(self):
        return random.sample(self.concepts, 1)[0]

    def get_perceptlet_type_by_name(self, name: str) -> PerceptletType:
        return self.perceptlet_types_dictionary[name]

    def update_activations(self):
        self.spread_activations()
        for concept in self.concepts:
            concept.activation.update()
            self.logger.log(concept)

    def spread_activations(self):
        for concept in self.concepts:
            concept.spread_activation()
