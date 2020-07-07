from typing import List

from homer.concept import Concept


class ConceptSpace:
    def __init__(self, concepts: List[Concept]):
        self.concepts = concepts
