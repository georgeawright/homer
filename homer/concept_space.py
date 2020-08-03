from typing import Set

from homer.concept import Concept
from homer.concepts.correspondence_type import CorrespondenceType
from homer.concepts.perceptlet_type import PerceptletType


class ConceptSpace:
    def __init__(
        self,
        perceptlet_types: Set[PerceptletType],
        correspondence_types: Set[CorrespondenceType],
        conceptual_spaces: Set[Concept],
        workspace_concepts: Set[Concept],
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

    def get_perceptlet_type_by_name(self, name: str) -> PerceptletType:
        return self.perceptlet_types_dictionary[name]
