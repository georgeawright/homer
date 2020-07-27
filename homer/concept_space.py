from typing import List

from homer.concept import Concept


class ConceptSpace:
    def __init__(self, concepts: List[Concept], correspondence_concepts: List[Concept]):
        self.concepts = concepts
        self.correspondence_concepts = correspondence_concepts
