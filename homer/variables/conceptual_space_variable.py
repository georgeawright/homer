from __future__ import annotations
from homer.variable import Variable


class ConceptualSpaceVariable(Variable):
    def __init__(self, possible_spaces: list = None):
        self.possible_spaces = [] if possible_spaces is None else possible_spaces

    def subsumes(self, other) -> bool:
        if len(self.possible_spaces) == 0:
            return True
        if isinstance(other, ConceptualSpaceVariable):
            if len(other.possible_spaces) == 0:
                return False
            for other_possible in other.possible_spaces:
                if other_possible not in self.possible_spaces:
                    return False
            return True
        return other in self.possible_spaces
