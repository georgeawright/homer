from typing import List

from homer.concept import Concept


class ConceptSpace:
    def __init__(
        self,
        conceptual_spaces: List[Concept],
        workspace_concepts: List[Concept],
        correspondence_concepts: List[Concept],
    ):
        self.conceptual_spaces = conceptual_spaces
        self.workspace_concepts = workspace_concepts
        self.correspondence_concepts = correspondence_concepts
        self.concepts = set.union(
            self.conceptual_spaces,
            self.workspace_concepts,
            self.correspondence_concepts,
        )
