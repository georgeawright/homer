from typing import List

from homer.concept import Concept
from homer.concepts.correspondence_type import CorrespondenceType
from homer.concepts.perceptlet_type import PerceptletType


class ConceptSpace:
    def __init__(
        self,
        perceptlet_types: List[PerceptletType],
        correspondence_types: List[CorrespondenceType],
        conceptual_spaces: List[Concept],
        workspace_concepts: List[Concept],
    ):
        self.perceptlet_types = perceptlet_types
        self.correspondence_types = correspondence_types
        self.conceptual_spaces = conceptual_spaces
        self.workspace_concepts = workspace_concepts
        self.concepts = set.union(
            self.perceptlet_types,
            self.correspondence_types,
            self.conceptual_spaces,
            self.workspace_concepts,
        )
