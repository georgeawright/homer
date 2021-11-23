from __future__ import annotations
from typing import List, Tuple, Union

from homer.location import Location
from homer.variable import Variable


class ConceptVariable(Variable):
    """
    Including a list of possible concepts overrides the other constraints.
    """

    def __init__(
        self,
        location: Location,
        relations: List[Tuple["Concept", callable]] = None,
        # callable for getting the concept that should be related
        possible_concepts: List["Concept"] = None,
    ):
        self.location = location
        self.relations = [] if relations is None else relations
        self.possible_concepts = [] if possible_concepts is None else possible_concepts

    def subsumes(self, other: Union["Concept", ConceptVariable]) -> bool:
        if len(self.possible_concepts) > 0:
            if isinstance(other, Variable):
                return all(
                    concept in self.possible_concepts
                    for concept in other.possible_concepts
                )
            return other in self.possible_concepts
        if self.location is not None:
            if isinstance(self.location.space, Variable):
                if not self.location.space.subsumes(other.location.space):
                    return False
            else:
                if self.location.space != other.location.space:
                    return False
                for self_coordinates, other_coordinates in zip(
                    self.location.coordinates, other.location.coordinates
                ):
                    for self_i, other_i in zip(self_coordinates, other_coordinates):
                        if isinstance(self_i, Variable):
                            if not self_i.subsumes(other_i):
                                return False
                        else:
                            if self_i != other_i:
                                return False
        for parent_concept, relative in self.relations:
            if not other.has_relation_with(relative(), parent_concept=parent_concept):
                return False
        return True

    def has_relation_with(self, other, parent_concept=None) -> bool:
        for parent, relative in self.relations:
            if other == relative() and parent_concept == parent:
                return True
        return False
